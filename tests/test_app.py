from fastapi.testclient import TestClient

from redactgate.app import app

c = TestClient(app)


def test_api_round_trip():
    r = c.post("/api/redact", json={"text": "Email ana@lima.pt or call +1 (415) 555-0132.", "use_model": False}).json()
    assert "ana@lima.pt" not in r["redacted"] and "[EMAIL_1]" in r["redacted"]
    back = c.post("/api/restore", json={"text": "Wrote to [EMAIL_1].", "mapping": r["mapping"]}).json()
    assert back["text"] == "Wrote to ana@lima.pt."


def test_page_redacts_and_restores():
    page = c.post("/", data={"text": "Call Ms. Ana Lima on +1 (415) 555-0132."}).text
    assert "[PHONE_1]" in page and "[PERSON_1]" in page
    import json, re, html
    mapping = html.unescape(re.search(r'name="mapping_json" value="([^"]*)"', page).group(1))
    page = c.post("/", data={"text": "x", "reply": "Called [PERSON_1].", "mapping_json": mapping}).text
    assert "Called Ana Lima." in page
