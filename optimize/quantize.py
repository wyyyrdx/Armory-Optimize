import os
import time
import json
import platform
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

ORIGINAL_MODEL_DIR = "models/original"
QUANTIZED_MODEL_DIR = "models/quantized"
NUM_WARMUP = 5
NUM_RUNS = 50
TEST_SENTENCE = "This movie was absolutely fantastic, I loved every minute of it!"


if platform.machine() in ("aarch64", "arm64"):
    torch.backends.quantized.engine = "qnnpack"
else:
    torch.backends.quantized.engine = "fbgemm"


def get_model_size_mb(path):
    total_bytes = 0
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        total_bytes += os.path.getsize(filepath)
    return total_bytes / (1024 * 1024)


def measure_latency(model, inputs):
    for _ in range(NUM_WARMUP):
        _ = model(**inputs)

    latencies = []
    for _ in range(NUM_RUNS):
        start = time.perf_counter()
        _ = model(**inputs)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)

    avg_latency_ms = sum(latencies) / len(latencies)
    throughput = 1000 / avg_latency_ms
    return avg_latency_ms, throughput


def quantize_model():
    print("Loading original FP32 model...")
    tokenizer = AutoTokenizer.from_pretrained(ORIGINAL_MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(ORIGINAL_MODEL_DIR)
    model.eval()

    print("Applying dynamic INT8 quantization...")
    quantized_model = torch.quantization.quantize_dynamic(
        model,
        {torch.nn.Linear},
        dtype=torch.qint8
    )
    quantized_model.eval()

    os.makedirs(QUANTIZED_MODEL_DIR, exist_ok=True)
    torch.save(quantized_model.state_dict(), f"{QUANTIZED_MODEL_DIR}/quantized_model.pt")
    tokenizer.save_pretrained(QUANTIZED_MODEL_DIR)

    original_size = get_model_size_mb(ORIGINAL_MODEL_DIR)
    quantized_size = os.path.getsize(f"{QUANTIZED_MODEL_DIR}/quantized_model.pt") / (1024 * 1024)

    print(f"\n--- Quantization Results ---")
    print(f"Original size: {original_size:.2f} MB")
    print(f"Quantized size: {quantized_size:.2f} MB")
    print(f"Size reduction: {(1 - quantized_size / original_size) * 100:.1f}%")

    print("\nMeasuring speed of quantized model...")
    inputs = tokenizer(TEST_SENTENCE, return_tensors="pt")
    avg_latency_ms, throughput = measure_latency(quantized_model, inputs)

    print(f"Avg latency: {avg_latency_ms:.2f} ms")
    print(f"Throughput: {throughput:.2f} requests/sec")

    results = {
        "model_size_mb": quantized_size,
        "avg_latency_ms": avg_latency_ms,
        "throughput_rps": throughput,
    }

    arch = platform.machine()
    os.makedirs("results/raw", exist_ok=True)
    output_path = f"results/raw/quantized_int8_{arch}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_path}")

    return quantized_model, tokenizer


if __name__ == "__main__":
    quantize_model()
