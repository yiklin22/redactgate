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


def _pdf(text):
    import io
    from reportlab.pdfgen import canvas
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    if text:
        c.drawString(72, 720, text)
    c.showPage()
    c.save()
    return buf.getvalue()


def _docx(text):
    import io
    import docx
    d = docx.Document()
    d.add_paragraph(text)
    t = d.add_table(rows=1, cols=2)
    t.rows[0].cells[0].text = "Phone"
    t.rows[0].cells[1].text = "+1 (415) 555-0132"
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def test_redact_pdf_and_docx_uploads():
    r = c.post("/api/redact-file", files={"file": ("a.pdf", _pdf("Email ana@lima.pt today."))}, data={"use_model": "false"})
    assert r.status_code == 200 and "[EMAIL_1]" in r.json()["redacted"] and "ana@lima.pt" not in r.json()["redacted"]
    r = c.post("/api/redact-file", files={"file": ("a.docx", _docx("Email ana@lima.pt today."))}, data={"use_model": "false"})
    red = r.json()["redacted"]
    assert "[EMAIL_1]" in red and "[PHONE_1]" in red  # table cells are read too


def test_rejects_unsupported_and_scanned_files():
    assert c.post("/api/redact-file", files={"file": ("a.xlsx", b"PK..")}).status_code == 415
    r = c.post("/api/redact-file", files={"file": ("scan.pdf", _pdf(""))})
    assert r.status_code == 415 and "text layer" in r.json()["detail"]
    page = c.post("/", files={"file": ("scan.pdf", _pdf(""))}).text
    assert "Could not read the file" in page
