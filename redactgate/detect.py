"""Find personal and secret data in text.

Two kinds of detectors:
- patterns with validation (card numbers pass the Luhn check, IBANs pass
  mod-97, routing numbers pass the ABA checksum), and patterns keyed on a
  nearby word ("passport no.", "password:");
- a named-entity model for people, places and organisations: by default
  Davlan/xlm-roberta-base-ner-hrl (AFL-3.0; de/en/es/fr/it/nl/pt and more),
  or dslim/bert-base-NER (MIT, English only). Both run on CPU.

Every detector returns Span(start, end, label, source).
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    label: str
    source: str


def _luhn(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
        alt = not alt
    return total % 10 == 0


def _iban_ok(s: str) -> bool:
    s = s.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    n = "".join(str(int(c, 36)) for c in s[4:] + s[:4])
    return int(n) % 97 == 1


def _aba_ok(d: str) -> bool:
    w = [3, 7, 1] * 3
    return len(d) == 9 and sum(int(c) * k for c, k in zip(d, w)) % 10 == 0


STREET = (r"(?i:alley|annex|arcade|avenue|ave|bayoo|beach|bend|bluffs?|bottoms?|boulevard|blvd|branch|bridge|brooks?|"
          r"burgs?|bypass|camp|canyon|cape|causeway|centers?|circles?|cir|cliffs?|close|club|commons?|corners?|course|"
          r"courts?|ct|coves?|creek|crescent|crest|crossing|crossroad|curve|dale|dam|divide|drives?|dr|estates?|"
          r"expressway|extensions?|falls?|ferry|fields?|flats?|fords?|forest|forges?|forks?|fort|freeway|gardens?|"
          r"gateways?|glens?|greens?|groves?|harbors?|haven|heights|highway|hwy|hills?|hollow|inlet|islands?|isle|"
          r"junctions?|keys?|knolls?|lakes?|land|landing|lane|ln|lights?|loaf|locks?|lodge|loop|mall|manors?|meadows?|"
          r"mews|mills?|mission|motorway|mount|mountains?|neck|orchard|oval|overpass|parks?|parkways?|pkwy|pass|"
          r"passage|path|pike|pines?|place|pl|plains?|plaza|points?|ports?|prairie|radial|ramp|ranch|rapids?|rest|"
          r"ridges?|river|roads?|rd|route|row|rue|run|shoals?|shores?|skyway|springs?|spurs?|squares?|st|station|"
          r"stravenue|stream|streets?|summit|terrace|throughway|trace|track|trafficway|trail|trailer|tunnel|turnpike|"
          r"underpass|unions?|valleys?|via|viaduct|views?|villages?|ville|vista|walks?|wall|ways?|wells?)")
CAP = r"[A-ZÀ-ÖØ-ÞĀ-Ž][^\W\d_]*(?:['-][^\W\d_]+)*"
# Street types written before the name (Rue de la Paix, Via Roma, Calle Mayor).
STREET_FIRST = (r"(?i:rue|avenue|boulevard|bd|chemin|allée|place|impasse|quai|route|calle|c/|avenida|avda\.?|camino|"
                r"pasaje|paseo|plaza|carrera|carrer|ronda|travesía|via|viale|piazza|corso|largo|strada|vicolo|contrada|rua|"
                r"acceso|alameda|bajada|callejón|cañada|carretera|cuesta|glorieta|pasadizo|rambla|urbanización|vía|"
                r"borgo|canale|incrocio|piazzale|rotonda|salita|stretto)")
AMBIGUOUS_FIRST = {"acceso", "alameda", "bajada", "callejón", "cañada", "carretera", "cuesta", "glorieta", "pasadizo",
                   "rambla", "urbanización", "vía", "borgo", "canale", "incrocio", "piazzale", "rotonda", "salita", "stretto"}
# Street types joined to the end of the name (Schnellstraße, Kayleighstraat, Åkervägen).
STREET_SUFFIX = (r"(?:straße|strasse|str\.|gasse|weg|ring|platz|allee|damm|ufer|steeg|straat|laan|gracht|plein|kade|"
                 r"singel|dreef|vägen|gatan|väg|gata|stigen|stig|baan|boulevard|torget|torg|gränd)")
# One word ending in a street type ("Roggestr.", "Annerose-Kühnert-Platz",
# "Kvarntorget"), with a house number before or after it (not a year), so that
# ordinary words such as "Spring" are not taken for a street.
SUFFIX_STREET = r"\b[A-ZÀ-ÖØ-ÞĀ-Ž](?:[^\W\d_]|-(?=[^\W\d_])){0,40}?(?i:" + STREET_SUFFIX + r")(?:\b|(?<=\.))"
HOUSE_NO = r"(?!(?:19|20)\d\d\b)\d{1,4}[a-z]?(?:/\d+)?\b"
# A postal address written over several lines: "123 Main Street" / "Toronto, ON M5J 1K1" / "Canada".
# The city line must carry a postcode or a two-letter code (state, country), or
# be followed by a postcode line; the last line may be a country.
_W = CAP + r"(?:[ \t]+" + CAP + r"){0,2}"
_COUNTRY = (r"(?:USA|US|UK|U\.S\.A?\.|United States(?: of America)?|United Kingdom|Canada|Australia|Ireland|"
            r"Germany|Deutschland|Austria|Österreich|France|Spain|España|Portugal|Italy|Italia|Netherlands|Nederland|"
            r"Belgium|België|Belgique|Sweden|Switzerland|Schweiz|Suisse|Mexico|México)")
# Two-letter codes on a city line: US states, Canadian provinces, UK.
_STATE = (r"(?:A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|PA|RI|S[CD]|T[NX]|UT|"
          r"V[AT]|W[AIVY]|AB|BC|MB|N[BLST]|ON|PE|QC|SK|YT|UK)")
_POST = (r"(?:[A-Z]{2}[ \t]+\d{5}(?:-\d{4})?|[A-Z]{2}[ \t]+[A-Z]\d[A-Z][ \t]?\d[A-Z]\d|[A-Z]\d[A-Z][ \t]?\d[A-Z]\d|"
         r"[A-Z]{1,2}\d[A-Z\d]?[ \t]?\d[A-Z]{2}|\d{4}[ \t]?[A-Z]{2}|\d{4,6})")
LINE_TAIL = (r"(?:\n[ \t]*" + _W + r",[ \t]*(?:(?:" + _POST + r"|" + _STATE + r"|" + _COUNTRY + r")\b(?:,[ \t]*(?:" + _POST + r"|" + _STATE + r"|" + _COUNTRY + r")\b)*"
             r"(?:\n[ \t]*" + _POST + r"(?=[ \t]*(?:\n|$)))?|" + _W + r"\n[ \t]*" + _POST + r"(?=[ \t]*(?:\n|$)))"
             r"(?:\n[ \t]*" + _COUNTRY + r"(?=[ \t]*(?:\n|$)))?)?")
ADDR_TAIL = (r"(?:,?\s+(?:[A-Z]{2}\s+\d{5}(?:-\d{4})?|[A-Z]\d[A-Z]\s?\d[A-Z]\d|[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}|\d{4}\s?[A-Z]{2}(?:\s+" + CAP + r")?|\d{5}(?:\s+" + CAP + r")?)"
             r"|,\s*(?:" + CAP + r"(?:\s+" + CAP + r"){0,2}|[A-Z]{2}|\d{4,6}(?:\s+" + CAP + r")?)){0,4}")

# (label, regex, validator or None, value group)
PATTERNS = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), None, 0),
    ("CARD", re.compile(r"(?<![\d-])(?:\d[ -]?){12,18}\d(?![\d-])"),
     lambda m: _luhn(re.sub(r"\D", "", m.group())), 0),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?\b"),
     lambda m: _iban_ok(m.group()), 0),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), None, 0),
    ("IP", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"), None, 0),
    ("IP", re.compile(r"(?<![\w:])(?:[0-9a-fA-F]{1,4}:){3,7}[0-9a-fA-F]{1,4}(?![\w:])|"
                      r"(?<![\w:])(?:[0-9a-fA-F]{1,4}:){1,6}:(?:[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){0,5})?(?![\w:])"),
     lambda m: bool(re.search(r"[a-fA-F]|::", m.group())), 0),
    ("PHONE", re.compile(r"(?<![\w+])\+\d{1,3}(?:[\s.-]?(?:\(\d{1,4}\)|\d{1,4})){2,5}(?![\w])|(?<![\w])0\d(?:[\s.-]\d{2}){4}(?![\w])"),
     lambda m: 9 <= len(re.sub(r"\D", "", m.group())) <= 15, 0),
    ("IBAN", re.compile(r"(?i:iban)\s*:?\s*([A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?)\b"), None, 1),
    ("PHONE", re.compile(r"(?<![\w+])(?:\+\d{1,3}[\s.-]?)?(?:\(\d{2,4}\)[\s.-]?)?\d{2,4}[\s.-]\d{3,4}(?:[\s.-]\d{2,4})?"
                         r"(?:\s*(?:x|ext\.?)\s*\d{1,5})?(?![\w])|(?<![\w+])\+\d{8,14}(?!\w)"),
     lambda m: len(re.sub(r"\D", "", m.group())) >= 9, 0),
    ("ROUTING", re.compile(r"(?i:routing|aba|rtn|transit)[^\d\n]{0,25}(\d{9})\b"), lambda m: _aba_ok(m.group(1)), 1),
    ("SWIFT", re.compile(r"(?i:swift|bic|bank\s+identifier)[^\n]{0,25}?\b([A-Z]{6}[A-Z0-9]{2}(?:[A-Z0-9]{3})?)\b"), None, 1),
    ("CVV", re.compile(r"(?i:cvv2?|cvc|security\s+code|card\s+verification)[^\d\n]{0,20}(\d{3,4})\b"), None, 1),
    ("SECRET", re.compile(r"(?i:password|passcode|passwd|pin|api[\s_-]?key|secret|access\s+token|token)"
                          r"\s*(?:is|:|=)\s*[\"']?([^\s\"',;]{4,})"), None, 1),
    ("SECRET", re.compile(r"\b(?:sk|pk|rk)_(?:live|test)_[A-Za-z0-9]{10,}\b|\bAKIA[0-9A-Z]{16}\b|\bgh[pousr]_[A-Za-z0-9]{20,}\b"), None, 0),
    ("ID", re.compile(r"(?i:passport|driver'?s?\s+licen[cs]e|licen[cs]e|employee|staff|customer|client|member|account|acct|"
                      r"policy|tax|national|social\s+security)\s*(?i:id|no\.?|number|num|#)?[\s:*#]*(?i:is\s+)?"
                      r"([A-Za-z0-9][A-Za-z0-9-]{3,}\d[A-Za-z0-9-]*|\d[A-Za-z0-9-]{4,})\b"), None, 1),
    ("DOB", re.compile(r"(?i:born|birth|d\.?o\.?b\.?|geburtsdatum|geboren|naissance|n[ée]\(?e?\)?\s+le|nacimiento|nacid[oa]|"
                       r"nascita|nat[oa]\s+il|geboortedatum|f[öo]delsedatum|f[öo]dd)[^\n\d]{0,20}"
                       r"(\d{1,4}[/.-]\d{1,2}[/.-]\d{1,4}|\d{8}|[^\W\d_]+\.?\s+\d{1,2},?\s+\d{4}|\d{1,2}\.?\s+[^\W\d_]+\.?\s+\d{4})"), None, 1),
    ("GEO", re.compile(r"-?\d{1,3}\.\d{3,},?\s+-?\d{1,3}\.\d{3,}|-?\d{1,3}\.\d{3,},-?\d{1,3}\.\d{3,}"), None, 0),
    ("GEO", re.compile(r"(?i:latitude)\s*:?\s*-?\d{1,3}\.\d+,?\s*(?i:longitude)\s*:?\s*-?\d{1,3}\.\d+"), None, 0),
    ("PERSON", re.compile(r"(?i:full\s+name|name|signature|signed|cardholder(?:\s+name)?|beneficiary(?:\s+name)?|"
                          r"account\s+holder|applicant|borrower|patient|employee\s+name|customer\s+name|attn|attention|"
                          r"nom|prénom|nom\s+complet|destinataire|expéditeur|titulaire|bénéficiaire|empfänger|auftraggeber|"
                          r"kontoinhaber|vollständiger\s+name|nombre|nombre\s+completo|titular|beneficiario|nome|nome\s+completo|"
                          r"intestatario|naam|volledige\s+naam|begunstigde|rekeninghouder|namn)"
                          r"[\"']?\s*(?:[:=>]|\bis\b)\s*[\"']?\s*"
                          r"(" + CAP + r"(?:\s+(?:[A-Z]\.|" + CAP + r")){1,3})"), None, 1),
    ("ROUTING", re.compile(r"(?i:routing|aba)\s*(?i:number|no\.?|#)?[^\d\n]{0,30}?(\d{9})\b"), None, 1),
    ("SECRET", re.compile(r"(?<![\w-])(?=[A-Za-z0-9_-]{20,64}(?![\w-]))(?=[A-Za-z0-9_-]*[a-z])(?=[A-Za-z0-9_-]*[A-Z])(?=[A-Za-z0-9_-]*\d)[A-Za-z0-9_-]{20,64}"),
     lambda m: not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]+", m.group()), 0),
    ("SECRET", re.compile(r"(?i:password|passcode|passwd)\b[^.\n]{0,30}?(?:[:=]|\bis\b|\bbe\b|['\"]|e\.g\.)\s*['\"]?([^\s'\",;]{6,40})"),
     lambda m: bool(re.search(r"\d|[^\w]", m.group(1))) and not m.group(1).startswith("("), 1),
    ("SECRET", re.compile(r"(?i:\bpin)\b[^\d\n]{0,25}(\d{4,6})\b"), None, 1),
    ("ID", re.compile(r"(?i:user\s*name|username|user\s*id|login)\s*[:=]\s*\**\s*([\w.@-]{3,})"), None, 1),
    ("ID", re.compile(r"(?i:\buser)\s+([\w.@-]*\d[\w.@-]*)"), None, 1),
    ("CARD", re.compile(r"(?i:card)[^\n\d]{0,25}(\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{3,4}|\d{4}[ -]\d{6}[ -]\d{5}|\d{15,16})\b"), None, 1),
    ("BANK_ACCOUNT", re.compile(r"\b[A-Z]{4}\d{10,30}\b"), None, 0),
    ("BANK_ACCOUNT", re.compile(r"(?i:bban|account\s+(?:number|no\.?|#))[^\w\n]{0,4}([A-Z0-9]{6,34})\b"),
     lambda m: any(c.isdigit() for c in m.group(1)), 1),
    ("SWIFT", re.compile(r"\b[A-Z]{6}[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b"),
     lambda m: any(c.isdigit() for c in m.group()) and m.group()[:4].isalpha(), 0),
    ("SECRET", re.compile(r"(?<![\w@])[^\s\"'<>()\[\]{},;]{10,40}(?![\w])"),
     lambda m: sum(bool(re.search(rx, m.group())) for rx in (r"[a-z]", r"[A-Z]", r"\d", r"[^\w\s]")) >= 4
     and not re.search(r"https?:|www\.|@|\.(?:com|org|net)\b|^\$|[.,:]$|[:/|=]|^\(|\d{5}|-\d{4}", m.group()), 0),
    # For street types that are also ordinary words or names (Borgo, Canale), not
    # after a capitalised word ("Version 2 Canale Today", "Section 4 Borgo Notes").
    ("ADDRESS", re.compile(r"\b\d{1,5}[a-z]?,?\s+" + STREET_FIRST + r"\s+(?:(?i:de|del|de la|des|du|di|della|dei|da|la|le|les|el|los|las|y|d'|d’|l'|l’)\s*)*"
                           + CAP + r"(?:\s+" + CAP + r"){0,3}(?:,?\s*(?i:apt|apartment|appartamento|piso|piano|puerta|étage)\.?\s*#?\w+)?" + ADDR_TAIL + LINE_TAIL),
     lambda m: not (re.match(r"\d+[a-z]?,?\s+(\w+)", m.group()).group(1).lower() in AMBIGUOUS_FIRST
                    and re.search(r"(?:^|[^\w])[A-ZÀ-ÖØ-Þ][^\W\d_]*[ \t]+$", m.string[max(0, m.start() - 40):m.start()])), 0),
    ("ADDRESS", re.compile(r"\b" + STREET_FIRST + r"\s+(?:(?i:de|del|de la|des|du|di|della|dei|da|la|le|les|el|los|las|y|d'|d’|l'|l’)\s*)*"
                           + CAP + r"(?:\s+" + CAP + r"){0,3},?\s+\d{1,5}[a-z]?\b"
                           r"(?:,?\s*(?i:apt|apartment|appartamento|piso|piano|puerta|étage)\.?\s*#?\w+)?" + ADDR_TAIL + LINE_TAIL), None, 0),
    ("ADDRESS", re.compile(r"(?:\b\d{1,5}[a-z]?,?\s+" + SUFFIX_STREET + r"(?:\s+" + HOUSE_NO + r")?|\b" + SUFFIX_STREET + r"\s+" + HOUSE_NO + r")"
                           r"(?:,?\s*(?i:apt|apartment|wohnung)\.?\s*#?\w+)?" + ADDR_TAIL + LINE_TAIL), None, 0),
    ("ADDRESS", re.compile(r"(?:\b\d{1,3}(?:st|nd|rd|th)\s+(?i:floor),\s*)?"
                           r"\b\d{1,6}\s+(?:" + CAP + r"[ \t]+){1,4}" + STREET + r"\b\.?"
                           r"(?:,?\s*(?i:apt|apartment|suite|unit|ste|floor)\.?\s*#?\w+)?"
                           # then up to four parts: city, state, postcode, country
                           r"(?:,?\s+(?:[A-Z]{2}\s+\d{5}(?:-\d{4})?|[A-Z]\d[A-Z]\s?\d[A-Z]\d|[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}|\d{5})"
                           r"|,\s*(?:" + CAP + r"(?:\s+" + CAP + r"){0,2}|[A-Z]{2}|\d{4,6})){0,4}" + LINE_TAIL), None, 0),
    ("PERSON", re.compile(r"\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|M|Mme|Mlle|Monsieur|Madame|Herr|Frau|Sr|Sra|Señor|Señora|Sig|Sig\.ra|Signor|Signora|Dhr|Mevr|Mevrouw)\.?\s+(" + CAP + r"(?:\s+(?:[A-Z]\.|" + CAP + r")){0,3})"), None, 1),
    ("PERSON", re.compile(r"(?i:dear|sincerely|regards|best)\s*,?\s+(" + CAP + r"(?:\s+(?:[A-Z]\.|" + CAP + r")){1,3})"), None, 1),
]


def find_patterns(text: str) -> list[Span]:
    out = []
    for label, rx, ok, group in PATTERNS:
        for m in rx.finditer(text):
            if ok is not None and not ok(m):
                continue
            start, end = m.start(group), m.end(group)
            while end > start and text[end - 1] in ".,;:":  # sentence punctuation is not part of the value
                end -= 1
            out.append(Span(start, end, label, "pattern"))
    return out


NER_LABELS = {"PER": "PERSON", "LOC": "ADDRESS", "ORG": "ORG"}
ROLES = {"lender", "borrower", "consultant", "client", "company", "party", "parties", "licensee", "licensor", "supplier",
         "buyer", "seller", "tenant", "landlord", "employer", "employee", "contractor", "customer", "vendor", "purchaser",
         "distributor", "agent", "guarantor", "investor", "manager", "owner", "recipient", "discloser", "provider"}
COMMON_WORDS = {"during", "monitoring", "mastering", "transferring", "offering", "remaining", "following", "including",
                "regarding", "pursuant", "notwithstanding", "subject", "provided", "section", "article", "schedule",
                "exhibit", "annex", "appendix", "currently", "northeast", "northwest", "southeast", "southwest"}
# "en": English-only BERT (MIT). "multi": XLM-RoBERTa for de/en/es/fr/it/nl/pt and
# others (AFL-3.0), slower.
NER_MODELS = {"en": "dslim/bert-base-NER", "multi": "Davlan/xlm-roberta-base-ner-hrl"}
_NER: dict = {}


def _pipeline(model: str = "en"):
    if model not in _NER:
        from transformers import pipeline
        _NER[model] = pipeline("token-classification", model=NER_MODELS[model],
                               aggregation_strategy="simple", device=-1)
    return _NER[model]


def find_entities(text: str, min_score: float = 0.6, chunk: int = 1500, model: str = "multi") -> list[Span]:
    """People, places and organisations from the NER model. Long text is read in
    overlapping chunks because the model sees at most 512 tokens."""
    out, ner = [], _pipeline(model)
    step = chunk - 200
    for base in range(0, max(1, len(text)), step):
        part = text[base: base + chunk]
        if not part.strip():
            continue
        for e in ner(part):
            label = NER_LABELS.get(e["entity_group"])
            st, en = base + int(e["start"]), base + int(e["end"])
            if not label or float(e["score"]) < min_score or en - st < 3:
                continue
            # The model can stop part-way through a word ("Mälz" of "Mälzer");
            # widen the span to whole words.
            while st > 0 and (text[st - 1].isalnum() or (text[st - 1] == "-" and st > 1 and text[st - 2].isalnum())):
                st -= 1
            while en < len(text) and (text[en].isalnum() or (text[en] == "-" and en + 1 < len(text) and text[en + 1].isalnum())):
                en += 1
            # A place name alone ("London", "USA") is not personal data; keep a
            # place only when it is part of a street address (a number nearby).
            if label == "ADDRESS" and not re.search(r"\d", text[max(0, st - 12): en + 12]):
                continue
            word = text[st:en]
            # Contract roles ("Lender", "the Consultant") and single ordinary
            # words the model tags at the start of a sentence are not names.
            if label == "PERSON" and word.lower() in ROLES:
                continue
            if label == "ADDRESS" and " " not in word and not re.search(r"\d", word) and word.lower() in COMMON_WORDS:
                continue
            out.append(Span(st, en, label, "ner"))
        if base + chunk >= len(text):
            break
    return out


# When spans overlap, the more specific label wins.
PRIORITY = ["SECRET", "CARD", "CVV", "IBAN", "BANK_ACCOUNT", "ROUTING", "SSN", "EMAIL", "IP", "SWIFT", "DOB", "ID", "PHONE",
            "GEO", "ADDRESS", "PERSON", "ORG"]


def merge(spans: list[Span], text: str = "") -> list[Span]:
    """Union overlapping spans; the merged span takes the highest-priority label.
    Address pieces split only by ", " are joined into one address."""
    out: list[Span] = []
    for s in sorted(spans, key=lambda s: (s.start, -s.end)):
        if (out and text and s.label == "ADDRESS" == out[-1].label and 0 <= s.start - out[-1].end <= 2
                and not text[out[-1].end:s.start].strip(" ,")):
            out[-1] = Span(out[-1].start, max(out[-1].end, s.end), "ADDRESS", out[-1].source)
        elif out and s.start < out[-1].end:
            last = out[-1]
            label = min((last.label, s.label), key=PRIORITY.index)
            out[-1] = Span(last.start, max(last.end, s.end), label, last.source if label == last.label else s.source)
        else:
            out.append(s)
    return out


def propagate(text: str, spans: list[Span]) -> list[Span]:
    """Mask every other place the same value appears ("Brett King" found once
    is masked everywhere in the document)."""
    out = list(spans)
    seen = set()
    for s in spans:
        value = text[s.start:s.end]
        if len(value) < 4 or (s.label, value) in seen:
            continue
        seen.add((s.label, value))
        for m in re.finditer(r"(?<!\w)" + re.escape(value) + r"(?!\w)", text):
            out.append(Span(m.start(), m.end(), s.label, s.source))
    return out


def detect(text: str, use_model: bool = True, labels: set[str] | None = None, model: str = "multi") -> list[Span]:
    spans = find_patterns(text) + (find_entities(text, model=model) if use_model else [])
    if labels is not None:
        spans = [s for s in spans if s.label in labels]
    return merge(propagate(text, merge(spans, text)), text)
