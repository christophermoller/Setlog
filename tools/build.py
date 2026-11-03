"""Build Setlog: src/app_src.html + src/lib.json -> index.html (PWA), sw.js, manifest, plus dist/artifact.html (Claude artifact build).
Run from the repo root: python3 tools/build.py"""
import json, hashlib, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
src = open(R + 'src/app_src.html').read()
app = src.replace('/*__LIB__*/[]', open(R + 'src/lib.json').read())
os.makedirs(R + 'dist', exist_ok=True)
open(R + 'dist/artifact.html', 'w').write(app)
def rep(old, new):
    global app
    assert app.count(old) == 1, old[:80]
    app = app.replace(old, new)
rep("function dbSet(path, data) {", "function dbSet(path, data) { if (!window.claude) return;")
rep("function dbDel(path) {", "function dbDel(path) { if (!window.claude) return;")
rep("var qs = {}, PK = 'saetlog.pending', pend = {};", "var qs = {}, PK = 'saetlog.pending', pend = {}; if (!window.claude) { try { localStorage.removeItem('saetlog.pending'); } catch (e) {} }")
rep('<meta name="claude:viewport-fit-sides" content="cover">', '')
ver = hashlib.sha1(app.encode()).hexdigest()[:10]
head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Setlog">
<meta name="theme-color" content="#1B1B1D">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="manifest" href="manifest.webmanifest">
<style>html,body{margin:0;height:100%;background:#1B1B1D}@media (display-mode: standalone){#app{padding-top:env(safe-area-inset-top)}}</style>
"""
tail = """
<script>if ('serviceWorker' in navigator) window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });</script>
"""
open(R + 'index.html', 'w').write(head + app + tail)
json.dump({"name": "Setlog", "short_name": "Setlog", "start_url": "./", "scope": "./", "display": "standalone", "background_color": "#1B1B1D", "theme_color": "#1B1B1D",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]},
          open(R + 'manifest.webmanifest', 'w'), indent=2)
open(R + 'sw.js', 'w').write("""// Setlog %s: network first so updates arrive, cache when offline
var C = 'setlog-%s', FILES = ['./', 'index.html', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', function (e) { self.skipWaiting(); e.waitUntil(caches.open(C).then(function (c) { return c.addAll(FILES); })); });
self.addEventListener('activate', function (e) { e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== C; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); })); });
self.addEventListener('fetch', function (e) {
  var u = new URL(e.request.url); if (e.request.method !== 'GET' || u.origin !== location.origin) return;
  e.respondWith(fetch(e.request, { cache: 'no-cache' }).then(function (r) { var cp = r.clone(); caches.open(C).then(function (c) { c.put(e.request, cp); }); return r; }).catch(function () { return caches.match(e.request).then(function (m) { return m || caches.match('index.html'); }); }));
});
""" % (ver, ver))
print('built', ver)
