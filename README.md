# Scribe Verify

**Can a small, non-generative model double-check an ambient AI scribe's note against the encounter transcript, sentence by sentence?**

This is a working mock-up of that idea, built on [Jev](https://docs.typesafe.ai) from TypeSafe AI. It takes an AI-drafted
psychiatry progress note and the transcript it was drafted from, asks Jev one question per sentence,
*"Is this statement supported by the encounter transcript?"*, and colours the draft by the answer:
**supported · contradicted · not found · ambiguous**. Click a sentence and it jumps to the transcript turn that
supports (or contradicts) it. The transcript is also checked in the other direction, so things the patient said
that never made it into the note are flagged as omissions.

**Live demo:** https://stephonomon.github.io/scribe-verify/  (self-contained page, results are embedded, no API calls from the browser)

![The draft on the left, colour-coded by transcript support; the transcript on the right with omission flags](docs/draft-view.png)

> Everything here is fabricated. There is no real patient, clinician, or recording. The encounter, the note,
> and the seeded errors were written for this demo. Nothing in this repository is medical advice or a validated
> clinical tool.

---

## Why

Ambient scribes (Abridge, Nuance DAX, Epic's own tools, and others) draft the note from the recording. The good
ones already let the clinician click a sentence and see the evidence in the transcript. Two failure modes still
land on the clinician at sign-off:

1. **Hallucination and drift.** The draft states something the patient never said, or states the opposite
   ("denies alcohol use" when the patient described three or four beers a night on weekends), or overstates
   ("sleep has improved" when the patient still wakes at 4 a.m. most nights).
2. **Omission.** Something clinically important was said and the draft simply doesn't have it. A handgun in the
   nightstand. A trazodone prescription from another doctor. A therapy waitlist.

The usual fix is to ask a second large language model to review the note. That works, but it is slow, expensive
at scale, and its "confidence" is whatever the model felt like writing. Jev is a different shape of model:
it does **no text generation**. You hand it a document (the *state*) and a set of typed questions (*Choice*,
*Noul*, *Score*), and it returns a calibrated probability distribution over the options for each one. That
makes it a natural fit for a verification layer:

- The question is fixed and auditable ("Is this statement supported by the transcript?"), not a free-form review.
- The output is a probability you can threshold. Below the threshold, route to human review; above it, auto-accept.
- Many questions can be asked of one document in a single call, which is exactly the shape of "check every
  sentence of this note against this transcript".

TypeSafe's own [citation check cookbook](https://docs.typesafe.ai/cookbooks/citation_check) does this for
LLM-generated citations against a source document (verified / contradicted / unsupported / fabricated, with an
auto-accept threshold). This repo is that recipe pointed at a clinical note.

## What it does

Two passes, both against the raw transcript, both using only Jev `choice` questions.

| Pass | Unit | Question asked of Jev | Options |
|---|---|---|---|
| Forward | each draft sentence | Is this statement supported by the encounter transcript? | `supported` · `contradicted` · `not_found` · `ambiguous` |
| Forward | each draft sentence | Which single transcript turn is the primary evidence for or against it? | `T01` … `T74` · `none` |
| Reverse | each transcript turn, with the preceding turn as context | Does the draft note capture the clinically relevant content of this turn? | `captured` · `partially` · `omitted` · `contradicted` · `not_clinical` |

The forward pass colours the draft and gives click-to-source. The reverse pass finds omissions. Confidence is
Jev's own calibrated probability for the chosen option; sentences below the auto-accept slider get a dashed
underline for human review, mirroring the cookbook's `AUTO_ACCEPT` threshold.

![A transcript turn opened to show the omission verdict, its probability bars, and the draft sentence that contradicts it](docs/omission-view.png)

### The viewer

- **Left:** the AI draft, one span per sentence. Colour encodes the verdict; the underline style encodes whether it cleared the threshold.
- **Right:** the transcript with timestamps and speaker. Turns the draft missed or contradicted carry a flag.
- Click a sentence to open its verification card (verdict, probabilities, the source turn quoted, other candidate turns) and scroll the transcript to the source.
- Click a transcript flag to see the capture verdict and which draft sentences cite that turn.
- The header chips filter the draft by verdict. **Support colors** turns the colouring off for a before/after. **IDs** shows sentence IDs.
- Accept / Edit / Remove / Add to draft are placeholders that show where this would plug into a real scribe's sign-off flow.

## Results

Run on 2026-09-21 with `jev-1.13.0`. The draft has 37 sentences; each one carries a hidden ground-truth label
(`ok`, `contradicted`, `hallucinated`, `ambiguous`, or `observation`) in [`data.py`](data.py) that the model never sees.

| | |
|---|---|
| Forward verdicts matching the seeded label | **33 / 37** |
| Seeded hallucinations (improved appetite; bipolar family history) | both `not_found` at 1.00, source `none` |
| Seeded contradictions (denies alcohol, denies SI, sertraline 100 mg, weekly CBT, discontinue trazodone, six-week follow-up, one week off work, resumed painting, no side effects, denies cannabis) | all caught, 0.71 to 1.00 |
| The four misses | all defensible readings at lower confidence (below) |
| Omissions surfaced by the reverse pass | early-waking frequency, trazodone grogginess, therapy waitlist, and more |
| Whole run | 111 API calls, 6 in parallel, 6.9 s wall clock, 321k input tokens |

The four "misses" are the interesting ones, because in each case the ground-truth label was a judgement call:

| Sentence | Seeded | Jev said | Why Jev has a point |
|---|---|---|---|
| Panic attacks have resolved. | ambiguous | contradicted 0.82 | Patient had one mild attack last month. "Resolved" is false. |
| Patient agreed to remove the firearm from the home. | ambiguous | contradicted 0.77 | She agreed to *ask about a safe* and explicitly would not promise removal. |
| Safety plan completed and 988 crisis line provided. | ok | ambiguous 0.89 | The transcript only agrees to do it before she leaves; it isn't shown happening. |
| Add bupropion for sexual side effects. | contradicted | ambiguous 0.74 | The clinician raised bupropion but deferred it four weeks. |

Mental status exam sentences ("well groomed, cooperative") come back `not_found`. That is correct: they are the
clinician's observations, not something anyone said, and the viewer treats them as a separate category
rather than as errors.

### One call, many questions

The 111-call run treats each sentence as its own request. Jev's API also accepts many questions over one
`state` in a single call. [`fanout_probe.py`](fanout_probe.py) sends all 37 forward questions in one request:

| | 37 separate calls | 1 call × 37 questions |
|---|---|---|
| Latency | 15.1 s summed (6.9 s wall, 6-wide) | **0.90 s** |
| Input tokens | 222,722 | **13,044** |
| Verdicts | — | identical, 37 / 37 |

That is the property that makes this shape interesting for scribing: a short transcript supports dozens of
independent yes/no questions, and they can all ride on one copy of the transcript.

## Limitations, honestly

- **It is one fabricated encounter.** The errors were seeded by the same author who wrote the transcript. Real scribe errors are subtler and real transcripts are messier (crosstalk, ASR errors, three people in the room).
- **Clinician-question noise.** In the reverse pass, a clinician's question ("Has that changed from before?") sometimes gets flagged "draft says otherwise" because the draft denies the thing the question presupposes. Arguably right, but noisy. Flags below 0.5 are rendered faded.
- **Sentence segmentation is given, not derived.** A real system has to split the note into checkable claims; compound sentences hide multiple claims.
- **Not_found is not the same as wrong.** Prior history, chart data, and the clinician's exam all legitimately land in a note without being spoken. A production version needs provenance categories beyond "the transcript".
- **No clinical validation of any kind.** This is a mock-up to make the architecture concrete.
- **Business-associate status.** Transcripts are PHI. Whether a given vendor can receive them is a contracting question this repo doesn't answer.

## What I'd benchmark next

One transcript × ~50 Jev questions in a single call, versus one transcript × one structured-output request to a
frontier LLM, on:

- latency and cost per encounter
- extraction accuracy against the seeded labels
- stability when fields are added or removed from the schema (does changing one question perturb the others?)
- confidence calibration (does 0.8 mean 80%?)

The seeded ground truth in `data.py` is already set up for it.

## Run it yourself

Python 3.10+, standard library only. You need a TypeSafe API key from https://console.typesafe.ai.

```bash
export TYPESAFE_API_KEY=...          # or put it in ~/.typesafe_api_key
python verify.py                     # both passes → results.json (about 7 s)
python build.py                      # embeds results.json into template.html → index.html
python fanout_probe.py               # the single-call comparison
open index.html
```

| File | What it is |
|---|---|
| [`data.py`](data.py) | The 74-turn transcript, the 37-sentence draft with hidden ground-truth labels, and the omission ground truth |
| [`verify.py`](verify.py) | The two Jev passes. The question definitions are at the top and are the whole "prompt" |
| [`fanout_probe.py`](fanout_probe.py) | All forward questions in one API call, compared against `results.json` |
| [`template.html`](template.html) | The viewer (no framework, no build step, works offline) |
| [`build.py`](build.py) | Embeds `results.json` into the template and strips the ground-truth labels |
| [`index.html`](index.html) | The built page that GitHub Pages serves |
| [`results.json`](results.json) | The run reported above, so you can inspect every probability without an API key |

The Jev request shape, for reference (see the [docs](https://docs.typesafe.ai) for the full API):

```json
POST https://api.typesafe.ai/v1/systemone
{
  "model": "jev-1.13.0",
  "state": { "transcript": "[T01 00:00 Clinician] Hi Maya ...", "claim": "Patient denies alcohol use." },
  "questions": {
    "relation": {
      "type": "choice",
      "instructions": "Is the `claim` supported by the encounter `transcript`?",
      "criteria": {
        "supported":    { "what": "The transcript states the claim or directly implies it is true" },
        "contradicted": { "what": "The transcript states the opposite of the claim ..." },
        "not_found":    { "what": "Nothing in the transcript addresses what the claim asserts" },
        "ambiguous":    { "what": "The transcript addresses the claim but the evidence is mixed or partial" }
      }
    }
  }
}
```

Response: `answers.relation.choice` plus `answers.relation.probabilities` over the four options.

## Links

- Jev / TypeSafe AI docs: https://docs.typesafe.ai
- The cookbook this is modelled on: https://docs.typesafe.ai/cookbooks/citation_check
- TypeSafe console (API keys): https://console.typesafe.ai

## Credits and disclosures

Concept and direction: [Stephon Proctor](https://github.com/Stephonomon), PhD, MBI, ABPP, ACHIP.

The code, the fabricated encounter and draft note, the seeded errors, the viewer, and the first draft of this README
were written by Claude (Claude Code, model Fable 5.1) working from that direction; the author set the direction and ran the results.
The Jev results reported above are real API responses, not simulated.

No affiliation with TypeSafe AI, Abridge, Epic, Nuance, or any scribe vendor. No funding. The author's employer
had no role in this.

MIT licensed. See [LICENSE](LICENSE).
