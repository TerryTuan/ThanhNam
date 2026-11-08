"""Xuất mỗi cuốn sách (sach/*/du-lieu.json) thành một tệp EPUB đọc được khi không có mạng (Apple Books, Kobo, Google Play Books...).

  python3 tools/export_epub.py [--seed known.json] [--out thư_mục]

Trong EPUB: bản gốc và bản dịch xen kẽ từng đoạn; từ mới chưa nhớ trong bản gốc được tô màu và chạm vào sẽ hiện nghĩa
(chú thích bật lên, "pop-up footnote"); cuối mỗi trang có từ vựng, mẫu câu, câu khó và ý nghĩa sâu xa.
--seed: tài liệu `known` của người dùng (keys, ...) để không tô màu các từ đã nhớ.
"""
import json
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parent.parent
argv = sys.argv[1:]
seed_path = argv[argv.index("--seed") + 1] if "--seed" in argv else None
out_dir = Path(argv[argv.index("--out") + 1]) if "--out" in argv else root / "app"
known = set()
if seed_path:
    d = json.loads(Path(seed_path).read_text(encoding="utf-8"))
    known = set((d.get("data", d)).get("keys", []))

CSS = """
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.55; margin: 0 4%; }
h1 { font-size: 1.5em; margin: 1.2em 0 .4em; }
h2 { font-size: 1.15em; margin: 1.6em 0 .5em; border-top: 1px solid #8884; padding-top: .6em; }
h3 { font-size: .8em; letter-spacing: .08em; text-transform: uppercase; margin: 1.2em 0 .3em; opacity: .7; }
p { margin: 0 0 .7em; }
p.src { opacity: .72; }
p.vi { margin-bottom: 1.1em; }
a.nw { color: #9a4a00; background: #fbe9cf55; border-bottom: 1px dotted #9a4a00; text-decoration: none; }
aside { display: none; }
p.v { margin: 0 0 .8em; }
.ipa { font-family: 'Helvetica Neue', Arial, sans-serif; opacity: .7; font-size: .9em; }
.pos { font-size: .8em; color: #1f6f8b; }
.ex { font-style: italic; opacity: .75; }
.formula { font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: bold; color: #1f6f8b; }
.note { font-size: .88em; opacity: .75; border-left: 2px solid #8886; padding-left: .6em; }
.insight p { border-left: 2px solid #1f6f8b; padding-left: .7em; }
"""


def forms(t):
    lw = t.lower()
    if len(lw) <= 2:
        return [lw]
    if len(lw) == 3:
        return [lw, lw + "s", lw + "es"]
    f = {lw, lw + "s", lw + "es", lw + "ed", lw + "d", lw + "ing", lw + "ly", lw + "er", lw + "est"}
    last = lw[-1]
    if last == "e":
        f |= {lw[:-1] + "ing", lw + "r", lw + "st"}
    if last == "y" and not re.search("[aeiou]y$", lw):
        f |= {lw[:-1] + x for x in ("ies", "ied", "ier", "iest", "ily")}
    if re.search(r"[^aeiou][aeiou][^aeiouwxy]$", lw):
        f |= {lw + last + x for x in ("ed", "ing", "er")}
    return sorted(f, key=len, reverse=True)


def word_regex(w):
    clean = re.sub(r"\s*\([^)]*\)", "", w).strip() or w
    parts = ["(?:" + "|".join(re.escape(x) for x in forms(t)) + ")" for t in clean.split()]
    return re.compile(r"(?<![\w])" + r"\s+".join(parts) + r"(?![\w])", re.I)


def x(t):
    return escape(str(t if t is not None else ""), quote=False)


def vocab_of(book):
    seen, out = set(), []
    for p in book["pages"]:
        for v in p.get("vocab") or []:
            w = v.get("w")
            if isinstance(w, str) and w.strip() and w not in seen:
                seen.add(w)
                out.append({**v, "key": f"{book['id']}|tu-vung|{w}", "re": word_regex(w)})
    return out


def build_book(book):
    vocab = [v for v in vocab_of(book) if v["key"] not in known]
    pages_per_file = 8
    files, nav_items = [], []
    note_id = 0
    for gi in range(0, len(book["pages"]), pages_per_file):
        group = book["pages"][gi:gi + pages_per_file]
        fname = f"c{gi // pages_per_file + 1:02d}.xhtml"
        body = []
        for p in group:
            pid = f"p{p['n']:03d}"
            label = f"Trang {p['n']:03d}" + (f" (trang sách {p['label']})" if p.get("label") else "")
            nav_items.append((label, f"{fname}#{pid}"))
            body.append(f'<h2 id="{pid}">{x(label)}</h2>')
            src, vi = p.get("source") or [], p.get("translation") or []
            used = set()
            for i in range(max(len(src), len(vi))):
                if i < len(src):
                    text, hits = src[i], []
                    for v in vocab:
                        if v["key"] in used:
                            continue
                        m = v["re"].search(text)
                        if m:
                            hits.append((m.start(), m.end(), v))
                    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
                    out, pos = [], 0
                    for a, z, v in hits:
                        if a < pos:
                            continue
                        note_id += 1
                        nid = f"n{note_id}"
                        used.add(v["key"])
                        out.append(x(text[pos:a]))
                        out.append(f'<a class="nw" epub:type="noteref" role="doc-noteref" href="#{nid}">{x(text[a:z])}</a>')
                        pos = z
                        v["_nid"] = nid
                        body.append(
                            f'<aside epub:type="footnote" role="doc-footnote" id="{nid}"><p><b>{x(v["w"])}</b> '
                            f'<span class="ipa">{x(v.get("ipa", ""))}</span> <i>{x(v.get("pos", ""))}</i><br/>{x(v.get("mean", ""))}'
                            + (f'<br/><span class="ex">{x(v.get("ex", ""))}</span>' if v.get("ex") else "") + "</p></aside>"
                        )
                    out.append(x(text[pos:]))
                    body.append(f'<p class="src" lang="en">{"".join(out)}</p>')
                if i < len(vi):
                    body.append(f'<p class="vi">{x(vi[i])}</p>')
            if p.get("note"):
                body.append(f'<p class="note">{x(p["note"])}</p>')
            pv = [v for v in p.get("vocab") or [] if isinstance(v, dict) and v.get("w")]
            if pv:
                body.append("<h3>Từ vựng</h3>")
                for v in pv:
                    mark = " ✓" if f"{book['id']}|tu-vung|{v['w']}" in known else ""
                    body.append(f'<p class="v"><b>{x(v["w"])}</b>{mark} <span class="ipa">{x(v.get("ipa", ""))}</span> <span class="pos">{x(v.get("pos", ""))}</span><br/>{x(v.get("mean", ""))}'
                                + (f'<br/><span class="ex">{x(v["ex"])}</span>' if v.get("ex") else "") + "</p>")
            if p.get("patterns"):
                body.append("<h3>Mẫu câu</h3>")
                for q in p["patterns"]:
                    body.append(f'<p class="v"><b>{x(q.get("name", ""))}</b><br/><span class="formula">{x(q.get("formula", ""))}</span><br/>{x(q.get("explain", ""))}'
                                f'<br/><span class="ex">{x(q.get("ex", ""))}</span> — {x(q.get("exVi", ""))}</p>')
            if p.get("hard"):
                body.append("<h3>Câu khó</h3>")
                for h in p["hard"]:
                    body.append(f'<p class="v"><span class="ex">{x(h.get("s", ""))}</span><br/>{x(h.get("parts", ""))}<br/>{x(h.get("mean", ""))}</p>')
            if p.get("insight"):
                body.append('<h3>Ý nghĩa sâu xa</h3><div class="insight">'
                            + "".join(f"<p>{x(t)}</p>" for t in re.split(r"(?:\n|\\n)+", p["insight"]) if t.strip()) + "</div>")
        title = f"{group[0]['n']:03d}–{group[-1]['n']:03d}"
        files.append((fname, f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="vi" xml:lang="vi">
<head><meta charset="utf-8"/><title>Trang {title}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
{chr(10).join(body)}
</body></html>'''))
    return files, nav_items


def write_epub(book, path):
    files, nav_items = build_book(book)
    author = book.get("author") or "Sổ tay đọc sách"
    ident = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "so-tay/" + book["id"]))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = "".join(f'<item id="{f[:-6]}" href="{f}" media-type="application/xhtml+xml"/>' for f, _ in files)
    spine = "".join(f'<itemref idref="{f[:-6]}"/>' for f, _ in files)
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">{ident}</dc:identifier><dc:title>{x(book["title"])} (song ngữ)</dc:title>
<dc:creator>{x(author)}</dc:creator><dc:language>vi</dc:language><meta property="dcterms:modified">{now}</meta></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/>{manifest}</manifest>
<spine>{spine}</spine></package>'''
    nav = ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="vi" xml:lang="vi">'
           '<head><meta charset="utf-8"/><title>Mục lục</title></head><body><nav epub:type="toc" id="toc"><h1>Mục lục</h1><ol>'
           + "".join(f'<li><a href="{h}">{x(t)}</a></li>' for t, h in nav_items) + "</ol></nav></body></html>")
    container = '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)  # phải đứng đầu, không nén
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        for f, content in files:
            z.writestr("OEBPS/" + f, content, compress_type=zipfile.ZIP_DEFLATED)
    return len(files), len(nav_items)


for jf in sorted(root.glob("sach/*/du-lieu.json")):
    book = json.loads(jf.read_text(encoding="utf-8"))
    target = out_dir / f"{book['id']}.epub"
    nfiles, npages = write_epub(book, target)
    print(f"{target}: {npages} trang, {nfiles} tệp nội dung, {target.stat().st_size // 1024} KB")
