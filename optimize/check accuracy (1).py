import os
import json
import platform
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

ORIGINAL_MODEL_DIR = "models/original"

if platform.machine() in ("aarch64", "arm64"):
    torch.backends.quantized.engine = "qnnpack"
else:
    torch.backends.quantized.engine = "fbgemm"

TEST_SENTENCES = [
    "This movie was absolutely fantastic, I loved every minute of it!",
    "Worst film I have ever seen, complete waste of time.",
    "The acting was great but the plot made no sense at all.",
    "I would definitely recommend this to all my friends.",
    "Terribly boring and way too long, I almost fell asleep.",
    "A masterpiece of modern cinema, beautifully directed.",
]

LABELS = {0: "NEGATIVE", 1: "POSITIVE"}


def get_prediction(model, tokenizer, sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probs, dim=-1).item()
    confidence = probs[0][predicted_class].item()
    return LABELS[predicted_class], confidence


def check_accuracy():
    print("Loading original FP32 model...")
    tokenizer = AutoTokenizer.from_pretrained(ORIGINAL_MODEL_DIR)
    original_model = AutoModelForSequenceClassification.from_pretrained(ORIGINAL_MODEL_DIR)
    original_model.eval()

    print("Creating quantized INT8 model...")
    quantized_model = torch.quantization.quantize_dynamic(
        original_model,
        {torch.nn.Linear},
        dtype=torch.qint8
    )
    quantized_model.eval()

    print("\nComparing predictions on test sentences...\n")
    results = []
    agreements = 0

    for sentence in TEST_SENTENCES:
        orig_label, orig_conf = get_prediction(original_model, tokenizer, sentence)
        quant_label, quant_conf = get_prediction(quantized_model, tokenizer, sentence)

        match = orig_label == quant_label
        if match:
            agreements += 1

        print(f"Sentence: {sentence}")
        print(f"  FP32 : {orig_label} ({orig_conf:.3f})")
        print(f"  INT8 : {quant_label} ({quant_conf:.3f})")
        print(f"  Match: {'YES' if match else 'NO'}\n")

        results.append({
            "sentence": sentence,
            "fp32_label": orig_label,
            "fp32_confidence": orig_conf,
            "int8_label": quant_label,
            "int8_confidence": quant_conf,
            "match": match,
        })

    agreement_rate = (agreements / len(TEST_SENTENCES)) * 100
    print(f"--- Summary ---")
    print(f"Agreement rate: {agreement_rate:.1f}% ({agreements}/{len(TEST_SENTENCES)})")

    arch = platform.machine()
    os.makedirs("results/raw", exist_ok=True)
    output_path = f"results/raw/accuracy_check_{arch}.json"

    with open(output_path, "w") as f:
        json.dump({
            "agreement_rate_pct": agreement_rate,
            "num_sentences": len(TEST_SENTENCES),
            "details": results,
        }, f, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    check_accuracy()
