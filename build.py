"""Embed results.json into template.html -> index.html (self-contained, no fetch needed)."""
import json
data = json.load(open("results.json"))
for c in data["claims"]: c.pop("seed", None)   # ground truth never shipped to the viewer
html = open("template.html").read().replace("__DATA__", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
open("index.html", "w").write(html); print(f"index.html {len(html)/1024:.0f} KB")
