import os
import time
import json
import platform
import argparse
import statistics
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

NUM_WARMUP = 10
NUM_RUNS = 100

TEST_SENTENCES = [
    "This movie was absolutely fantastic, I loved every minute of it!",
    "Worst film I have ever seen, complete waste of time.",
    "The acting was great but the plot made no sense at all.",
    "A masterpiece of modern cinema, beautifully directed.",
]

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


def measure_latency(model, all_inputs):
    for i in range(NUM_WARMUP):
        _ = model(**all_inputs[i % len(all_inputs)])

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
    return avg_latency_ms, std_latency_ms, throughput


def quantize_model(model_dir, output_dir, label):
    print(f"Loading original FP32 model from {model_dir}...")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()

    print("Applying dynamic INT8 quantization...")
    quantized_model = torch.quantization.quantize_dynamic(
        model,
        {torch.nn.Linear},
        dtype=torch.qint8
    )
    quantized_model.eval()

    os.makedirs(output_dir, exist_ok=True)
    torch.save(quantized_model.state_dict(), f"{output_dir}/quantized_model.pt")
    tokenizer.save_pretrained(output_dir)

    original_size = get_model_size_mb(model_dir)
    quantized_size = os.path.getsize(f"{output_dir}/quantized_model.pt") / (1024 * 1024)

    print(f"\n--- Quantization Results ---")
    print(f"Original size: {original_size:.2f} MB")
    print(f"Quantized size: {quantized_size:.2f} MB")
    print(f"Size reduction: {(1 - quantized_size / original_size) * 100:.1f}%")

    print(f"\nMeasuring speed ({NUM_RUNS} runs across {len(TEST_SENTENCES)} sentences)...")
    all_inputs = [tokenizer(s, return_tensors="pt") for s in TEST_SENTENCES]
    avg_latency_ms, std_latency_ms, throughput = measure_latency(quantized_model, all_inputs)

    print(f"Avg latency: {avg_latency_ms:.2f} ms (std: {std_latency_ms:.2f} ms)")
    print(f"Throughput: {throughput:.2f} requests/sec")

    results = {
        "model_size_mb": quantized_size,
        "avg_latency_ms": avg_latency_ms,
        "std_latency_ms": std_latency_ms,
        "throughput_rps": throughput,
        "num_runs": NUM_RUNS,
        "num_test_sentences": len(TEST_SENTENCES),
    }

    arch = platform.machine()
    os.makedirs("results/raw", exist_ok=True)
    output_path = f"results/raw/{label}_{arch}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_path}")

    return quantized_model, tokenizer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Apply dynamic INT8 quantization to any Hugging Face model directory and benchmark it."
    )
    parser.add_argument("--model-dir", default="models/original")
    parser.add_argument("--output-dir", default="models/quantized")
    parser.add_argument("--label", default="quantized_int8")
    args = parser.parse_args()

    quantize_model(args.model_dir, args.output_dir, args.label)
