# redactgate

Take personal data out of text before it goes to an AI model, then put it
back into the answer. Runs locally on CPU; nothing is sent anywhere.

**The business problem.** Teams want to paste customer emails, contracts and
support tickets into ChatGPT or Claude, and their privacy policy (or GDPR, or
a client contract) says they can't send customer personal data to a third
party. redactgate swaps each name, email, card number and so on for a
placeholder (`[PERSON_1]`, `[CARD_1]`), so the model still sees who did what.
When the answer comes back, it swaps the real values back in.

![redactgate page](docs/screenshot.png)

## What it finds

- **Patterns with checks:** emails, phone numbers, card numbers (Luhn check),
  IBANs (mod-97 check), US routing numbers (ABA checksum, or after the words
  "routing number"), SSNs, IPv4/IPv6, SWIFT/BIC codes, CVVs, passwords and
  API keys, passport/licence/customer/employee IDs after their label, dates of
  birth, coordinates, street addresses with city/state/postcode.
- **Names and places:** `dslim/bert-base-NER` (MIT licence, about 400 MB,
  CPU). Spans are widened to whole words. A place is only masked when it is
  part of a street address; a city or country on its own is left in.
- **Repeats:** once a value is found, every other copy of it in the document
  is masked with the same placeholder.

Dates, times, amounts and company names are left in by design. Company names
are detected (`ORG`) but not masked by default.

## How well it works

Measured on [Gretel's synthetic_pii_finance_multilingual](https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual)
(Apache-2.0): synthetic financial documents (loan forms, SWIFT messages,
contracts, emails) with labelled personal data. English only. Rules were tuned
on the first 500 documents of the train split; the 2,891-document test split
was run once at the end.

A labelled value counts as masked when at least 80% of its characters are
covered.

| split | method | values masked | characters masked | documents with any leak | precision (lower bound) |
|---|---|---|---|---|---|
| dev (500) | patterns + model | 79.3% (1118/1409) | 85.6% | 32.2% | 66.6% |
| test (2,891) | patterns only | 55.0% (4516/8205) | 63.3% | 58.0% | 65.1% |
| test (2,891) | **patterns + model** | **76.0% (6239/8205)** | **83.0%** | **37.0%** | 65.6% |
| test (2,891) | Microsoft Presidio 2.2 (analyzer 3.8, default config, spaCy `en_core_web_lg`) | 52.7% (4322/8205) | 62.0% | 64.4% | 29.1% |

Per type on test (patterns + model): names 74%, street addresses 82%,
emails 93%, phone numbers 86%, card numbers 93%, IBANs 97%, SWIFT 100%, IPs
98-100%; weakest are passwords (43%), API keys (39%), customer and employee
IDs (38-41%), and routing numbers (43%). Full table: `docs/results-test-model.md`.
Speed: 152 ms per document on CPU with the model, 1 ms without.

**Against Presidio.** Out of the box, Presidio masks about as many names (72%
vs 74%) but far fewer street addresses (12% vs 82%), SWIFT codes, passwords
and bank account numbers. Its precision lower bound is lower because by
default it also masks every date, time, city and country. It is faster
(27 ms vs 152 ms per document). This compares defaults: Presidio is built to
take custom recognizers, and adding address and banking ones would close much
of the gap. Run: `python scripts/evaluate.py --split test --detector presidio`
from a venv with `presidio-analyzer` and `en_core_web_lg`.

What the numbers mean:

- **It is not safe as the only control.** 37% of test documents still had at
  least one labelled value left in. Use it to cut how much personal data
  leaves, with a person reading the redacted text before it is sent (the
  page shows it for that reason), not as a guarantee.
- **Precision is a lower bound.** The dataset's labels are incomplete: many
  names, emails and addresses in the documents are not labelled. A sample of
  150 dev documents showed most "false positives" were real emails and names
  the labels missed; the rest were mostly short fragments and message-format
  syntax, which I then filtered.
- **Synthetic data.** Card and routing numbers in the dataset often fail
  their checksums, so the tool also accepts them when a label word ("card",
  "routing number") is next to them. Real documents may behave differently.
- **One methodology slip:** the very first patterns-only run (before the dev
  split existed) was on the test split. All tuning after that used dev only.
- A shortened name ("Mr. Quesada" after "Jerónimo E. Quesada") gets its own
  placeholder, so the model does not know they are the same person.

## Run it

```bash
uv venv && uv pip install torch transformers fastapi uvicorn jinja2 python-multipart pyarrow pytest httpx
pytest -q                                  # 7 tests (patterns only; no model download)
uvicorn redactgate.app:app --port 8840     # page at http://localhost:8840
```

JSON API, to put in front of any model:

```bash
curl -s localhost:8840/api/redact -H 'content-type: application/json' -d '{"text": "Email ana@lima.pt"}'
# {"redacted": "Email [EMAIL_1]", "mapping": {"[EMAIL_1]": "ana@lima.pt"}, ...}
curl -s localhost:8840/api/restore -H 'content-type: application/json' \
  -d '{"text": "Wrote to [EMAIL_1]", "mapping": {"[EMAIL_1]": "ana@lima.pt"}}'
```

Reproduce the measurements:

```bash
mkdir -p data/raw
curl -L -o data/raw/en_train.parquet https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual/resolve/main/data/English_train-00000-of-00001.parquet
curl -L -o data/raw/en_test.parquet  https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual/resolve/main/data/English_test-00000-of-00001.parquet
python scripts/evaluate.py --split dev          # first 500 train documents
python scripts/evaluate.py --split test         # run once
```

## Not done

- No direct call to Claude or another model; it's copy and paste, or the
  JSON API. (No API key was available when this was built.)
- English only. The dataset has Dutch, French, German, Italian, Spanish and
  Swedish splits that were not tried.
- No PDF or Word input; text only.
- Presidio with custom recognizers was not tried; only its defaults.
