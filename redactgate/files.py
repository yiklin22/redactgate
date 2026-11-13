"""Text from uploaded files: .txt, .pdf (text layer only, no OCR) and .docx."""
import io

MAX_BYTES = 10 * 1024 * 1024


class Unreadable(ValueError):
    pass


def read_text(name: str, data: bytes) -> str:
    if len(data) > MAX_BYTES:
        raise Unreadable("file is larger than 10 MB")
    low = name.lower()
    if low.endswith(".txt") or low.endswith(".md") or low.endswith(".eml"):
        return data.decode("utf-8", errors="replace")
    if low.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        if not text.strip():
            raise Unreadable("the PDF has no text layer (a scan?); OCR is not supported")
        return text
    if low.endswith(".docx"):
        import docx
        d = docx.Document(io.BytesIO(data))
        parts = [p.text for p in d.paragraphs]
        for table in d.tables:
            for row in table.rows:
                parts.append(" | ".join(c.text for c in row.cells))
        return "\n".join(parts)
    raise Unreadable("only .txt, .pdf and .docx files are supported")
