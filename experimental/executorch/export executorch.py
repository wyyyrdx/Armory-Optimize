import time
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from executorch.exir import to_edge
from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner

MODEL_DIR = "models/original"
TEST_SENTENCE = "This movie was absolutely fantastic, I loved every minute of it!"
NUM_WARMUP = 5
NUM_RUNS = 30


class DistilBertWrapper(torch.nn.Module):
    """Wraps the HF model so it returns a plain tensor (logits) instead of a ModelOutput object."""
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask):
        return self.model(input_ids=input_ids, attention_mask=attention_mask).logits


print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
base_model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
base_model.eval()

wrapped_model = DistilBertWrapper(base_model).eval()

inputs = tokenizer(TEST_SENTENCE, return_tensors="pt")
example_inputs = (inputs["input_ids"], inputs["attention_mask"])

print("Exporting model with torch.export (FP32, no internal quantization)...")
exported_program = torch.export.export(wrapped_model, example_inputs)

print("Lowering to ExecuTorch with XNNPACK backend...")
edge_program = to_edge(exported_program)
edge_program = edge_program.to_backend(XnnpackPartitioner())
et_program = edge_program.to_executorch()

with open("model.pte", "wb") as f:
    f.write(et_program.buffer)

print("\n✅ Exported model.pte successfully")

print("\nLoading .pte for benchmarking...")
from executorch.extension.pybindings.portable_lib import _load_for_executorch

et_model = _load_for_executorch("model.pte")
et_inputs = [inputs["input_ids"], inputs["attention_mask"]]

print(f"Warming up ({NUM_WARMUP} runs)...")
for _ in range(NUM_WARMUP):
    _ = et_model.forward(et_inputs)

print(f"Measuring latency ({NUM_RUNS} runs)...")
latencies = []
for _ in range(NUM_RUNS):
    start = time.perf_counter()
    _ = et_model.forward(et_inputs)
    end = time.perf_counter()
    latencies.append((end - start) * 1000)

avg_latency_ms = sum(latencies) / len(latencies)
throughput = 1000 / avg_latency_ms

print(f"\n--- ExecuTorch (XNNPACK backend, FP32) Results ---")
print(f"Avg latency: {avg_latency_ms:.2f} ms")
print(f"Throughput: {throughput:.2f} requests/sec")
