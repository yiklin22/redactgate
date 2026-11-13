// Loads the real unpacked extension in Chromium (new headless mode) and pastes
// into a fake chatgpt.com page, so the manifest, the background worker and its
// call to the local service are exercised end to end.
const path = require("path");
const fs = require("fs");
const os = require("os");
const { chromium } = require("playwright");

(async () => {
  const ext = path.join(__dirname, "..");
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "rg-ext-"));
  const ctx = await chromium.launchPersistentContext(dir, {
    channel: "chromium", headless: true,
    args: [`--disable-extensions-except=${ext}`, `--load-extension=${ext}`],
  });
  let [worker] = ctx.serviceWorkers();
  if (!worker) worker = await ctx.waitForEvent("serviceworker", { timeout: 10000 });
  console.log("service worker:", worker.url());
  await ctx.route("https://chatgpt.com/**", (r) => r.fulfill({ contentType: "text/html", body: fs.readFileSync(path.join(__dirname, "fake-chat.html"), "utf8") }));
  const page = await ctx.newPage();
  await page.goto("https://chatgpt.com/");
  await page.waitForSelector("#redactgate-restore", { timeout: 10000 });
  await page.focus("#ta");
  await page.evaluate(() => {
    const dt = new DataTransfer(); dt.setData("text/plain", "Email ana.lima@example.com about card 4111 1111 1111 1111.");
    document.querySelector("#ta").dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt, bubbles: true, cancelable: true }));
  });
  await page.waitForFunction(() => document.querySelector("#ta").value.length > 0, null, { timeout: 30000 });
  console.log("textarea:", await page.inputValue("#ta"));
  await ctx.close();
  fs.rmSync(dir, { recursive: true, force: true });
})().catch((e) => { console.error("FAILED:", e.message.split("\n")[0]); process.exit(1); });
