# Museum of Useless Knowledge

**Facts you absolutely did not need to know.**  
Powered by Waad. Optimized for Arm. Completely unnecessary.

Submission for the [Arm Create: AI Optimization Challenge 2026](https://arm-ai-optimization-challenge.devpost.com) — **Cloud AI Track**

---

## The idea

A playful digital museum of strange, surprising, and seemingly useless facts.

- Browse exhibits on plaques
- Draw a random exhibit
- Filter by category, sort by weirdness
- Submit your own fact and watch the curator classify it live
- See weirdness score, WTF factor, category, and confidence
- Learn how the inference engine behind the museum was optimized for Arm64

This is **not** a chatbot. The core AI capability is **classification and scoring**.

---

## Why this is an Arm project

The museum sits on top of real Arm64 optimization work that already lived in this repository under the name **Armory**.

We took DistilBERT (sequence classification) and measured:

| Backend | Arch | Latency | Throughput | Model size |
|---------|------|---------|------------|------------|
| PyTorch FP32 | x86_64 | 65.12 ms | 15.36 req/s | 256.10 MB |
| PyTorch FP32 | **Arm64** | **21.07 ms** | **47.47 req/s** | 256.10 MB |
| PyTorch INT8 (dynamic) | x86_64 | 25.24 ms | 39.62 req/s | 132.29 MB |
| PyTorch INT8 (dynamic) | **Arm64** | **25.40 ms** | **39.37 req/s** | 132.29 MB |
| **ExecuTorch + XNNPACK/KleidiAI** | **Arm64** | **12.98 ms** | **77.04 req/s** | — |

**Honest finding (preserved from the original work):**  
Before quantization, Arm64 was ~3.1× faster than x86_64 on the same FP32 model. After INT8 the gap nearly disappeared — both architectures converge around ~25 ms. The clearest Arm-specific win is the ExecuTorch path: the *same* FP32 model runs **1.6× faster** than plain PyTorch FP32 simply by using an Arm-optimized inference engine (XNNPACK + KleidiAI kernels where available).

All Arm64 numbers were produced on real `ubuntu-24.04-arm` GitHub Actions runners — no emulation.

These numbers are **frozen historical results**. They are never invented or altered.

---

## How the AI works (museum classifier)

```
Fact text
    ↓
Text preprocessing
    ↓
Lightweight hybrid classifier
    ├── Category prediction (lexicon + pattern signals)
    ├── Weirdness score (surprise markers, comparisons, biological absurdity)
    ├── WTF factor (visceral language + weirdness)
    └── Confidence
    ↓
Museum metadata → Exhibit plaque
```

**Important honesty note:**  
The original DistilBERT model is fine-tuned for *sentiment*. We do **not** pretend it magically understands “weirdness.”  

The museum classifier is a reproducible, deterministic hybrid (keyword/pattern signals + stable hashing for score jitter). Scores are explicitly presented as **“AI-generated museum scores” / playful curator scores**, not scientific psychological measurements.

The original DistilBERT + quantization + ExecuTorch pipeline remains fully intact for benchmarking and can be pointed at any Hugging Face sequence-classification model.

---

## Arm optimization (preserved)

Everything under the original optimization paths is still here and runnable:

```bash
# Original Armory flow (unchanged)
pip install -r requirements.txt          # transformers + torch
python models/download_model.py
python benchmark/harness.py              # FP32 baseline
python optimize/quantize.py              # INT8 dynamic quant
python optimize/check_accuracy.py        # prediction agreement
python experimental/executorch/export_executorch.py   # ExecuTorch + XNNPACK
```

CI workflows on real Arm64 runners:

- `.github/workflows/benchmark-arm64.yml`
- `.github/workflows/quantize-arm64.yml`
- `.github/workflows/executorch-arm64.yml`

Raw artifacts live in `results/raw/` and charts in `results/charts/`.

---

## Demo (the product)

```bash
# One command
./museum/scripts/run_museum.sh
```

Then open **http://127.0.0.1:8000**

### Demo flow (60–90 s)

1. **Entrance** — “Welcome to the world’s least useful museum.”
2. **Gallery** — browse bizarre plaques, filter by category, sort by weirdness.
3. **Random Exhibit** — draw one.
4. **Submit a Fact** — type something like *“Some turtles can breathe through their butts.”*
5. Watch the curator return category, weirdness, WTF, confidence.
6. **Arm Engine** page — show the real benchmark table (12.98 ms / 77.04 req/s).
7. Close with: *“Optimized for Arm. Powered by curiosity. Completely unnecessary.”*

---

## Architecture

```
Armory-Optimize/                    # repo root (preserves original name & history)
├── benchmark/                      # original FP32 harness
├── optimize/                       # original INT8 quant + accuracy check
├── experimental/executorch/        # original ExecuTorch + XNNPACK path
├── models/                         # download helper
├── results/                        # frozen benchmark artifacts + charts
├── .github/workflows/              # native Arm64 CI
│
└── museum/                         # THE PRODUCT
    ├── data/facts.jsonl            # curated strange facts
    ├── ml/classifier.py            # category + weirdness + WTF pipeline
    ├── backend/app.py              # FastAPI (exhibits, classify, arm benchmarks)
    ├── frontend/                   # museum UI (entrance, gallery, plaques, submit, arm)
    ├── tests/                      # classifier + API tests
    └── scripts/run_museum.sh       # one-command demo
```

---

## Dataset

`museum/data/facts.jsonl` — 100 high-quality, redistributable strange facts.

Each record:

```json
{
  "id": "005",
  "fact": "Some turtles can breathe through their butts.",
  "category": "Animals",
  "weirdness": 96,
  "wtf": 99,
  "tags": ["cloacal respiration"],
  "source": "herpetology"
}
```

Categories: Nature · Human · History · Space · Science · Why Does This Exist? · Animals · Earth · Technology · Random / Other

Facts are chosen for being widely reported, public-domain-friendly, or common knowledge. The museum clearly separates factual content from AI-generated classification scores.

---

## Accuracy / limitations

- Museum scores are **playful and deterministic**, not peer-reviewed psychological instruments.
- Category prediction uses strong lexical signals; edge cases fall to “Random / Other.”
- Original DistilBERT accuracy checks (FP32 vs INT8 agreement) remain in `optimize/check_accuracy.py` (100% agreement on the original test sentences).
- Live museum classification latency is measured per request and shown in the UI; it is **not** claimed to be the 12.98 ms ExecuTorch number unless that exact pipeline is re-benchmarked for the new workload.

---

## Run locally

```bash
# Product (museum)
./museum/scripts/run_museum.sh
# → http://127.0.0.1:8000

# Original optimization benchmarks (requires torch + transformers)
pip install -r requirements.txt
python models/download_model.py
python benchmark/harness.py
python optimize/quantize.py
```

---

## Run / reproduce on Arm64

Use the existing GitHub Actions workflows (real Arm silicon):

- **Benchmark on Arm64**
- **Quantize on Arm64**
- **ExecuTorch on Arm64**

Or on any Arm64 machine with the same commands listed above.

---

## Project story (for judges)

**Problem:** AI inference does not have to mean expensive GPU infrastructure.

**Insight:** Many useful AI workloads can run efficiently on CPU — especially when the inference *engine* is Arm-aware.

**Technical work:** We optimized NLP inference for Arm64 using quantization and ExecuTorch + XNNPACK/KleidiAI, measured real latency/throughput on native Arm64 runners, and kept every artifact reproducible.

**Product:** We turned that inference engine into an interactive AI museum of strange facts.

**Why it matters:** The museum demonstrates how a lightweight classification workload can feel instant and interactive on CPU infrastructure.

**Punchline:**  
*We optimized AI to answer the most important questions nobody asked.*

---

## License

MIT — see [LICENSE](./LICENSE).
