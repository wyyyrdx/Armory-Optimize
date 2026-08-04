import time
import os
import json
import platform
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = "models/original"
NUM_WARMUP = 5
NUM_RUNS = 50
TEST_SENTENCE = "This movie was absolutely fantastic, I loved every minute of it!"


def get_model_size_mb(path):
    total_bytes = 0
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        total_bytes += os.path.getsize(filepath)
    return total_bytes / (1024 * 1024)


def run_benchmark():
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()
    inputs = tokenizer(TEST_SENTENCE, return_tensors="pt")

    print(f"Warming up ({NUM_WARMUP} runs)...")
    for _ in range(NUM_WARMUP):
        _ = model(**inputs)

    print(f"Measuring latency ({NUM_RUNS} runs)...")
    latencies = []
    for _ in range(NUM_RUNS):
        start = time.perf_counter()
        _ = model(**inputs)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)

    avg_latency_ms = sum(latencies) / len(latencies)
    throughput = 1000 / avg_latency_ms

    model_size_mb = get_model_size_mb(MODEL_DIR)

    print("\n--- Results ---")
    print(f"Model size: {model_size_mb:.2f} MB")
    print(f"Avg latency: {avg_latency_ms:.2f} ms")
    print(f"Throughput: {throughput:.2f} requests/sec")

    return {
        "model_size_mb": model_size_mb,
        "avg_latency_ms": avg_latency_ms,
        "throughput_rps": throughput,
    }


if __name__ == "__main__":
    results = run_benchmark()

    os.makedirs("results/raw", exist_ok=True)
    arch = platform.machine()
    output_path = f"results/raw/baseline_fp32_{arch}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved to {output_path}")
