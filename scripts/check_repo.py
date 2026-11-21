"""Static repository checks (nothing is run, no DuckDB needed).

* every Python script compiles (warnings count as errors)
* every local link and image in the README points to a file that exists
* the raw CSV has the 41 columns the pipeline expects, and no secrets file is tracked
"""
import csv
import os
import re
import subprocess
import sys
import urllib.parse
import warnings

problems = []
tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True, encoding="utf-8").stdout.splitlines()
tracked = [t.strip('"') for t in tracked]

warnings.simplefilter("error", SyntaxWarning)
py = sorted(t for t in tracked if t.endswith(".py"))
for f in py:
    with open(f, encoding="utf-8") as fh:
        try:
            compile(fh.read(), f, "exec")
        except (SyntaxError, SyntaxWarning) as exc:
            problems.append(f"{f}: does not compile: {exc}")

if ".env" in tracked:
    problems.append(".env is tracked by git")

with open("README.md", encoding="utf-8") as fh:
    readme = fh.read()
n_links = 0
# markdown links and images; file names may contain one level of parentheses
for target in re.findall(r"\]\(((?:[^()\s]|\([^)]*\))+)\)", readme):
    if re.match(r"^(https?:|#|mailto:)", target):
        continue
    n_links += 1
    path = urllib.parse.unquote(target.split("#")[0])
    if not os.path.exists(path):
        problems.append(f"README: link to a missing file: {path}")

raw = "data/311_Elevator_Service_Requests_.csv"
with open(raw, encoding="utf-8", newline="") as fh:
    header = next(csv.reader(fh))
if len(header) != 41 or "Complaint Type" not in header or "Created Date" not in header or "Closed Date" not in header:
    problems.append(f"{raw}: unexpected header ({len(header)} columns)")

print(f"Checked {len(py)} Python scripts, {n_links} local README links, the raw CSV header, {len(problems)} problem(s)")
for p in problems:
    print("FAIL ", p)
sys.exit(1 if problems else 0)
