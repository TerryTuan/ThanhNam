"""Xuất mỗi cuốn thành EPUB chỉ có bản dịch tiếng Việt, đọc liền mạch như một cuốn sách (không cần mạng: Apple Books, Kobo...).

  python3 tools/export_epub_vi.py [--out thư_mục] [--data thư_mục_chứa_sach]

Văn bản lấy từ tools/flow.js (qua Node): bỏ chỗ hai trang chụp chồng lên nhau, nối câu bị cắt đôi giữa hai trang,
không có tiêu đề trang trong thân sách; mục lục chia theo cụm 10 trang.
"""
import json
import subprocess
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parent.parent
argv = sys.argv[1:]
out_dir = Path(argv[argv.index("--out") + 1]) if "--out" in argv else root / "app"
data_root = Path(argv[argv.index("--data") + 1]) if "--data" in argv else root  # thư mục chứa sach/*/du-lieu.json (mặc định: repo)

CSS = """
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.7; margin: 0 5%; }
h1 { font-size: 1.4em; margin: 1.4em 0 .8em; }
p { margin: 0; text-indent: 1.4em; text-align: justify; }
p.first { text-indent: 0; }
"""
XHTML_HEAD = ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
              '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="vi" xml:lang="vi">')


def x(t):
    return escape(str(t if t is not None else ""), quote=False)


def write_epub(book, jf, path, group=10):
    flow = json.loads(subprocess.run(["node", str(root / "tools/flow_cli.js"), str(jf)], capture_output=True, text=True, check=True).stdout)
    order = []
    for para in flow:
        for n in para["pages"]:
            if n not in order:
                order.append(n)
    chunks = [order[i:i + group] for i in range(0, len(order), group)]
    chunk_of = {n: ci for ci, c in enumerate(chunks) for n in c}
    bodies, seen, anchor_chunk = [[] for _ in chunks], set(), {}
    for para in flow:
        ci = chunk_of[para["pages"][0]]
        anchors = ""
        for n in para["pages"]:
            if n not in seen:
                seen.add(n)
                anchors += f'<span id="p{n:03d}"></span>'
                anchor_chunk[n] = ci  # mốc trang nằm trong tệp của đoạn chứa nó (đoạn nối từ trang trước có thể kéo mốc sang tệp trước)
        cls = ' class="first"' if not bodies[ci] else ""
        bodies[ci].append(f"<p{cls}>{anchors}{x(para['t'])}</p>")
    keep = [ci for ci in range(len(chunks)) if bodies[ci]]  # bỏ phần trống nếu mọi trang của nó đã nối vào phần trước
    fname_of = {ci: f"v{k + 1:02d}.xhtml" for k, ci in enumerate(keep)}
    files, nav = [], []
    for k, ci in enumerate(keep):
        c = chunks[ci]
        label = f"Phần {k + 1} (trang {c[0]:03d}–{c[-1]:03d})"
        target = anchor_chunk.get(c[0], ci)
        nav.append((label, f"{fname_of.get(target, fname_of[ci])}#p{c[0]:03d}"))
        files.append((fname_of[ci], XHTML_HEAD + f'<head><meta charset="utf-8"/><title>{x(label)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>'
                      f'<body><h1>{x(label)}</h1>\n' + "\n".join(bodies[ci]) + "\n</body></html>"))
    ident = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "so-tay-vi/" + book["id"]))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = "".join(f'<item id="{f[:-6]}" href="{f}" media-type="application/xhtml+xml"/>' for f, _ in files)
    spine = "".join(f'<itemref idref="{f[:-6]}"/>' for f, _ in files)
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           f'<dc:identifier id="uid">{ident}</dc:identifier><dc:title>{x(book["title"])} (bản dịch tiếng Việt)</dc:title>\n'
           f'<dc:creator>{x(book.get("author") or "Sổ tay đọc sách")}</dc:creator><dc:language>vi</dc:language><meta property="dcterms:modified">{now}</meta></metadata>\n'
           '<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/>'
           f'{manifest}</manifest>\n<spine>{spine}</spine></package>')
    navx = (XHTML_HEAD + '<head><meta charset="utf-8"/><title>Mục lục</title></head><body><nav epub:type="toc" id="toc"><h1>Mục lục</h1><ol>'
            + "".join(f'<li><a href="{h}">{x(t)}</a></li>' for t, h in nav) + "</ol></nav></body></html>")
    container = ('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
                 '<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)  # phải đứng đầu, không nén
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", navx, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        for f, content in files:
            z.writestr("OEBPS/" + f, content, compress_type=zipfile.ZIP_DEFLATED)
    return len(flow), len(files), len(order)


for jf in sorted(data_root.glob("sach/*/du-lieu.json")):
    book = json.loads(jf.read_text(encoding="utf-8"))
    target = out_dir / f"{book['id']}-tieng-viet.epub"
    nparas, nfiles, npages = write_epub(book, jf, target)
    print(f"{target}: {npages} trang -> {nparas} đoạn liền mạch, {nfiles} phần, {target.stat().st_size // 1024} KB")
