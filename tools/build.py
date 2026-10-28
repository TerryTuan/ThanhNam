"""Ghép dữ liệu tất cả các sách (sach/*/du-lieu.json) vào app/template.html -> app/so-tay.html."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
books = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(root.glob("sach/*/du-lieu.json"))]
data = json.dumps(books, ensure_ascii=False).replace("</", "<\\/")
html = (root / "app/template.html").read_text(encoding="utf-8").replace("/*__DATA__*/[]", data)
(root / "app/so-tay.html").write_text(html, encoding="utf-8")
print(f"app/so-tay.html: {len(books)} sách, {sum(len(b['pages']) for b in books)} trang")
