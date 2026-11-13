"""Reversible redaction: swap each detected value for a placeholder before the
text leaves your system, then put the values back into the answer.

The same value gets the same placeholder everywhere ("Maria Gonzalez" is
[PERSON_1] in every place it appears), so a model can still reason about who
did what. The mapping never leaves your side.
"""
from __future__ import annotations

import re

from .detect import Span, detect

PERSONAL = {"PERSON", "ADDRESS", "EMAIL", "PHONE", "CARD", "CVV", "IBAN", "BANK_ACCOUNT", "ROUTING", "SSN", "IP", "SWIFT",
            "SECRET", "ID", "DOB", "GEO"}


def redact(text: str, use_model: bool = True, labels: set[str] = PERSONAL,
           spans: list[Span] | None = None) -> tuple[str, dict[str, str]]:
    """Return (redacted text, mapping placeholder -> original value)."""
    if spans is None:
        spans = detect(text, use_model=use_model, labels=labels)
    by_value: dict[tuple[str, str], str] = {}
    counts: dict[str, int] = {}
    mapping: dict[str, str] = {}
    # Full names first, so a later (or earlier) "Mr. Quesada" can point to the
    # same person: "Jerónimo E. Quesada" -> [PERSON_1], "Quesada" -> [PERSON_1_LAST].
    last_names: dict[str, str] = {}
    for s in spans:
        value = text[s.start:s.end].strip()
        key = (s.label, value.lower())
        if s.label == "PERSON" and len(value.split()) > 1 and key not in by_value:
            counts["PERSON"] = counts.get("PERSON", 0) + 1
            by_value[key] = f"[PERSON_{counts['PERSON']}]"
            mapping[by_value[key]] = text[s.start:s.end]
            last_names.setdefault(value.split()[-1].lower(), by_value[key][:-1] + "_LAST]")
    out, pos = [], 0
    for s in spans:
        value = text[s.start:s.end]
        key = (s.label, value.strip().lower())
        if key not in by_value and s.label == "PERSON" and key[1] in last_names:
            by_value[key] = last_names[key[1]]
            mapping[by_value[key]] = value
        if key not in by_value:
            counts[s.label] = counts.get(s.label, 0) + 1
            by_value[key] = f"[{s.label}_{counts[s.label]}]"
            mapping[by_value[key]] = value
        out.append(text[pos:s.start])
        out.append(by_value[key])
        pos = s.end
    out.append(text[pos:])
    return "".join(out), mapping


def restore(text: str, mapping: dict[str, str]) -> str:
    """Put original values back. Also accepts placeholders a model wrote without
    brackets ("PERSON_1"). Placeholders the model invented are left as they are."""
    def sub(m):
        key = "[" + m.group(1) + "]"
        return mapping.get(key, m.group())
    return re.sub(r"\[?\b([A-Z]+(?:_[A-Z]+)*_\d+(?:_LAST)?)\b\]?", sub, text)
