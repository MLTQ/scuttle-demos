#!/usr/bin/env python3
"""Run Scuttle live across US Federal Law (eCFR), Wikispeedia, and the sample Markdown vault."""
import argparse
import tempfile
from pathlib import Path

from scuttle import ScuttleSearcher, ScuttleWorker, index_directory, load_world


def show(title, res):
    print(f"\n=== {title} ===")
    print(f"Query: {res['query']}")
    print(f"Reads: {res['reads_used']}/{res['budget']}")
    for hit in (res["contributing"] or res["top_pages"][:3])[:5]:
        tag = "SEED" if hit["from_seed"] else f"HOP (step {hit['read_step']})"
        print(f"  [{hit['p_contributes']:.3f}] [{tag}] {hit['title']}")
        if len(hit["trail"]) > 1:
            print("     Trail: " + " -> ".join(t["title"][:45] for t in hit["trail"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Multiqueue/scuttle-1.7b")
    ap.add_argument("--quant", choices=["none", "bf16", "8bit", "4bit"], default="4bit")
    ap.add_argument("--device", default="auto")
    a = ap.parse_args()

    root = Path(__file__).resolve().parent
    worker = ScuttleWorker(a.model, device=a.device, quant=a.quant)

    # 1. US Federal Law (eCFR)
    ecfr = load_world(root / "graphs" / "ecfr-law-graph.json.gz")
    res = ScuttleSearcher(ecfr, worker=worker).search(
        "exemption from registration for private securities offerings to accredited investors",
        budget=12,
    )
    show("US Federal Law (eCFR)", res)

    # 2. Wikispeedia (masked conceptual query)
    wiki = load_world(root / "graphs" / "wikispeedia-graph.json.gz")
    res = ScuttleSearcher(wiki, worker=worker).search(
        "15th-century Inca citadel perched high in the Andes Mountains of Peru",
        budget=12,
    )
    show("Wikispeedia (Masked Topic)", res)

    # 3. Sample Markdown / Obsidian vault indexed on the fly
    with tempfile.TemporaryDirectory() as td:
        gpath = Path(td) / "vault-graph.json.gz"
        index_directory(root / "vault", gpath, domain="engineering", doc_noun="note")
        vault = load_world(gpath)
        res = ScuttleSearcher(vault, worker=worker).search(
            "how do we rotate expired signing keys without dropping active sessions?",
            n_seeds=2,
            budget=6,
        )
        show("Sample Markdown Vault (On-the-fly Index)", res)


if __name__ == "__main__":
    main()
