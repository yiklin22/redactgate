"""Tests that run the NER model (about 1 GB download on first run).
Skipped in CI: pytest -m "not model"."""
import pytest

from redactgate.redact import redact, restore

pytestmark = pytest.mark.model


def test_model_finds_a_name_without_a_label_word():
    text = "Yesterday Daniel Okafor asked for a refund."
    red, mapping = redact(text)
    assert "Daniel Okafor" not in red and "[PERSON_1]" in red
    assert restore(red, mapping) == text
