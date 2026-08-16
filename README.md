# Armory
Powered by a real Arm-optimized NLP pipeline.


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Benchmark on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/benchmark-arm64.yml/badge.svg)
![Quantize on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/quantize-arm64.yml/badge.svg)
![ExecuTorch on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/executorch-arm64.yml/badge.svg)

---

## What is this?

A slightly unhinged web museum full of useless facts, with a real Arm64 optimization project underneath.

You can browse weird exhibits, collect badges, submit your own facts, and check the **Arm Performance** page for the actual benchmark results.

Behind the playful museum is a real NLP optimization experiment using DistilBERT for sentiment analysis.

---

## The Arm Optimization

I used **DistilBERT**, fine-tuned for sentiment analysis, and evaluated two optimization paths:

- **INT8 dynamic quantization**
- **ExecuTorch + XNNPACK**

The goal was to measure how the same AI workload behaves on **Arm64 vs x86_64**, before and after optimization.

Every benchmark was run on real hardware **no emulation**.

### Results (Real Hardware)

| Metric       | FP32/x86_64 | FP32/Arm64 | INT8/x86_64 | INT8/Arm64 |
|--------------|-------------|------------|-------------|------------|
| Model size   | 256.10 MB   | 256.10 MB  | 132.29 MB   | 132.29 MB  |
| Avg latency  | 65.12 ms    | 21.07 ms   | 25.24 ms    | 25.40 ms   |
| Throughput   | 15.36 req/s | 47.47 req/s| 39.62 req/s | 39.37 req/s|

### The interesting part

Arm64 was approximately **3.1× faster than x86_64 at FP32**.

After INT8 quantization, however, the gap almost completely disappeared:

- x86_64: **25.24 ms**
- Arm64: **25.40 ms**

Both architectures ended up around **25 ms latency**.

INT8 also reduced the model size from **256.10 MB → 132.29 MB**, a reduction of approximately **48%**.

This was not the result I expected.

Instead of hiding it, I kept it, because it demonstrates something more useful:

> **Arm optimization is something to measure, not assume.**

### ExecuTorch + XNNPACK

The ExecuTorch + XNNPACK path was also substantially faster than the baseline paths in our measurements.

The measured result was approximately:

- **1.6× faster than the FP32 baseline**
- **2× faster than the standard INT8 path**

The current ExecuTorch path runs FP32; the internal PT2E INT8 quantization path was not included because of dependency and version conflicts.
---

## How the optimization works

1. Load the pretrained FP32 DistilBERT model.
2. Apply dynamic INT8 quantization (`qnnpack` on Arm, `fbgemm` on x86).
3. Export the model through ExecuTorch’s XNNPACK backend.
4. Benchmark size, latency, and throughput on real hardware.
5. Verify that predictions still match the original model (100% agreement).

---

## Running the original optimization pipeline

```bash
git clone https://github.com/wyyyrdx/Armory-Optimize.git
cd Armory-Optimize
pip install -r requirements.txt

python models/download_model.py
python benchmark/harness.py
python optimize/quantize.py
python optimize/check_accuracy.py
python report/generate_charts.py
```

For the ExecuTorch path:
```bash
pip install executorch
pip uninstall -y torchvision
python experimental/executorch/export_executorch.py
```

You can also trigger the workflows directly from the **Actions** tab on GitHub (runs on real Arm64 runners).

---

## Running the museum

You need two terminals.

**First time only:**
```powershell
# Backend
cd path\to\museum
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd path\to\museum\frontend
npm install
```

**Every time:**

**Terminal 1 – Backend**
```powershell
cd path\to\museum
.\.venv\Scripts\Activate.ps1
.\run_backend.ps1
```

**Terminal 2 – Frontend**
```powershell
cd path\to\museum\frontend
npm run dev
```

Then open: [http://localhost:5173](http://localhost:5173)

---

## Comparison Charts

![Model size comparison](results/charts/model_size_comparison.png)
![Latency comparison](results/charts/latency_comparison.png)
![Throughput comparison](results/charts/throughput_comparison.png)

---

## Limitations

- Benchmarks compare different cloud instances (GitHub Actions x86 vs Arm), so some differences may not be purely architectural.
- The ExecuTorch path currently runs FP32 (internal PT2E quantization had version conflicts and was skipped).
- Only dynamic quantization on Linear layers is used in the PyTorch path.

---

## License

MIT - see [LICENSE](./LICENSE).
