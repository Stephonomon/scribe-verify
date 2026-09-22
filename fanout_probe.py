"""The real-life Jev shape for one encounter: every forward question over ONE copy of the transcript, in as few calls as the
64k-token request cap allows. Compared against the 37 separate per-sentence calls recorded in results.json.
  Run A: 37 support questions in one call.
  Run B: 37 support + 37 source-turn questions. A source question has 75 options, so ~2.9k tokens each; 37 of them exceed
         the cap, so they are chunked: 1 support call + 2 source calls, run in parallel."""
import json, time, concurrent.futures as cf
from verify import jev, TX, RELATION, CLAIMS, TRANSCRIPT

sep = {c["id"]: c for c in json.load(open("results.json"))["claims"]}
def q_support(c): return {**RELATION, "instructions": f"Claim {c['id']}: \"{c['text']}\" — " + RELATION["instructions"].replace("The `claim` is one sentence", "This claim is one sentence")}
SRC_CRIT = {t["id"]: {"what": f"{t['id']} ({'clinician' if t['speaker']=='DR' else 'patient'}) is the primary turn addressing the claim"} for t in TRANSCRIPT}; SRC_CRIT["none"] = {"what": "No turn addresses the claim"}
def q_source(c): return {"type": "choice", "instructions": f"Claim {c['id']}: \"{c['text']}\" — Which single transcript turn (by its [Txx] tag) is the primary evidence for or against this claim? Prefer the patient's answer over the clinician's question; for plan items, prefer the clinician's statement over the patient's acknowledgement.", "criteria": SRC_CRIT}
def timed(qs):
    t0 = time.time(); r = jev({"transcript": TX}, qs); return r, time.time() - t0

sep_lat = sum(s["latency_s"] for s in sep.values()); sep_in = sum(s["usage"]["input_tokens"] for s in sep.values())
print(f"37 separate per-sentence calls (support + source): {sep_lat:.1f}s summed latency, {sep_in} input tokens\n")

rA, lA = timed({c["id"]: q_support(c) for c in CLAIMS})
agree = sum(rA["answers"][c["id"]]["choice"] == sep[c["id"]]["verdict"] for c in CLAIMS)
print(f"A: 1 call x 37 support questions: {lA:.2f}s, {rA['usage']['input_tokens']} in / {rA['usage']['output_tokens']} out; verdict agreement {agree}/37\n")

half = len(CLAIMS) // 2
batches = [{c["id"]: q_support(c) for c in CLAIMS}, {c["id"]+"_src": q_source(c) for c in CLAIMS[:half]}, {c["id"]+"_src": q_source(c) for c in CLAIMS[half:]}]
t0 = time.time()
with cf.ThreadPoolExecutor(3) as ex: results = list(ex.map(timed, batches))
wall = time.time() - t0
answers = {}; [answers.update(r["answers"]) for r, _ in results]
tin = sum(r["usage"]["input_tokens"] for r, _ in results); tout = sum(r["usage"]["output_tokens"] for r, _ in results)
va = sum(answers[c["id"]]["choice"] == sep[c["id"]]["verdict"] for c in CLAIMS)
sa = sum(answers[c["id"]+"_src"]["choice"] == sep[c["id"]]["source"] for c in CLAIMS)
for c in CLAIMS:
    v = answers[c["id"]]; s = sep[c["id"]]
    if v["choice"] != s["verdict"]: print(f"  VERDICT DIFF {c['id']}: fanout={v['choice']} ({v['probabilities'][v['choice']]:.2f})  separate={s['verdict']} ({s['confidence']:.2f})  {c['text'][:50]}")
    a = answers[c["id"]+"_src"]
    if a["choice"] != s["source"]: print(f"  SRC DIFF {c['id']}: fanout={a['choice']} ({a['probabilities'][a['choice']]:.2f})  separate={s['source']} ({s['source_conf']:.2f})  {c['text'][:50]}")
print(f"\nB: real-life shape, {len(batches)} calls in parallel ({', '.join(str(r['usage']['input_tokens']) for r, _ in results)} tokens each): "
      f"{wall:.2f}s wall, {tin} in / {tout} out; verdict agreement {va}/37, source agreement {sa}/37")
json.dump({"A": {"calls": 1, "latency_s": round(lA, 2), "input_tokens": rA["usage"]["input_tokens"], "output_tokens": rA["usage"]["output_tokens"], "verdict_agreement": agree},
           "B": {"calls": len(batches), "wall_s": round(wall, 2), "per_call_input": [r["usage"]["input_tokens"] for r, _ in results], "input_tokens": tin, "output_tokens": tout, "verdict_agreement": va, "source_agreement": sa}},
          open("fanout_result.json", "w"), indent=1)
