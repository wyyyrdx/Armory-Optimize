import time
import os
import json
import platform
import statistics
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = "models/original"
NUM_WARMUP = 10
NUM_RUNS = 100

TEST_SENTENCES = [
    "This movie was absolutely fantastic, I loved every minute of it!",
    "Worst film I have ever seen, complete waste of time.",
    "The acting was great but the plot made no sense at all.",
    "A masterpiece of modern cinema, beautifully directed.",
]


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

    all_inputs = [tokenizer(s, return_tensors="pt") for s in TEST_SENTENCES]

    print(f"Warming up ({NUM_WARMUP} runs)...")
    for i in range(NUM_WARMUP):
        _ = model(**all_inputs[i % len(all_inputs)])

    print(f"Measuring latency ({NUM_RUNS} runs across {len(TEST_SENTENCES)} sentences)...")
    latencies = []
    for i in range(NUM_RUNS):
        inputs = all_inputs[i % len(all_inputs)]
        start = time.perf_counter()
        _ = model(**inputs)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)

    avg_latency_ms = statistics.mean(latencies)
    std_latency_ms = statistics.stdev(latencies)
    throughput = 1000 / avg_latency_ms

    model_size_mb = get_model_size_mb(MODEL_DIR)

    print("\n--- Results ---")
    print(f"Model size: {model_size_mb:.2f} MB")
    print(f"Avg latency: {avg_latency_ms:.2f} ms (std: {std_latency_ms:.2f} ms)")
    print(f"Throughput: {throughput:.2f} requests/sec")

    results = {
        "model_size_mb": model_size_mb,
        "avg_latency_ms": avg_latency_ms,
        "std_latency_ms": std_latency_ms,
        "throughput_rps": throughput,
        "num_runs": NUM_RUNS,
        "num_test_sentences": len(TEST_SENTENCES),
    }

    arch = platform.machine()
    os.makedirs("results/raw", exist_ok=True)
    output_path = f"results/raw/baseline_fp32_{arch}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_path}")

    return results


if __name__ == "__main__":
    run_benchmark()
