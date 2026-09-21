"""Run Jev citation checks in both directions and write results.json.
Forward:  each draft claim -> relation {supported, contradicted, not_found, ambiguous} + primary source turn.
Reverse:  each transcript turn -> is its content captured by the draft? {captured, partially, omitted, not_clinical}.
"""
import json, os, sys, time, urllib.request, concurrent.futures as cf
from data import TRANSCRIPT, CLAIMS, PATIENT

def _key():
    k = os.environ.get("TYPESAFE_API_KEY")
    if k: return k.strip()
    p = os.path.expanduser("~/.typesafe_api_key")
    if os.path.exists(p): return open(p).read().strip()
    sys.exit("Set TYPESAFE_API_KEY or put your key in ~/.typesafe_api_key (get one at https://console.typesafe.ai)")
KEY = _key()
URL, MODEL = "https://api.typesafe.ai/v1/systemone", "jev-1.13.0"
TX = "\n".join(f"[{t['id']} {t['t']} {'Clinician' if t['speaker']=='DR' else 'Patient'}] {t['text']}" for t in TRANSCRIPT)
DRAFT_TXT = "\n".join(f"[{c['id']} {c['section']}] {c['text']}" for c in CLAIMS)

def jev(state, questions):
    body = {"model": MODEL, "state": state, "questions": questions}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)
        except Exception as e:
            if attempt == 2: raise
            time.sleep(2)

RELATION = {"type": "choice",
  "instructions": "The `claim` is one sentence from an AI-drafted psychiatric progress note. Is it supported by the encounter `transcript`? Judge only what was said in the transcript, not clinical plausibility.",
  "criteria": {
    "supported":    {"what": "The transcript states the claim or directly implies it is true, even in different words or units"},
    "contradicted": {"what": "The transcript states the opposite of the claim, or gives a different value/fact that makes the claim false (wrong dose, wrong duration, denies something the patient endorsed)"},
    "not_found":    {"what": "Nothing in the transcript addresses what the claim asserts; the content would have to have come from somewhere else",
                     "not_for": "Claims the transcript does address but only partially or vaguely (that is `ambiguous`)"},
    "ambiguous":    {"what": "The transcript addresses the claim but the evidence is mixed, partial, hedged, or overstated by the claim, so a clinician should look before signing"}}}

def source_q(): 
    crit = {t["id"]: {"what": f"Turn {t['id']} ({'clinician' if t['speaker']=='DR' else 'patient'}, {t['t']}) is the primary turn that addresses the claim"} for t in TRANSCRIPT}
    crit["none"] = {"what": "No turn in the transcript addresses the claim"}
    return {"type": "choice", "instructions": "Which single transcript turn is the primary evidence for or against the `claim`? Prefer the patient's answer over the clinician's question when both exist.", "criteria": crit}
SOURCE = source_q()

CAPTURE = {"type": "choice",
  "instructions": "Does the AI-drafted `note` capture the clinically relevant content of this transcript `turn`? The note is for a psychiatrist; medications, substance use, safety/risk factors, side effects, symptoms, stressors, and plan items are all clinically relevant.",
  "criteria": {
    "captured":     {"what": "The note contains the substance of this turn (wording may differ)"},
    "partially":    {"what": "The note mentions the topic but misses a clinically meaningful detail from this turn, or states it differently"},
    "omitted":      {"what": "This turn contains clinically relevant information that appears nowhere in the note"},
    "contradicted": {"what": "The note addresses this topic but states something different from what this turn says (e.g. denies something the patient endorsed, wrong dose, wrong timeframe)"},
    "not_clinical": {"what": "This turn is a greeting, transition, pleasantry, acknowledgement, or a clinician question whose answer is in the next turn; nothing new to capture from this turn itself"}}}

def forward(c):
    t0 = time.time(); r = jev({"transcript": TX, "claim": c["text"]}, {"relation": RELATION, "source": SOURCE})
    a = r["answers"]; rel, src = a["relation"], a["source"]
    top = sorted(src["probabilities"].items(), key=lambda kv: -kv[1])[:3]
    return {**c, "verdict": rel["choice"], "confidence": round(rel["probabilities"][rel["choice"]], 3),
            "probs": {k: round(v, 3) for k, v in rel["probabilities"].items()},
            "source": src["choice"], "source_conf": round(src["probabilities"][src["choice"]], 3),
            "source_alts": [[k, round(v, 3)] for k, v in top if v > 0.05],
            "usage": r["usage"], "latency_s": round(time.time() - t0, 2)}

def reverse(t):
    i = int(t["id"][1:]) - 1; prev = TRANSCRIPT[i-1] if i else None
    ctx = f"[{prev['id']} {'Clinician' if prev['speaker']=='DR' else 'Patient'}] {prev['text']}" if prev else "(start of encounter)"
    t0 = time.time(); r = jev({"note": DRAFT_TXT, "preceding_turn_for_context": ctx, "turn": f"[{t['id']} {'Clinician' if t['speaker']=='DR' else 'Patient'}] {t['text']}"}, {"capture": CAPTURE})
    a = r["answers"]["capture"]
    return {**t, "capture": a["choice"], "confidence": round(a["probabilities"][a["choice"]], 3),
            "probs": {k: round(v, 3) for k, v in a["probabilities"].items()}, "usage": r["usage"], "latency_s": round(time.time() - t0, 2)}

if __name__ == "__main__":
    t0 = time.time()
    with cf.ThreadPoolExecutor(6) as ex:
        fwd = list(ex.map(forward, CLAIMS)); rev = list(ex.map(reverse, TRANSCRIPT))
    tok = sum(x["usage"]["input_tokens"] for x in fwd + rev), sum(x["usage"]["output_tokens"] for x in fwd + rev)
    out = {"patient": PATIENT, "model": MODEL, "run_at": time.strftime("%Y-%m-%d %H:%M"), "wall_s": round(time.time() - t0, 1),
           "calls": len(fwd) + len(rev), "input_tokens": tok[0], "output_tokens": tok[1], "claims": fwd, "turns": rev}
    json.dump(out, open("results.json", "w"), indent=1)
    print(f"{out['calls']} calls, {out['wall_s']}s wall, {tok[0]} in / {tok[1]} out tokens")
    print("\nFORWARD (seed -> verdict)")
    for c in fwd: print(f"  {c['id']} {c['seed']:12} -> {c['verdict']:12} {c['confidence']:.2f}  src={c['source']}({c['source_conf']:.2f})  {c['text'][:60]}")
    print("\nREVERSE (turns flagged omitted/partially)")
    for t in rev:
        if t["capture"] in ("omitted", "partially"): print(f"  {t['id']} {t['capture']:9} {t['confidence']:.2f}  {t['text'][:70]}")
