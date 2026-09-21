"""Probe: 1 transcript x 37 relation questions in ONE Jev call, vs the 37 separate calls in results.json."""
import json, time
from verify import jev, TX, RELATION, CLAIMS
qs = {c["id"]: {**RELATION, "instructions": f"Claim {c['id']}: \"{c['text']}\" — " + RELATION["instructions"].replace("The `claim` is one sentence", "This claim is one sentence")} for c in CLAIMS}
t0 = time.time(); r = jev({"transcript": TX}, qs); lat = time.time() - t0
sep = {c["id"]: c for c in json.load(open("results.json"))["claims"]}
agree = 0
for c in CLAIMS:
    a = r["answers"][c["id"]]; s = sep[c["id"]]
    same = a["choice"] == s["verdict"]; agree += same
    if not same: print(f"  DIFF {c['id']}: fanout={a['choice']} ({a['probabilities'][a['choice']]:.2f})  separate={s['verdict']} ({s['confidence']:.2f})  {c['text'][:55]}")
print(f"1 call x {len(qs)} questions: {lat:.2f}s, {r['usage']['input_tokens']} in / {r['usage']['output_tokens']} out; agreement with separate calls {agree}/{len(qs)}")
sep_lat = sum(s["latency_s"] for s in sep.values()); sep_in = sum(s["usage"]["input_tokens"] for s in sep.values())
print(f"37 separate calls: {sep_lat:.1f}s summed latency (ran 6-wide), {sep_in} input tokens")
