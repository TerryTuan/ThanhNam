"""Ghép dữ liệu các sách (sach/*/du-lieu.json) vào app/template.html.
  python3 tools/build.py                      -> app/so-tay.html (bản trực tuyến, xuất bản lên claude.ai)
  python3 tools/build.py --offline [--seed known.json]
                                              -> thêm app/so-tay-offline.html: một tệp HTML tự chứa, mở được không cần mạng.
  --seed: tệp JSON tài liệu `known` của người dùng (keys, lv, due, daily, at) để mang theo tiến độ học vào bản offline.
"""
import json
import sys
from datetime import date
from pathlib import Path

root = Path(__file__).resolve().parent.parent
books = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(root.glob("sach/*/du-lieu.json"))]
data = json.dumps(books, ensure_ascii=False).replace("</", "<\\/")
tpl = (root / "app/template.html").read_text(encoding="utf-8")
online = tpl.replace("/*__DATA__*/[]", data)
(root / "app/so-tay.html").write_text(online, encoding="utf-8")
print(f"app/so-tay.html: {len(books)} sách, {sum(len(b['pages']) for b in books)} trang")

if "--offline" in sys.argv:
    seed = "null"
    if "--seed" in sys.argv:
        d = json.loads(Path(sys.argv[sys.argv.index("--seed") + 1]).read_text(encoding="utf-8"))
        d = d.get("data", d)
        seed = json.dumps({k: d[k] for k in ("keys", "lv", "due", "daily", "at") if k in d}, ensure_ascii=False).replace("</", "<\\/")
    off = (tpl.replace("/*__DATA__*/[]", data).replace("/*__OFFLINE__*/false", "true")
           .replace("/*__BUILT__*/", date.today().isoformat()).replace("/*__SEED__*/null", seed)
           .replace("<title>Sổ tay đọc sách</title>", "<title>Sổ tay đọc sách (offline)</title>"))
    # Bỏ liên kết phông chữ Google (không có mạng): dùng phông hệ thống đã khai báo trong CSS.
    off = "\n".join(l for l in off.split("\n") if "fonts.googleapis.com" not in l and "rel=\"preconnect\"" not in l)
    (root / "app/so-tay-offline.html").write_text(off, encoding="utf-8")
    print(f"app/so-tay-offline.html: {len(off) // 1024} KB, tiến độ mang theo: {'có' if seed != 'null' else 'không'}")
