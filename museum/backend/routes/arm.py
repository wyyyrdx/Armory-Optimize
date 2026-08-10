from fastapi import APIRouter

router = APIRouter()


@router.get("/arm/benchmarks")
def arm_benchmarks():
    return {
        "note": "Published results from real Arm64 GitHub Actions runners (Armory project).",
        "model": "DistilBERT (sequence classification)",
        "results": [
            {
                "backend": "PyTorch FP32",
                "arch": "Arm64",
                "latency_ms": 21.07,
                "throughput_rps": 47.47,
                "model_size_mb": 256.10,
            },
            {
                "backend": "PyTorch INT8 (dynamic quantization)",
                "arch": "Arm64",
                "latency_ms": 25.40,
                "throughput_rps": 39.37,
                "model_size_mb": 132.29,
            },
            {
                "backend": "ExecuTorch + XNNPACK/KleidiAI (FP32)",
                "arch": "Arm64",
                "latency_ms": 12.98,
                "throughput_rps": 77.04,
                "model_size_mb": None,
                "highlight": True,
            },
            {
                "backend": "PyTorch FP32",
                "arch": "x86_64",
                "latency_ms": 65.12,
                "throughput_rps": 15.36,
                "model_size_mb": 256.10,
            },
            {
                "backend": "PyTorch INT8 (dynamic quantization)",
                "arch": "x86_64",
                "latency_ms": 25.24,
                "throughput_rps": 39.62,
                "model_size_mb": 132.29,
            },
        ],
        "honest_finding": (
            "Before quantization, Arm64 was ~3.1× faster than x86_64 on FP32. "
            "After INT8 the gap nearly disappeared. ExecuTorch + XNNPACK/KleidiAI "
            "is the clearest Arm-specific win."
        ),
    }