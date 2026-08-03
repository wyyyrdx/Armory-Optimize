from transformers import AutoTokenizer , AutoModelForSequenceClassification
import os

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
SAVE_DIR = "models/original"

os.makedirs (SAVE_DIR , exist_ok= True)

print (f"Downloading {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained (MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained (MODEL_NAME)

tokenizer.save_pretrained (SAVE_DIR)
model.save_pretrained (SAVE_DIR)

print (f"saved to {SAVE_DIR}")
