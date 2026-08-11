# Museum of Useless Knowledge
**Facts you absolutely did not need to know.**  
Powered by a real Arm-optimized NLP pipeline.


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Benchmark on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/benchmark-arm64.yml/badge.svg)
![Quantize on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/quantize-arm64.yml/badge.svg)
![ExecuTorch on Arm64](https://github.com/wyyyrdx/Armory-Optimize/actions/workflows/executorch-arm64.yml/badge.svg)

---

## What is this?

A slightly unhinged web museum full of useless facts, with a real Arm64 optimization project underneath.

You can browse weird exhibits, collect badges, submit your own facts, and check the **Arm Performance** page for the actual benchmark numbers.

---

## What I optimized (the Arm story)

I took a real NLP model (DistilBERT, fine-tuned for sentiment analysis) and optimized it for Arm64 in two ways:

1. **INT8 dynamic quantization**
2. **ExecuTorch + XNNPACK** (uses Arm’s KleidiAI kernels automatically)

Every result comes from real Arm64 and x86_64 hardware — no emulation.

### Results (Real Hardware)

| Metric       | FP32/x86_64 | FP32/Arm64 | INT8/x86_64 | INT8/Arm64 |
|--------------|-------------|------------|-------------|------------|
| Model size   | 256.10 MB   | 256.10 MB  | 132.29 MB   | 132.29 MB  |
| Avg latency  | 65.12 ms    | 21.07 ms   | 25.24 ms    | 25.40 ms   |
| Throughput   | 15.36 req/s | 47.47 req/s| 39.62 req/s | 39.37 req/s|

**Honest finding:**  
Arm64 was ~3.1× faster than x86 at FP32, but after INT8 quantization the gap almost disappeared. Both architectures ended up around ~25 ms latency.

The ExecuTorch path was ~1.6× faster than FP32 and about 2× faster than standard INT8 quantization.

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

MIT — see [LICENSE](./LICENSE).
