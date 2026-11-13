"""Measure how much labelled personal data redactgate masks, on Gretel's
synthetic financial documents (Apache-2.0).

  python scripts/evaluate.py [--limit N] [--no-model]

A labelled span counts as masked when at least 80% of its characters are
covered by a detected span (of any label). The dataset's labels are
incomplete (some names and addresses are not labelled), so precision here is
a lower bound: a "false positive" can be real personal data the labels missed.
"""
import argparse
import collections
import json
import sys
import time
from pathlib import Path

import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from redactgate.detect import detect  # noqa: E402
from redactgate.redact import PERSONAL  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
# Dataset labels that are not personal data; reported, not counted in the headline.
NOT_PERSONAL = {"company", "date", "time", "date_time"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-model", action="store_true")
    ap.add_argument("--split", choices=["dev", "test"], default="dev",
                    help="dev = first 500 documents of the train split (for tuning); test = the test split")
    a = ap.parse_args()
    if a.split == "test":
        rows = pq.read_table(ROOT / "data/raw/en_test.parquet").to_pylist()
    else:
        rows = pq.read_table(ROOT / "data/raw/en_train.parquet").slice(0, 500).to_pylist()
    if a.limit:
        rows = rows[: a.limit]
    labels = PERSONAL | {"ORG"}
    per = collections.defaultdict(lambda: [0, 0])  # label -> [masked, total]
    chars_gold = chars_hit = pred_chars = pred_in_gold = 0
    docs_leak = 0
    misses = []
    t0 = time.time()
    for r in rows:
        text = r["generated_text"]
        gold = json.loads(r["pii_spans"]) if isinstance(r["pii_spans"], str) else r["pii_spans"]
        spans = detect(text, use_model=not a.no_model, labels=labels)
        personal_spans = [s for s in spans if s.label in PERSONAL]
        covered = bytearray(len(text))
        for s in personal_spans:
            covered[s.start:s.end] = b"\x01" * (s.end - s.start)
        covered_any = bytearray(covered)
        for s in spans:
            covered_any[s.start:s.end] = b"\x01" * (s.end - s.start)
        gold_mask = bytearray(len(text))
        leaked = False
        for g in gold:
            st, en, lab = g["start"], g["end"], g["label"]
            n = max(1, en - st)
            cov = covered_any if lab in NOT_PERSONAL else covered
            hit = sum(cov[st:en]) / n >= 0.8
            per[lab][0] += hit
            per[lab][1] += 1
            if lab not in NOT_PERSONAL:
                gold_mask[st:en] = b"\x01" * (en - st)
                chars_gold += en - st
                chars_hit += sum(covered[st:en])
                if not hit:
                    leaked = True
                    if len(misses) < 400:
                        misses.append({"label": lab, "value": text[st:en], "context": text[max(0, st - 60): en + 30]})
        docs_leak += leaked
        pred_chars += sum(covered)
        pred_in_gold += sum(1 for i, c in enumerate(covered) if c and gold_mask[i])
    secs = time.time() - t0
    personal = {k: v for k, v in per.items() if k not in NOT_PERSONAL}
    caught = sum(v[0] for v in personal.values())
    total = sum(v[1] for v in personal.values())
    method = "patterns only" if a.no_model else "patterns + NER model"
    lines = [f"# redactgate on Gretel synthetic_pii_finance_multilingual, {a.split} ({len(rows)} documents, {method})", "",
             f"- Personal-data spans masked (>=80% of characters): **{caught}/{total} = {caught / total:.1%}**",
             f"- Characters of personal data masked: {chars_hit}/{chars_gold} = {chars_hit / chars_gold:.1%}",
             f"- Documents with at least one labelled personal value left unmasked: {docs_leak}/{len(rows)} = {docs_leak / len(rows):.1%}",
             f"- Masked characters inside a labelled span (precision lower bound): {pred_in_gold / max(1, pred_chars):.1%}",
             f"- Time: {secs:.0f} s, {1000 * secs / len(rows):.0f} ms per document on CPU", "",
             "| label | masked | total | rate |", "|---|---|---|---|"]
    for k, (h, n) in sorted(per.items(), key=lambda kv: -kv[1][1]):
        note = " (not personal; masked only as ORG/any)" if k in NOT_PERSONAL else ""
        lines.append(f"| {k}{note} | {h} | {n} | {h / n:.0%} |")
    out = "\n".join(lines) + "\n"
    print(out)
    tag = f"{a.split}-" + ("patterns" if a.no_model else "model")
    if not a.limit:
        (ROOT / f"docs/results-{tag}.md").write_text(out)
    (ROOT / ".cache").mkdir(exist_ok=True)
    with open(ROOT / f".cache/misses-{tag}.jsonl", "w") as f:
        for m in misses:
            f.write(json.dumps(m) + "\n")


if __name__ == "__main__":
    main()
