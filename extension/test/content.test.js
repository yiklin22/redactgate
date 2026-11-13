// Runs content.js in headless Chromium on a fake chat page served at
// https://chatgpt.com (intercepted; nothing reaches the real site). The
// extension's background call is replaced by a bridge to the real local
// redactgate service on 127.0.0.1:8840, or by a failure for the "down" case.
const test = require("node:test");
const assert = require("node:assert");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const PAGE = fs.readFileSync(path.join(__dirname, "fake-chat.html"), "utf8");
const CONTENT = path.join(__dirname, "..", "content.js");
const TEXT = "Please refund Ms. Ana Lima (ana.lima@example.com, +1 (415) 555-0132), card 4111 1111 1111 1111.";
let browser;

test.before(async () => { browser = await chromium.launch(); });
test.after(async () => { await browser.close(); });

async function open({ serviceUp = true } = {}) {
  const ctx = await browser.newContext();
  await ctx.route("https://chatgpt.com/**", (r) => r.fulfill({ contentType: "text/html", body: PAGE }));
  const page = await ctx.newPage();
  await page.exposeFunction("rgRedact", async (text) => {
    if (!serviceUp) return { ok: false, error: "connection refused" };
    const r = await fetch("http://127.0.0.1:8840/api/redact", {
      method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ text, use_model: false }),
    });
    const d = await r.json();
    return { ok: true, redacted: d.redacted, mapping: d.mapping };
  });
  await page.addInitScript(() => {
    window.chrome = { runtime: { sendMessage: (msg, cb) => { window.rgRedact(msg.text).then(cb); } } };
  });
  await page.addInitScript({ path: CONTENT });
  await page.goto("https://chatgpt.com/");
  return page;
}

async function paste(page, selector, text) {
  await page.focus(selector);
  await page.evaluate(([sel, t]) => {
    const dt = new DataTransfer();
    dt.setData("text/plain", t);
    document.querySelector(sel).dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt, bubbles: true, cancelable: true }));
  }, [selector, text]);
}

test("paste into a textarea inserts the redacted text", async () => {
  const page = await open();
  await paste(page, "#ta", TEXT);
  await page.waitForFunction(() => document.querySelector("#ta").value.length > 0);
  const v = await page.inputValue("#ta");
  assert.ok(!v.includes("ana.lima@example.com") && !v.includes("4111"), v);
  assert.match(v, /\[EMAIL_1\]/);
  assert.match(v, /\[CARD_1\]/);
  assert.match(await page.textContent("#redactgate-note"), /replaced \d+ values/);
  await page.context().close();
});

test("paste into a rich-text editor inserts the redacted text", async () => {
  const page = await open();
  await paste(page, "#ce", TEXT);
  await page.waitForFunction(() => document.querySelector("#ce").textContent.length > 0);
  const v = await page.textContent("#ce");
  assert.ok(!v.includes("ana.lima@example.com"), v);
  assert.match(v, /\[PHONE_1\]/);
  await page.context().close();
});

test("with the service down, the paste is blocked, not passed through", async () => {
  const page = await open({ serviceUp: false });
  await paste(page, "#ta", TEXT);
  await page.waitForSelector("#redactgate-note");
  assert.equal(await page.inputValue("#ta"), "");
  assert.match(await page.textContent("#redactgate-note"), /not running/);
  await page.context().close();
});

test("Restore selection puts the real values back", async () => {
  const page = await open();
  await paste(page, "#ta", TEXT);
  await page.waitForFunction(() => document.querySelector("#ta").value.length > 0);
  await page.evaluate(() => {
    const r = document.createRange();
    r.selectNodeContents(document.querySelector("#answer"));
    const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  });
  await page.click("#redactgate-restore");
  await page.waitForFunction(() => window.__redactgateLastRestore);
  const out = await page.evaluate(() => window.__redactgateLastRestore);
  assert.match(out, /Dear Ana Lima, we refunded/);
  assert.match(out, /went to ana\.lima@example\.com\./);
  assert.match(out, /\[PERSON_9\] is unknown/);
  await page.context().close();
});
