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
- **Names and places:** `Davlan/xlm-roberta-base-ner-hrl` (AFL-3.0, about
  1 GB, CPU; covers German, English, Spanish, French, Italian, Dutch,
  Portuguese and others) by default, or `dslim/bert-base-NER` (MIT, English
  only). Spans are widened to whole words. A place is only masked when it is
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
| test (2,891) | Microsoft Presidio analyzer 2.2.366, default config, spaCy 3.8 `en_core_web_lg` | 52.7% (4322/8205) | 62.0% | 64.4% | 29.1% |

Per type on test (patterns + model): names 74%, street addresses 82%,
emails 93%, phone numbers 86%, card numbers 93%, IBANs 97%, SWIFT 100%, IPs
98-100%; weakest are passwords (43%), API keys (39%), customer and employee
IDs (38-41%), and routing numbers (43%). Full table: `docs/results-test-model.md`.
Speed: 152 ms per document on CPU with the model, 1 ms without.

**Other languages.** EU businesses are the obvious buyers (GDPR), so the
same evaluation was run on the dataset's German, French, Spanish, Italian and
Dutch splits. Dev is the first 200 train documents per language; each test
split (about 450 documents) was run once. Additions for these languages:
street-name-first and street-suffix address forms ("Rue de la Paix",
"Schnellstraße 12, 45678 Berlin", "Åkervägen"), European phone formats,
"IBAN:"-keyed IBANs, date-of-birth and name labels in each language
("Geburtsdatum", "né(e) le", "Nom", "Herr", "Monsieur").

| language | dev, English setup | dev, multilingual model | dev, + European rules | **test** (values masked) | test, docs with any leak |
|---|---|---|---|---|---|
| German | 44.4% | 53.3% | 67.2% | **66.5%** (766/1152) | 44.6% |
| French | 37.3% | 50.8% | 68.2% | **68.5%** (886/1293) | 47.2% |
| Spanish | 45.9% | 56.7% | 66.5% | **71.8%** (971/1353) | 40.3% |
| Italian | 39.1% | 50.1% | 70.1% | **66.9%** (880/1315) | 47.1% |
| Dutch | 41.3% | 53.8% | 64.2% | **65.3%** (807/1236) | 46.5% |
| English | 79.3% | 83.0% | 84.0% | **81.8%** (6715/8205)* | 27.9% |

\* English test with the multilingual model is the second run on the
English test split (the first, with the English model, gave 76.0%). The
switch to the multilingual model was decided on dev (83.0% vs 79.3%) before
that run. Swedish was not tried: the model does not cover it.

Non-English recall is about 15 points below English: half of the documents
still leak at least one value. The precision lower bound stays between 62%
and 71%.

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
- **Precision is a lower bound, and the real figure is higher.** The labels
  are incomplete. I audited 100 random masks (from 300 English test
  documents) that touch no labelled value: 50 were real personal data the
  labels missed (names in chat transcripts, phone numbers, SSNs in CSV rows,
  account numbers), 50 were not (city/country names in company addresses,
  role words like "Lender", capitalised ordinary words, numbers in tables).
  Such masks are 24% of masked characters, so about 12% of masked characters
  are false positives: **estimated precision about 88%**. One annotator (me),
  100 items: treat it as a rough estimate. The audit is in
  `docs/precision-audit.json`. Afterwards, role words and a short list of
  ordinary words were filtered from the model's output (English dev: recall
  unchanged at 84.0%, lower bound 64.9% -> 65.8%).
- **Synthetic data.** Card and routing numbers in the dataset often fail
  their checksums, so the tool also accepts them when a label word ("card",
  "routing number") is next to them. Real documents may behave differently.
- **One methodology slip:** the very first patterns-only run (before the dev
  split existed) was on the test split. All tuning after that used dev only.
- A shortened name ("Mr. Quesada" after "Jerónimo E. Quesada") becomes
  `[PERSON_1_LAST]`, so the model can tell it is the same person as
  `[PERSON_1]`. Restore also accepts placeholders a model wrote without
  brackets. Without the model (patterns only), first names are often missed.

## Run it

```bash
uv venv && uv pip install torch transformers sentencepiece protobuf fastapi uvicorn jinja2 python-multipart pyarrow pdfplumber python-docx pytest httpx reportlab
pytest -q                                  # 11 tests (patterns only; no model download)
uvicorn redactgate.app:app --port 8840     # page at http://localhost:8840
```

JSON API, to put in front of any model:

```bash
curl -s localhost:8840/api/redact -H 'content-type: application/json' -d '{"text": "Email ana@lima.pt"}'
# {"redacted": "Email [EMAIL_1]", "mapping": {"[EMAIL_1]": "ana@lima.pt"}, ...}
curl -s localhost:8840/api/restore -H 'content-type: application/json' \
  -d '{"text": "Wrote to [EMAIL_1]", "mapping": {"[EMAIL_1]": "ana@lima.pt"}}'
```

Files: the page takes a .pdf (with a text layer; scans are refused, there is
no OCR), .docx (paragraphs and tables) or .txt upload, and so does
`POST /api/redact-file` (multipart, field `file`). Output is redacted text,
not a redacted PDF.

Reproduce the measurements:

```bash
mkdir -p data/raw
curl -L -o data/raw/en_train.parquet https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual/resolve/main/data/English_train-00000-of-00001.parquet
curl -L -o data/raw/en_test.parquet  https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual/resolve/main/data/English_test-00000-of-00001.parquet
python scripts/evaluate.py --split dev          # first 500 train documents
python scripts/evaluate.py --split test         # run once
```

## Browser extension (`extension/`)

The product shape: paste into ChatGPT, Claude or Gemini and the text is
redacted before it lands in the box; select the AI's answer and press
"Restore selection" to copy it with the real values back in.

- The extension calls the redactgate service on your own computer
  (`127.0.0.1:8840`) from its background worker; the chat site never sees the
  service or the mapping. The mapping lives only in that tab's memory.
- If the service is not running, the paste is **blocked** with a note,
  rather than letting the unredacted text through.

Install: start the service (`uvicorn redactgate.app:app --port 8840`), then
Chrome > Extensions > Developer mode > Load unpacked > `extension/`.

Tests (`cd extension && npm install && npm test`, 4 tests): `content.js` in
headless Chromium on a fake chat page served at `https://chatgpt.com`
(intercepted, nothing reaches the real site), calling the real local
service: paste into a textarea and into a rich-text editor, paste blocked
when the service is down, restore of a selected answer. `node
test/load-extension.js` loads the real unpacked extension and pastes through
its background worker. Not tested on the real ChatGPT, Claude or Gemini
pages, whose editors may handle inserted text differently.

## Not done

- No direct call to Claude or another model; it's copy and paste, or the
  JSON API. (No API key was available when this was built.)
- Swedish and other languages outside the model are untested.
- Output is text: a redacted PDF or Word file with the layout kept is not built.
- Presidio with custom recognizers was not tried; only its defaults.
