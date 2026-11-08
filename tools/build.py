"""Ghép dữ liệu các sách (sach/*/du-lieu.json) vào app/template.html.
  python3 tools/build.py                          -> app/so-tay.html (bản trực tuyến, xuất bản lên claude.ai)
  python3 tools/build.py --offline [--seed k.json] -> thêm app/so-tay-offline.html: một tệp HTML tự chứa, có cả sách (mang theo tiến độ nếu có --seed)
  python3 tools/build.py --pwa                    -> docs/: ứng dụng cài lên màn hình chính, chạy offline, KHÔNG chứa nội dung sách (index.html, sw.js, manifest, biểu tượng)
  python3 tools/build.py --data-file out.json [--seed k.json]
                                                  -> tệp dữ liệu (sách + tiến độ) để nhập vào ứng dụng PWA một lần
--seed: tệp JSON tài liệu `known` của người dùng (keys, lv, due, daily, at).
"""
import json
import sys
from datetime import date
from pathlib import Path

root = Path(__file__).resolve().parent.parent
argv = sys.argv[1:]
arg = lambda name: argv[argv.index(name) + 1] if name in argv else None
books = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(root.glob("sach/*/du-lieu.json"))]
js = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
data = js(books)
tpl = (root / "app/template.html").read_text(encoding="utf-8")
seed_obj = None
if arg("--seed"):
    d = json.loads(Path(arg("--seed")).read_text(encoding="utf-8"))
    d = d.get("data", d)
    seed_obj = {k: d[k] for k in ("keys", "lv", "due", "daily", "at") if k in d}

RESET = """<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>"""


def standalone(html, head_extra=""):
    """Gói thành tài liệu HTML đầy đủ (doctype, viewport...) để mở như một trang độc lập; claude.ai tự làm việc này cho bản trực tuyến."""
    cut = html.index("<header>")
    return ('<!doctype html>\n<html lang="vi"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            + RESET + head_extra + html[:cut] + "</head><body>\n" + html[cut:] + "\n</body></html>\n")


def no_google_fonts(html):
    # Không có mạng: bỏ liên kết phông Google, CSS đã khai báo phông hệ thống thay thế.
    return "\n".join(l for l in html.split("\n") if "fonts.googleapis.com" not in l and 'rel="preconnect"' not in l)


(root / "app/so-tay.html").write_text(tpl.replace("/*__DATA__*/[]", data), encoding="utf-8")
print(f"app/so-tay.html: {len(books)} sách, {sum(len(b['pages']) for b in books)} trang")

if "--offline" in argv:
    off = (tpl.replace("/*__DATA__*/[]", data).replace("/*__OFFLINE__*/false", "true").replace("/*__BUILT__*/", date.today().isoformat())
           .replace("/*__SEED__*/null", js(seed_obj) if seed_obj else "null")
           .replace("<title>Sổ tay đọc sách</title>", "<title>Sổ tay đọc sách (offline)</title>"))
    off = standalone(no_google_fonts(off))
    (root / "app/so-tay-offline.html").write_text(off, encoding="utf-8")
    print(f"app/so-tay-offline.html: {len(off) // 1024} KB, tiến độ mang theo: {'có' if seed_obj else 'không'}")

if "--pwa" in argv:
    stamp = date.today().strftime("%Y%m%d") + "-" + str(abs(hash(tpl)) % 10**6)
    pwa = tpl.replace("/*__PWA__*/false", "true").replace("/*__BUILT__*/", date.today().isoformat())
    extra = ('<meta name="theme-color" content="#1f6f8b"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
             '<meta name="apple-mobile-web-app-title" content="Sổ tay"><meta name="apple-mobile-web-app-status-bar-style" content="default">'
             '<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png">')
    out = root / "docs"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(standalone(no_google_fonts(pwa), extra), encoding="utf-8")
    (out / "manifest.webmanifest").write_text(json.dumps({
        "name": "Sổ tay đọc sách", "short_name": "Sổ tay", "lang": "vi", "start_url": "./", "scope": "./", "display": "standalone",
        "background_color": "#eef2f5", "theme_color": "#1f6f8b",
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
        ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "sw.js").write_text(f"""// Service worker: lưu mã ứng dụng để mở được khi không có mạng. Dữ liệu sách nằm trong IndexedDB của thiết bị, không đi qua đây.
const CACHE = "so-tay-{stamp}";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {{
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, {{ ignoreSearch: true }}).then(hit => hit || fetch(e.request).then(r => {{
    const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r;
  }}).catch(() => caches.match("index.html"))));
}});
""", encoding="utf-8")
    print(f"docs/: ứng dụng PWA ({(out / 'index.html').stat().st_size // 1024} KB, không chứa nội dung sách), cache {stamp}")

if arg("--data-file"):
    payload = {"format": "so-tay-du-lieu", "built": date.today().isoformat(), "books": books}
    if seed_obj:
        payload["progress"] = seed_obj
    Path(arg("--data-file")).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"{arg('--data-file')}: {len(books)} sách, tiến độ: {'có' if seed_obj else 'không'}")
