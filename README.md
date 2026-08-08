# Armory: Arm64 vs x86 AI Inference Optimization

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Benchmark on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/benchmark-arm64.yml/badge.svg)
![Quantize on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/quantize-arm64.yml/badge.svg)
![ExecuTorch on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/executorch-arm64.yml/badge.svg)

**Submission for the [Arm Create: AI Optimization Challenge 2026](https://arm-ai-optimization-challenge.devpost.com)**

## What I optimized (the Arm story)

I took a real, widely-used NLP model (DistilBERT, fine-tuned for sentiment analysis) and optimized it for Arm64 in two ways: **INT8 dynamic quantization**, and deployment through **ExecuTorch with the XNNPACK backend**, which uses Arm's KleidiAI kernels automatically on supported hardware. Every result below comes from real Arm64 and x86_64 hardware, no emulation, no mocked numbers (see [Reproducing these results](#reproducing-these-results)).

**Headline results, on real Arm64 hardware:**
- **INT8 quantization**: 48.3% smaller model, with 100% prediction agreement vs the original
- **ExecuTorch + XNNPACK/KleidiAI**: the biggest win, **1.6x faster than FP32** and **~2x faster than standard INT8 quantization**, just from using an Arm-optimized inference engine

## Full benchmark results

### Quantization: FP32 vs INT8, x86_64 vs Arm64

| Metric | FP32 / x86_64 | FP32 / Arm64 | INT8 / x86_64 | INT8 / Arm64 |
|---|---|---|---|---|
| Model size | 256.10 MB | 256.10 MB | 132.29 MB | 132.29 MB |
| Avg latency | 65.12 ms | 21.07 ms | 25.24 ms | 25.40 ms |
| Throughput | 15.36 req/s | 47.47 req/s | 39.62 req/s | 39.37 req/s |

📊 [View the comparison charts](#comparison-charts)

### Arm-specific acceleration: ExecuTorch + XNNPACK/KleidiAI (on Arm64)

| Method | Avg latency | Throughput |
|---|---|---|
| PyTorch FP32 | 21.07 ms | 47.47 req/s |
| PyTorch INT8 (dynamic quantization) | 25.40 ms | 39.37 req/s |
| **ExecuTorch + XNNPACK/KleidiAI (FP32)** | **12.98 ms** | **77.04 req/s** |

This is the clearest Arm-specific result in the project: simply running the same FP32 model through Arm's own optimized inference engine outperforms both plain PyTorch FP32 and standard INT8 quantization, without changing the model's weights at all.

## Accuracy check: does quantization break the model?

I compared predictions from the original FP32 model and the quantized INT8 model on 6 test sentences (mixed positive/negative, including ambiguous ones):

- **Agreement rate: 100% (6/6)**,  every prediction matched between FP32 and INT8, with confidence scores staying within a fraction of a percent of each other.

Full details and the script used are in [`optimize/check_accuracy.py`](optimize/check_accuracy.py) and [`results/raw/accuracy_check_x86_64.json`](results/raw/accuracy_check_x86_64.json).

## An honest finding worth highlighting

Before quantization, **Arm64 was ~3.1x faster than x86_64** on the same FP32 model. After INT8 quantization, that gap nearly disappeared — both architectures converge to roughly the same latency (~25 ms). A follow-up run with more statistical rigor (100 runs across 4 sentences of varying length, tracking standard deviation) confirmed this pattern holds and isn't a measurement fluke.

My read: PyTorch dispatches to different quantized backends depending on architecture — `fbgemm` on x86, `qnnpack` on Arm and `fbgemm` appears more aggressively optimized for INT8 on x86 in this PyTorch version. This is exactly why the ExecuTorch/XNNPACK result above matters: it shows that the *engine* running the model on Arm matters as much as the quantization technique itself.

## How the optimization works

1. Load the pretrained FP32 DistilBERT model from Hugging Face.
2. **Quantization path**: apply `torch.quantization.quantize_dynamic`, converting `Linear` layers to 8-bit integers, with the correct backend selected per architecture (`qnnpack` for Arm64, `fbgemm` for x86_64).
3. **ExecuTorch path**: export the model with `torch.export`, lower it through ExecuTorch's XNNPACK backend, and run it via the ExecuTorch runtime, this automatically uses Arm's KleidiAI kernels where available.
4. Benchmark model size, latency, and throughput identically across every configuration.
5. Verify the quantized model's predictions still agree with the original.

## Why real Arm64 hardware, not emulation

All Arm64 numbers were produced on **GitHub Actions' native `ubuntu-24.04-arm` hosted runners**, real Arm64 silicon, not QEMU emulation.

## Project structure

```
armory-optimize/
├── .github/workflows/ # CI pipelines that run everything on real Arm64 hardware
├── models/ # Model download script
├── optimize/ # Quantization + accuracy check scripts
├── benchmark/ # Benchmark harness (latency, throughput, size)
├── experimental/executorch/ # ExecuTorch + XNNPACK/KleidiAI export & benchmark
├── results/
│ ├── raw/ # Raw JSON results for every configuration
│ └── charts/ # Generated comparison charts
├── report/ # Chart generation script
├── requirements.txt
└── LICENSE
```

## Reproducing these results

You can re-run every benchmark yourself, either locally or via the included GitHub Actions workflows (recommended, since it runs on real Arm64 hardware for free with no cloud account needed):

```bash
pip install -r requirements.txt
python models/download_model.py
python benchmark/harness.py # baseline FP32 benchmark
python optimize/quantize.py # quantize + benchmark INT8
python optimize/check_accuracy.py # verify predictions still match
python report/generate_charts.py # regenerate the comparison charts
python experimental/executorch/export_executorch.py # ExecuTorch/XNNPACK export + benchmark
```

Or, from this repo's **Actions** tab, manually trigger:
- `Benchmark on Arm64` — FP32 baseline on a real Arm64 runner
- `Quantize on Arm64` — quantization + benchmark on a real Arm64 runner
- `ExecuTorch on Arm64` — ExecuTorch/XNNPACK export + benchmark on a real Arm64 runner

## Reuse this on your own model

`download_model.py` and `quantize.py` work on any Hugging Face sequence-classification model, not just DistilBERT:

```bash
python models/download_model.py --model bert-base-uncased --save-dir models/my_model
python optimize/quantize.py --model-dir models/my_model --label my_model_int8
```

## Limitations

- Benchmarks compare a GitHub Actions x86_64 runner against a GitHub Actions Arm64 runner. These are different underlying cloud instances, so some of the raw latency difference may reflect instance-level differences in addition to architecture, I call this out rather than overstating a pure "Arm vs x86" claim.
- The ExecuTorch path currently runs the FP32 model rather than a fully INT8-quantized model within ExecuTorch itself; combining both is a natural next step.
- Only dynamic quantization on Linear layers is applied for the PyTorch path; static quantization and ONNX export are natural next steps.

## Comparison Charts

![Model size comparison](results/charts/model_size_comparison.png)
![Latency comparison](results/charts/latency_comparison.png)
![Throughput comparison](results/charts/throughput_comparison.png)

## License

MIT — see [LICENSE](./LICENSE).