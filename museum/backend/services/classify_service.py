from ml.classifier import classify_fact, Result


def classify(text: str) -> Result:
    return classify_fact(text)