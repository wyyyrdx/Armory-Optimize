# Armory: Arm64 vs x86 AI Inference Optimization

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Benchmark on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/benchmark-arm64.yml/badge.svg)
![Quantize on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/quantize-arm64.yml/badge.svg)
![ExecuTorch on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/executorch-arm64.yml/badge.svg)

**Submission for the [Arm Create: AI Optimization Challenge 2026](https://arm-ai-optimization-challenge.devpost.com)**

## What I optimized (the Arm story)

I took a real, widely-used NLP model (DistilBERT, fine-tuned for sentiment analysis) and optimized it for Arm64 two ways: **INT8 dynamic quantization**, and deployment through **ExecuTorch with the XNNPACK backend**, which uses Arm's KleidiAI kernels automatically on supported hardware. Every result below comes from real Arm64 and x86_64 hardware, no emulation, no mocked numbers. The ExecuTorch path came out **1.6x faster than FP32 and ~2x faster than standard INT8 quantization**, just from using an Arm-optimized inference engine.

---

## Run this yourself (tested, no manual setup)

Every command below is exactly what CI runs on a real Arm64 GitHub Actions runner, copy-paste them in order:

```bash
git clone https://github.com/wyyyrdx/Armory-Optimize.git
cd Armory-Optimize
pip install -r requirements.txt
python models/download_model.py
python benchmark/harness.py # baseline FP32
python optimize/quantize.py # INT8 quantization
python optimize/check_accuracy.py # verify predictions still match
python report/generate_charts.py # regenerate charts

# ExecuTorch path (separate install, larger download):
pip install executorch
python experimental/executorch/export_executorch.py
```

No account, no API key, no paid cloud instance required. Or, from this repo's **Actions** tab, run any of `Benchmark on Arm64`, `Quantize on Arm64`, or `ExecuTorch on Arm64` directly on real Arm64 hardware with one click, no local setup at all.

---

## Results

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

### Accuracy: does quantization break the model?

I compared predictions from the original FP32 model and the quantized INT8 model on 6 test sentences. **Agreement rate: 100% (6/6)** every prediction matched, with confidence scores within a fraction of a percent. Details in [`optimize/check_accuracy.py`](optimize/check_accuracy.py) and [`results/raw/accuracy_check_x86_64.json`](results/raw/accuracy_check_x86_64.json).

---

## An honest finding worth highlighting

Before quantization, Arm64 was ~3.1x faster than x86_64 on the same FP32 model. After INT8 quantization, that gap nearly disappeared, both architectures converge to roughly the same latency (~25 ms). A follow-up run with more statistical rigor (100 runs across 4 sentences of varying length, tracking standard deviation) confirmed this pattern holds and isn't a measurement fluke.

My read: PyTorch dispatches to different quantized backends depending on architecture, `fbgemm` on x86, `qnnpack` on Arm and `fbgemm` appears more aggressively optimized for INT8 on x86 in this PyTorch version. This is exactly why the ExecuTorch/XNNPACK result matters: the *engine* running the model on Arm matters as much as the quantization technique itself.

## How the optimization works

1. Load the pretrained FP32 DistilBERT model from Hugging Face.
2. **Quantization path**: apply `torch.quantization.quantize_dynamic`, converting `Linear` layers to 8-bit integers, with the correct backend selected per architecture (`qnnpack` for Arm64, `fbgemm` for x86_64).
3. **ExecuTorch path**: export the model with `torch.export`, lower it through ExecuTorch's XNNPACK backend, and run it via the ExecuTorch runtime, this automatically uses Arm's KleidiAI kernels where available.
4. Benchmark model size, latency, and throughput identically across every configuration, and verify the quantized model's predictions still agree with the original.

All Arm64 numbers were produced on **GitHub Actions' native `ubuntu-24.04-arm` hosted runners** real Arm64 silicon, not emulation.

## Reuse this on your own model

`download_model.py` and `quantize.py` work on any Hugging Face sequence-classification model, not just DistilBERT:

```bash
python models/download_model.py --model bert-base-uncased --save-dir models/my_model
python optimize/quantize.py --model-dir models/my_model --label my_model_int8
```

## Comparison Charts

![Model size comparison](results/charts/model_size_comparison.png)
![Latency comparison](results/charts/latency_comparison.png)
![Throughput comparison](results/charts/throughput_comparison.png)

## Limitations

- Benchmarks compare a GitHub Actions x86_64 runner against a GitHub Actions Arm64 runner, different underlying cloud instances, so some of the raw latency difference may reflect instance-level differences in addition to architecture.
- The ExecuTorch path currently runs the FP32 model rather than a fully INT8-quantized model within ExecuTorch itself; combining both is a natural next step.
- Only dynamic quantization on Linear layers is applied for the PyTorch path; static quantization and ONNX export are natural next steps.

## License

MIT — see [LICENSE](./LICENSE).