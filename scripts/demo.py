"""Round trip on one made-up customer email: redact, (pretend to) ask a model,
restore the answer.

  python scripts/demo.py

No model API is called: the "model answer" below is written by hand, the way
a model replies when it only sees placeholders. The NER model runs locally
(downloaded once from Hugging Face, about 1 GB).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from redactgate.redact import redact, restore  # noqa: E402

EMAIL = """\
From: Daniel Okafor <d.okafor@example.com>
Subject: Refund for double charge

Hi, I was charged twice for my March invoice on card 4111 1111 1111 1111.
Please refund the second payment to my account GB82 WEST 1234 5698 7654 32.
My address is 742 Maple Avenue, Springfield, IL 62704 and you can reach me
on +1 (217) 555-0148. Thanks, Daniel Okafor"""

# What a model might write back, seeing only the redacted email.
MODEL_ANSWER = """\
Dear [PERSON_1],

Thank you for contacting us. We have confirmed the duplicate charge on card
[CARD_1] and refunded the second payment to [IBAN_1]. You will receive a
confirmation at [EMAIL_1]; if anything is unclear we will call you on
[PHONE_1]."""


def main():
    redacted, mapping = redact(EMAIL)
    print("== 1. Original email (stays on your machine)\n")
    print(EMAIL)
    print("\n== 2. What is sent to the model\n")
    print(redacted)
    print("\n== 3. Mapping (stays on your machine)\n")
    for placeholder, value in mapping.items():
        print(f"{placeholder:14} {value}")
    print("\n== 4. Model answer (made up for the demo)\n")
    print(MODEL_ANSWER)
    print("\n== 5. Answer with the real values restored\n")
    print(restore(MODEL_ANSWER, mapping))


if __name__ == "__main__":
    main()
