// Calls the local redactgate service. The page never talks to it directly,
// so the chat site cannot read the mapping or reach the service.
const API = "http://127.0.0.1:8840/api/redact";

chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
  if (msg.type !== "redact") return;
  fetch(API, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ text: msg.text }),
  })
    .then((r) => (r.ok ? r.json() : Promise.reject(new Error("HTTP " + r.status))))
    .then((data) => reply({ ok: true, redacted: data.redacted, mapping: data.mapping }))
    .catch((e) => reply({ ok: false, error: String(e) }));
  return true; // reply asynchronously
});
