from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import argparse

DEFAULT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
DEFAULT_SAVE_DIR = "models/original"


def download_model(model_name, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    print(f"Downloading {model_name} ...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    tokenizer.save_pretrained(save_dir)
    model.save_pretrained(save_dir)

    print(f"Saved to {save_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download any Hugging Face sequence classification model for use with quantize.py"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL_NAME,
        help=f"Hugging Face model name (default: {DEFAULT_MODEL_NAME})"
    )
    parser.add_argument(
        "--save-dir", default=DEFAULT_SAVE_DIR,
        help=f"Where to save the downloaded model (default: {DEFAULT_SAVE_DIR})"
    )
    args = parser.parse_args()

    download_model(args.model, args.save_dir)
