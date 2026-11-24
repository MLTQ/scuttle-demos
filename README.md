# Scuttle Demo Graphs & Sample Vault

Ready-to-run real-world linked document graphs and a sample Markdown/Obsidian vault for **[Scuttle](https://github.com/MLTQ/scuttle)** ([`Multiqueue/scuttle-1.7b`](https://huggingface.co/Multiqueue/scuttle-1.7b)).

Kept in a dedicated companion repository so the main [`MLTQ/scuttle`](https://github.com/MLTQ/scuttle) codebase stays clean and lightweight.

---

## Included Demos

| Path | Size | Documents | Links | Description | Data License |
| --- | ---: | ---: | ---: | --- | --- |
| `graphs/ecfr-law-graph.json.gz` | 5.5 MB | 21,879 | 21,438 | US Federal Law (eCFR Titles 11, 17, 21, 27, 37, 47) linked by statutory `§` cross-references | US Gov Public Domain |
| `graphs/wikispeedia-graph.json.gz` | 7.1 MB | 4,604 | 119,772 | Wikispeedia Wikipedia subset linked by reading-order hyperlinks | CC-BY-SA 3.0 |
| `vault/` | 4 KB | 6 | 9 | Sample Markdown/Obsidian engineering wiki (`[[wikilinks]]` + `[markdown](links.md)`) | MIT |

---

## 10-Second Quickstart

```bash
# 1. Install Scuttle (with 4-bit NF4 support = 1.70 GiB static VRAM, 100% accuracy retention)
pip install "scuttle-search[quant] @ git+https://github.com/MLTQ/scuttle.git"

# 2. Clone these demo graphs
git clone https://github.com/MLTQ/scuttle-demos.git
cd scuttle-demos

# 3. Run all three demos (US Federal Law, Wikispeedia, and local Markdown vault indexing)
python run_demo.py --quant 4bit
```

Or try individual CLI commands:

```bash
# Search US Federal Law (securities exemptions)
scuttle search \
  --graph graphs/ecfr-law-graph.json.gz \
  --query "exemption from registration for private securities offerings to accredited investors" \
  --quant 4bit

# Search Wikispeedia (masked conceptual query — target title not in query!)
scuttle search \
  --graph graphs/wikispeedia-graph.json.gz \
  --query "15th-century Inca citadel perched high in the Andes Mountains of Peru" \
  --quant 4bit

# Index the sample Markdown vault and search it
scuttle index vault -o vault-graph.json.gz --domain engineering --noun note
scuttle search \
  --graph vault-graph.json.gz \
  --query "how do we rotate expired signing keys without dropping active sessions?" \
  --quant 4bit
```

## Using with the Scuttle MCP Server

Point `scuttle-mcp` straight at `graphs/` so your AI agent (Antigravity, Claude Code, Cursor, Codex) can query `ecfr-law` and `wikispeedia` by name:

```json
{
  "mcpServers": {
    "scuttle": {
      "command": "scuttle-mcp",
      "args": [
        "--quant", "4bit",
        "--idle-offload", "120",
        "--graphs", "/absolute/path/to/scuttle-demos/graphs"
      ]
    }
  }
}
```

## Attribution & Data Licenses

- **Code, scripts, and `vault/`:** [MIT License](LICENSE).
- **`graphs/ecfr-law-graph.json.gz`:** Built from official US Electronic Code of Federal Regulations (eCFR) XML published by the US Government Publishing Office / Office of the Federal Register (Public Domain under 17 U.S.C. § 105).
- **`graphs/wikispeedia-graph.json.gz`:** Derived from the Stanford SNAP / EPFL Wikispeedia dataset and Wikipedia article extracts (CC-BY-SA 3.0).
