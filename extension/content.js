// redactgate content script for AI chat sites.
// Paste: the text goes to the local service first; the redacted version is
// inserted instead. If the service is not running, the paste is blocked and
// a note says so (nothing unredacted goes in by accident).
// Restore: select the AI's answer and press the button; the original values
// replace the placeholders and the result is copied to the clipboard.
(function () {
  "use strict";
  const mapping = {}; // placeholder -> original, this tab only, never stored on disk
  const NOTE_ID = "redactgate-note";

  function note(text, ms = 4000) {
    let n = document.getElementById(NOTE_ID);
    if (!n) {
      n = document.createElement("div");
      n.id = NOTE_ID;
      n.style.cssText = "position:fixed;right:16px;bottom:16px;z-index:2147483647;max-width:320px;" +
        "background:#1b1f24;color:#fff;font:14px/1.4 system-ui,sans-serif;padding:10px 14px;border-radius:8px";
      document.documentElement.appendChild(n);
    }
    n.textContent = text;
    clearTimeout(n._t);
    n._t = setTimeout(() => n.remove(), ms);
  }

  function restore(text) {
    // Same rule as redactgate.redact.restore: brackets optional, _LAST for surnames.
    return text.replace(/\[?\b([A-Z]+(?:_[A-Z]+)*_\d+(?:_LAST)?)\b\]?/g, (m, key) => mapping["[" + key + "]"] ?? m);
  }

  function insert(target, text) {
    if (target.tagName === "TEXTAREA" || target.tagName === "INPUT") {
      const s = target.selectionStart ?? target.value.length;
      const e = target.selectionEnd ?? target.value.length;
      target.value = target.value.slice(0, s) + text + target.value.slice(e);
      target.selectionStart = target.selectionEnd = s + text.length;
      target.dispatchEvent(new Event("input", { bubbles: true }));
    } else {
      document.execCommand("insertText", false, text);
    }
  }

  function editable(el) {
    return el && (el.tagName === "TEXTAREA" || el.tagName === "INPUT" || el.isContentEditable);
  }

  document.addEventListener("paste", (ev) => {
    const target = ev.target.closest ? ev.target.closest("textarea,input,[contenteditable='true'],[contenteditable='']") : null;
    if (!editable(target)) return;
    const text = ev.clipboardData && ev.clipboardData.getData("text/plain");
    if (!text) return;
    ev.preventDefault();
    ev.stopImmediatePropagation();
    chrome.runtime.sendMessage({ type: "redact", text }, (res) => {
      if (!res || !res.ok) {
        note("redactgate: the local service is not running, so the paste was blocked. Start it with: uvicorn redactgate.app:app --port 8840", 8000);
        return;
      }
      Object.assign(mapping, res.mapping);
      target.focus();
      insert(target, res.redacted);
      const n = Object.keys(res.mapping).length;
      note(n ? `redactgate: replaced ${n} value${n > 1 ? "s" : ""} with placeholders.` : "redactgate: nothing to redact.");
    });
  }, true);

  const btn = document.createElement("button");
  btn.id = "redactgate-restore";
  btn.textContent = "Restore selection";
  btn.title = "Put the real values back into the selected text and copy it";
  btn.style.cssText = "position:fixed;right:16px;bottom:64px;z-index:2147483647;font:13px system-ui,sans-serif;" +
    "padding:6px 10px;border-radius:6px;border:1px solid #888;background:#fff;color:#111;cursor:pointer";
  btn.addEventListener("mousedown", (e) => e.preventDefault()); // keep the selection
  btn.addEventListener("click", async () => {
    const sel = String(window.getSelection() || "");
    if (!sel) return note("redactgate: select the answer first.");
    const out = restore(sel);
    try {
      await navigator.clipboard.writeText(out);
      note("redactgate: restored text copied to the clipboard.");
    } catch (e) {
      note("redactgate: could not copy; restored text is in the console.");
      console.log(out);
    }
    window.__redactgateLastRestore = out; // for tests
  });
  const add = () => document.body.appendChild(btn);
  if (document.body) add();
  else document.addEventListener("DOMContentLoaded", add, { once: true });
})();
