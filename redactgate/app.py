"""Local web page and JSON API.

  uvicorn redactgate.app:app --port 8840

POST /api/redact  {"text": ..., "use_model": true}  -> {"redacted", "mapping", "spans"}
POST /api/restore {"text": ..., "mapping": {...}}   -> {"text"}

Run it on your own machine or network: the mapping holds the original
values and is returned to the caller, never stored.
"""
import json
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .detect import detect
from .redact import PERSONAL, redact, restore

app = FastAPI(title="redactgate")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
MAX_CHARS = 100_000


class RedactIn(BaseModel):
    text: str
    use_model: bool = True


class RestoreIn(BaseModel):
    text: str
    mapping: dict[str, str]


def _run(text: str, use_model: bool):
    text = text[:MAX_CHARS]
    spans = detect(text, use_model=use_model, labels=PERSONAL)
    red, mapping = redact(text, spans=spans)
    return text, red, mapping, spans


@app.post("/api/redact")
def api_redact(body: RedactIn):
    text, red, mapping, spans = _run(body.text, body.use_model)
    return {"redacted": red, "mapping": mapping,
            "spans": [{"start": s.start, "end": s.end, "label": s.label, "source": s.source} for s in spans]}


@app.post("/api/restore")
def api_restore(body: RestoreIn):
    return {"text": restore(body.text, body.mapping)}


@app.get("/", response_class=HTMLResponse)
def page(request: Request):
    return templates.TemplateResponse(request, "index.html", {"text": ""})


@app.post("/", response_class=HTMLResponse)
def page_post(request: Request, text: str = Form(""), use_model: str = Form(""), reply: str = Form(""),
              mapping_json: str = Form(""), redacted: str = Form("")):
    if reply and mapping_json:
        mapping = json.loads(mapping_json)
        return templates.TemplateResponse(request, "index.html", {
            "text": text, "redacted": redacted, "mapping": mapping, "mapping_json": mapping_json,
            "reply": reply, "restored": restore(reply, mapping)})
    text, red, mapping, spans = _run(text, bool(use_model))
    counts = {}
    for s in spans:
        counts[s.label] = counts.get(s.label, 0) + 1
    return templates.TemplateResponse(request, "index.html", {
        "text": text, "redacted": red, "mapping": mapping, "mapping_json": json.dumps(mapping),
        "counts": sorted(counts.items()), "use_model": bool(use_model)})
