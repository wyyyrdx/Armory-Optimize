import json
import os
import matplotlib.pyplot as plt

RESULTS_DIR = "results/raw"
CHARTS_DIR = "results/charts"

FILES = {
    "FP32 / x86_64": "baseline_fp32_x86_64.json",
    "FP32 / Arm64": "baseline_fp32_aarch64.json",
    "INT8 / x86_64": "quantized_int8_x86_64.json",
    "INT8 / Arm64": "quantized_int8_aarch64.json",
}

COLORS = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]


def load_all_results():
    data = {}
    for label, filename in FILES.items():
        path = os.path.join(RESULTS_DIR, filename)
        with open(path) as f:
            data[label] = json.load(f)
    return data


def make_bar_chart(data, metric_key, title, ylabel, filename):
    labels = list(data.keys())
    values = [data[label][metric_key] for label in labels]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, values, color=COLORS)
    plt.title(title, fontsize=14, fontweight="bold")
    plt.ylabel(ylabel)
    plt.xticks(rotation=15)

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()
    os.makedirs(CHARTS_DIR, exist_ok=True)
    output_path = os.path.join(CHARTS_DIR, filename)
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved {output_path}")


def generate_charts():
    data = load_all_results()

    make_bar_chart(
        data, "model_size_mb",
        "Model Size: FP32 vs INT8 (x86_64 vs Arm64)",
        "Size (MB)",
        "model_size_comparison.png",
    )

    make_bar_chart(
        data, "avg_latency_ms",
        "Average Latency: FP32 vs INT8 (x86_64 vs Arm64)",
        "Latency (ms) — lower is better",
        "latency_comparison.png",
    )

    make_bar_chart(
        data, "throughput_rps",
        "Throughput: FP32 vs INT8 (x86_64 vs Arm64)",
        "Requests / sec — higher is better",
        "throughput_comparison.png",
    )

    print("\nAll charts generated in results/charts/")


if __name__ == "__main__":
    generate_charts()
