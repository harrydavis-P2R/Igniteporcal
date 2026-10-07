#!/usr/bin/env python3
"""Build the installable offline app (PWA) from src/calculator.html.

src/calculator.html is the page body (also published as a Claude artifact).
This writes:
  index.html            full page with app/iPad meta tags, local fonts and service worker registration
  manifest.webmanifest  app name, colours and icons
  sw.js                 service worker that caches every file so the app works offline

Run: python3 build.py
"""
import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT / "src/calculator.html").read_text()

# Use the self-hosted fonts instead of Google Fonts so nothing needs the internet.
src = re.sub(r'<link rel="(?:preconnect|stylesheet)" href="https://fonts\.(?:googleapis|gstatic)\.com[^>]*>\n', "", src)

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Ignite BA Day Calculator: what today's starter kit sales put in the retailer's pocket.">
<meta name="theme-color" content="#1d2a5e">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="BA Day">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="stylesheet" href="fonts/fonts.css">
<style>
/* Keep content clear of the iPad status bar and home indicator when opened from the Home Screen. */
:root { padding: env(safe-area-inset-top, 0px) env(safe-area-inset-right, 0px) env(safe-area-inset-bottom, 0px) env(safe-area-inset-left, 0px); background: #1d2a5e; }
html, body { -webkit-text-size-adjust: 100%; }
button { touch-action: manipulation; }
</style>
</head>
<body>
"""

INSTALL_BANNER = """
<div id="installBar" hidden style="position:fixed;left:0;right:0;bottom:0;z-index:50;background:#1d2a5e;color:#fff;padding:12px 16px calc(12px + env(safe-area-inset-bottom, 0px));display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;box-shadow:0 -4px 16px rgba(0,0,0,.2);font:15px Barlow, system-ui, sans-serif">
  <img src="icons/icon-192.png" alt="" width="40" height="40" style="border-radius:9px">
  <span id="installText" style="flex:1 1 240px;max-width:560px"></span>
  <button type="button" id="installBtn" hidden style="border:0;background:#ffd200;color:#1d2a5e;font:700 16px Barlow, system-ui, sans-serif;padding:10px 18px;border-radius:10px;cursor:pointer">Install app</button>
  <button type="button" id="installClose" aria-label="Hide" style="border:0;background:transparent;color:#fff;font-size:24px;line-height:1;cursor:pointer;padding:4px 8px">×</button>
</div>
<script>
(function () {
  // Show how to add the app to the Home Screen, unless it's already installed or was dismissed.
  var standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
  var dismissed = false;
  try { dismissed = localStorage.getItem("ba-install-dismissed") === "1"; } catch (e) {}
  if (standalone || dismissed || location.protocol === "file:") return;
  var bar = document.getElementById("installBar"), text = document.getElementById("installText"), btn = document.getElementById("installBtn");
  var ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  function show() { bar.hidden = false; document.body.style.paddingBottom = (bar.offsetHeight + 8) + "px"; }
  if (ios) {
    text.innerHTML = "<b>Add BA Day to your Home Screen:</b> tap the Share button <span aria-hidden='true'>(square with an arrow)</span>, then <b>Add to Home Screen</b>. It then works with no signal.";
    show();
  }
  var deferred = null;
  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault(); deferred = e;
    text.innerHTML = "<b>Install BA Day</b> on this device. It then opens like an app and works with no signal.";
    btn.hidden = false; show();
  });
  btn.addEventListener("click", function () {
    if (!deferred) return;
    deferred.prompt();
    deferred.userChoice.finally(function () { deferred = null; bar.hidden = true; document.body.style.paddingBottom = ""; });
  });
  document.getElementById("installClose").addEventListener("click", function () {
    bar.hidden = true; document.body.style.paddingBottom = "";
    try { localStorage.setItem("ba-install-dismissed", "1"); } catch (e) {}
  });
})();
</script>
"""

SW_REGISTER = """
<script>
if ("serviceWorker" in navigator && location.protocol !== "file:") {
  window.addEventListener("load", function () {
    var hadController = !!navigator.serviceWorker.controller;
    navigator.serviceWorker.register("sw.js").catch(function () {});
    // When a new version is installed, reload once so the BA is on the latest maths.
    navigator.serviceWorker.addEventListener("controllerchange", function () {
      if (hadController) location.reload();
    });
  });
}
</script>
</body>
</html>
"""

(ROOT / "index.html").write_text(HEAD + src + INSTALL_BANNER + SW_REGISTER)

manifest = {
    "name": "Ignite BA Day Calculator",
    "short_name": "BA Day",
    "description": "What today's Ignite starter kit sales put in the retailer's pocket.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "any",
    "background_color": "#eef0f6",
    "theme_color": "#1d2a5e",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}
(ROOT / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n")

# Everything the app needs offline. The cache name changes whenever any file changes,
# so installed copies pick up updates the next time they open with signal.
assets = ["./", "index.html", "manifest.webmanifest"]
assets += sorted(str(p.relative_to(ROOT)) for d in ("fonts", "icons") for p in (ROOT / d).iterdir() if p.is_file())
h = hashlib.sha256()
for a in assets[1:]:
    h.update((ROOT / a).read_bytes())
version = h.hexdigest()[:10]

sw = f"""// Generated by build.py. Caches the whole app so it works offline.
const CACHE = "ba-day-{version}";
const ASSETS = {json.dumps(assets, indent=2)};

self.addEventListener("install", (e) => {{
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
}});

self.addEventListener("activate", (e) => {{
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
}});

// Cache first, so the app opens instantly with no signal; fall back to the network for anything new.
self.addEventListener("fetch", (e) => {{
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request, {{ ignoreSearch: true }}).then((hit) =>
      hit || fetch(e.request).catch(() => e.request.mode === "navigate" ? caches.match("index.html") : Response.error())
    )
  );
}});
"""
(ROOT / "sw.js").write_text(sw)
print(f"Built index.html, manifest.webmanifest, sw.js (cache ba-day-{version}, {len(assets)} files)")
