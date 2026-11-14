// Ghép bản dịch tiếng Việt của các trang thành một mạch đọc liền như một cuốn sách.
// Dùng chung cho ứng dụng (build.py chèn vào template ở dấu /*__FLOW__*/) và cho tệp xuất (tools/export_epub.js qua Node).
//   flowOf(pages) -> [{ t: "đoạn văn", pages: [n, ...], terms }] ; pages là mảng trang có source[] và translation[].
// Hai việc xử lý ở chỗ nối giữa hai trang:
//  1) Trang chụp chồng lên nhau (cuối trang trước trùng đầu trang sau): bỏ các câu bị lặp ở trang sau, có đối chiếu bản dịch để chắc chắn.
//  2) Câu bị cắt đôi giữa hai trang (dấu "..."): nối hai nửa lại thành một đoạn.
(function (root) {
  const ELL_END = /\s*(\.\.\.|…)\s*$/, ELL_START = /^\s*(\.\.\.|…)\s*/;
  const wordsOf = t => (String(t).toLowerCase().replace(/[’]/g, "'").match(/[\p{L}\p{N}']+/gu) || []);

  // Số từ tiếng Anh mà hậu tố của trang trước trùng tiền tố của trang sau (tối thiểu 4 từ), 0 nếu không chồng.
  function overlapWords(prevSrc, nextSrc) {
    const a = wordsOf((prevSrc || []).join(" ")), b = wordsOf((nextSrc || []).join(" "));
    for (let n = Math.min(a.length, b.length, 200); n >= 4; n--) {
      let ok = true;
      for (let i = 0; i < n; i++) if (a[a.length - n + i] !== b[i]) { ok = false; break; }
      if (ok) return n;
    }
    return 0;
  }
  // Trong n từ đầu của trang sau: có bao nhiêu câu trọn vẹn, và phần chồng có kết thúc giữa một câu (partial) hay không.
  function headInfo(nextSrc, n) {
    const text = (nextSrc || []).join(" ").replace(ELL_START, ""); let count = 0, end = 0;
    for (const m of text.matchAll(/[\p{L}\p{N}']+/gu)) { if (++count === n) { end = m.index + m[0].length; break; } }
    if (!end) return { n: 0, partial: false };
    const tailPunct = (text.slice(end).match(/^[.!?…"”')\]]*/) || [""])[0], head = text.slice(0, end) + tailPunct;
    const rest = text.slice(end + tailPunct.length);
    return { n: (head.match(/[.!?…](?=["”')\]]*(\s|$))/g) || []).length, partial: !/[.!?…]["”')\]]*$/.test(head) && /\S/.test(rest) };
  }
  // Tách câu tiếng Việt: sau . ! ? … rồi khoảng trắng và chữ hoa/chữ số/mở ngoặc kép.
  const splitSentences = p => String(p).split(/(?<=[.!?…]["”')\]]*)\s+(?=["“(]?[\p{Lu}0-9])/u).map(s => s.trim()).filter(Boolean);
  const jaccard = (x, y) => { const a = new Set(wordsOf(x)), b = new Set(wordsOf(y)); let i = 0; a.forEach(w => { if (b.has(w)) i++; }); return a.size + b.size - i ? i / (a.size + b.size - i) : 0; };

  function dropLeadingSentences(paras, n) {
    const out = []; let left = n;
    for (const p of paras) {
      if (left <= 0) { out.push(p); continue; }
      const ss = splitSentences(left === n ? p.replace(ELL_START, "") : p);
      if (ss.length <= left) { left -= ss.length; continue; }
      out.push(ss.slice(left).join(" ")); left = 0;
    }
    return out;
  }

  function flowOf(pages) {
    const list = (pages || []).filter(p => p && Array.isArray(p.translation) && p.translation.some(t => String(t).trim()));
    const out = []; let prev = null;
    list.forEach((p, idx) => {
      let mergeNext = false;
      let paras = p.translation.map(t => String(t).trim()).filter(Boolean);
      if (prev) {
        // 1) bỏ phần chồng lặp
        const k = overlapWords(prev.source, p.source);
        if (k) {
          const { n, partial } = headInfo(p.source, k);
          const prevS = splitSentences(prev.translation.map(t => String(t).trim()).filter(Boolean).join(" "));
          const nextS = splitSentences(paras.join(" ").replace(ELL_START, ""));
          if (n > 0 && jaccard(prevS.slice(-n).join(" "), nextS.slice(0, n).join(" ")) >= 0.3) paras = dropLeadingSentences(paras, n);
          // Phần chồng dừng giữa câu: bản dịch cuối trang trước là nửa câu, trang sau có câu đầy đủ -> bỏ nửa câu, giữ câu đầy đủ.
          const lastOut = out[out.length - 1], truncated = prevS[prevS.length - 1], full = nextS[n];
          if (partial && lastOut && truncated && full && jaccard(truncated, full) >= 0.25) {
            const ss = splitSentences(lastOut.t);
            if (ss.length > 1) { lastOut.t = ss.slice(0, -1).join(" "); mergeNext = true; } else out.pop(); // câu đầy đủ nối tiếp ngay đoạn cũ
          }
        }
      }
      if (!paras.length) { prev = p; return; }
      // 2) nối câu bị cắt đôi
      const last = out[out.length - 1];
      if (last && prev) {
        const aOpen = ELL_END.test(last.t), first = paras[0], bCont = ELL_START.test(first);
        const rest = first.replace(ELL_START, ""), bLower = /^\p{Ll}/u.test(rest);
        const aEndsSentence = /[.!?"”)\]]\s*$/.test(last.t);
        if (mergeNext || (aOpen && (bCont || bLower)) || (bCont && bLower && !aEndsSentence)) {
          last.t = last.t.replace(ELL_END, "") + " " + rest;
          if (!last.pages.includes(p.n)) last.pages.push(p.n);
          paras = paras.slice(1);
        }
      }
      paras.forEach(t => out.push({ t, pages: [p.n] }));
      prev = p;
    });
    if (out.length) out[0].t = out[0].t.replace(ELL_START, ""); // đầu sách: bỏ dấu "..." mở đầu
    return out;
  }

  const api = { flowOf, overlapWords, headInfo, splitSentences };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.FLOW = api;
})(typeof window !== "undefined" ? window : globalThis);
