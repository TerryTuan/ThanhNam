# Sổ tay đọc sách song ngữ (Anh / Trung → Việt)

Repo này là nơi lưu bản dịch và ghi chú khi người dùng đọc sách tiếng Anh và tiếng Trung.
Người dùng dán (copy) từng trang sách vào; Claude dịch, giải nghĩa và lưu lại theo thứ tự.

## Trình độ người dùng
- Tiếng Anh: IELTS 6.0 (~B2). Đã biết từ vựng thông dụng; cần giải thích từ học thuật, thành ngữ, cụm động từ, cấu trúc câu phức.
- Tiếng Trung: HSK 4. Đã biết ~1200 từ HSK1–4; cần giải thích từ HSK5 trở lên, thành ngữ (成语), văn viết (书面语), cấu trúc ngữ pháp nâng cao.
- Luôn trả lời và giải thích bằng **tiếng Việt**.

## Khi người dùng dán một trang sách
1. Xác định ngôn ngữ (Anh / Trung) và tên sách. Nếu chưa biết tên sách, hỏi một lần rồi dùng tiếp cho các trang sau.
2. Trả lời trong chat theo đúng mẫu trong `sach/MAU-TRANG.md`:
   - **Bản dịch tiếng Việt**: dịch tự nhiên, sát nghĩa, giữ đoạn văn như bản gốc.
   - **Từ vựng**: chỉ chọn từ *vượt trình độ* (8–15 từ/trang). Tiếng Anh: từ, phiên âm IPA, từ loại, nghĩa trong ngữ cảnh, ví dụ ngắn. Tiếng Trung: chữ Hán, pinyin, âm Hán Việt, cấp HSK (nếu có), nghĩa, ví dụ.
   - **Ngữ pháp**: 2–5 điểm ngữ pháp/cấu trúc đáng học trong trang, trích câu gốc, giải thích, cho 1 ví dụ mới.
   - **Câu khó**: phân tích 1–3 câu dài/khó nhất (tách mệnh đề, chỉ chủ ngữ – vị ngữ).
3. Lưu file (thư mục `sach/<ten-sach-khong-dau>/`, tên dùng chữ thường, gạch ngang):
   - `trang-NNN.md`: toàn bộ nội dung trang (bản gốc + dịch + từ vựng + ngữ pháp). NNN là số thứ tự tăng dần 001, 002, ... (không phải số trang in trong sách; ghi số trang thật vào tiêu đề nếu người dùng cho biết).
   - `ban-dich-tieng-viet.md`: **nối thêm** bản dịch tiếng Việt của trang vào cuối file, có tiêu đề `## Trang NNN`, để đọc liền mạch từ đầu đến cuối.
   - `tu-vung.md`: nối thêm từ vựng mới vào bảng tổng hợp (bỏ qua từ đã có).
   - `mau-cau.md`: nối thêm các mẫu câu/cấu trúc ngữ pháp của trang (cấu trúc, câu gốc, giải thích, ví dụ + bản dịch ví dụ).
   - `du-lieu.json`: thêm trang mới vào mảng `pages` (source, translation, note, vocab, patterns, hard) — đây là dữ liệu cho trang học. Mỗi từ vựng có trường `vi`: cụm tiếng Việt chép đúng y như trong bản dịch, để tô màu từ mới trong bản tiếng Việt.
   - Cập nhật danh sách sách và số trang trong `sach/README.md`.
4. Chạy `python3 tools/build.py` rồi xuất bản lại `app/so-tay.html` lên cùng artifact
   https://claude.ai/artifact/LQp55JRNdBsgjCH1c1DYPA (dùng tham số `url` nếu ở cuộc hội thoại khác).
   Trang học có 3 tab: Bản dịch · Từ vựng · Mẫu câu (danh sách + thẻ ghi nhớ).
5. Commit (message dạng `<ten-sach>: trang NNN`) và push lên nhánh đang làm việc.

## Trang thêm từ phần mềm (tab "+ Thêm")
Người dùng có thể tự dán chữ hoặc ảnh trang sách vào tab "+ Thêm" của trang học. Trang được dịch ngay trong phần mềm
và lưu vào cơ sở dữ liệu của artifact (collection `pages`, id `<ten-sach>-NNN`, cùng cấu trúc với một phần tử `pages` trong `du-lieu.json`, thêm trường `hard`).
Khi người dùng nhắc "đồng bộ", hoặc trước khi lưu một trang mới qua chat: đọc collection `pages` bằng ArtifactData,
chép các trang chưa có vào repo (trang-NNN.md, ban-dich-tieng-viet.md, tu-vung.md, mau-cau.md, du-lieu.json), build lại, xuất bản lại rồi commit.
Không xoá document trong db trừ khi người dùng yêu cầu (trang trong repo luôn được ưu tiên khi trùng số thứ tự).

## Nhiều cuốn sách
Mỗi cuốn có thư mục riêng `sach/<ten-sach-khong-dau>/` (cùng tên với `slug` của tên sách trong phần mềm: bỏ dấu, chữ thường, gạch ngang) và id `book` trong db trùng tên thư mục.
Số trang, từ vựng, mẫu câu, dấu "đã nhớ" và vị trí đọc Kindle đều tính riêng cho từng cuốn. Khi đồng bộ, trang nào thuộc `book` nào thì chép vào thư mục sách đó,
tạo `du-lieu.json` mới cho sách chưa có (id, title, original, author, lang, pages) và thêm dòng vào `sach/README.md`.

## Ý nghĩa sâu xa (trường `insight`)
Mỗi trang có thêm trường `insight`: 4–7 câu tiếng Việt giải thích ý chính, bối cảnh và điều đáng suy ngẫm của trang (chuỗi rỗng nếu không có gì sâu xa hơn nghĩa bề mặt; `insightDone: true` khi đã thử).
Phần mềm tự tạo sau từ vựng; khi trả lời trong chat cũng thêm mục "Ý nghĩa sâu xa" ở cuối, và lưu vào `trang-NNN.md` và `du-lieu.json`.

## Mức nhớ và trò chơi
Mỗi từ vựng/mẫu câu có mức nhớ 0–3 (lưu trong `lv`, đồng bộ cùng dấu "đã nhớ" trong db riêng của người dùng, không nằm trong repo).
Tab Từ vựng và Mẫu câu có chế độ "Trò chơi" (trắc nghiệm, điền từ, gõ từ; chọn mẫu, chọn công thức, sắp xếp câu). Đúng thì tăng mức, đạt 3 thì tự chuyển "Đã nhớ"; sai thì về 0.
Danh sách mặc định chỉ hiện mục "Cần nhớ", các mục đã nhớ nằm trong phần thu gọn. Vì vậy mỗi `ex` của từ vựng phải chứa đúng từ đó (để làm câu điền từ) và mỗi mẫu câu phải có `ex` đầy đủ, 4–14 từ (để làm câu sắp xếp).

## Ưu tiên từ hay gặp
Mỗi từ vựng có độ hay gặp (số lần xuất hiện trong bản gốc cả cuốn; mẫu câu: số trang dùng mẫu đó). Danh sách và thẻ ghi nhớ mặc định xếp hay gặp trước, trò chơi chọn mục theo điểm
hay gặp x mức nhớ còn thiếu. Vì vậy trường `w` của từ vựng nên là dạng gốc như trong sách; chú thích loại từ trong ngoặc làm giảm độ chính xác khi đếm.

## Ôn hôm nay, nghe và tra thêm từ
- Lịch ôn: mỗi mục có `due` (thời điểm ôn kế tiếp: mức 0 sau 5 phút, mức 1 sau 1 ngày, mức 2 sau 3 ngày, đã nhớ sau 7 ngày) và thống kê `daily` (số câu mỗi ngày, chuỗi ngày học). Cùng `lv` và dấu đã nhớ, chúng lưu trong db riêng của người dùng, không nằm trong repo.
  Nút "Ôn ngay" chơi các mục đến hạn trước, rồi mục cần nhớ điểm cao.
- Trò chơi có thêm câu "Nghe rồi chọn từ" (dùng giọng đọc của thiết bị).
- "Tra thêm từ khác" (tab Từ vựng) hỏi Claude nghĩa của từ bất kỳ rồi lưu vào collection `words` (id `<id-sách>__<slug-từ>`, trường book, w, ipa, pos, mean, ex). Từ thêm tay chỉ nằm trong db, hiển thị là "Thêm tay"; khi đồng bộ có thể chép vào `tu-vung.md` nếu người dùng muốn.

## Chạm vào từ để tra
Ở tab Bản dịch, tab + Thêm và chế độ Kindle (bật nút "Chạm để tra"), chạm vào bất kỳ từ nào trong bản gốc (đoạn `p[lang]`) thì phần mềm xác định từ và câu chứa nó:
nếu từ hoặc cụm đó đã có trong danh sách từ vựng (kể cả đã nhớ) thì mở giải nghĩa có sẵn, nếu chưa thì hỏi Claude nghĩa theo ngữ cảnh câu (kết quả được nhớ tạm trong phiên) và cho thêm vào collection `words` như mục "Tra thêm từ khác".

## Chẩn đoán lỗi
Khi gặp lỗi lúc hiển thị, phần mềm hiện khung "Có lỗi khi hiển thị" kèm nội dung lỗi và nút "Thử lại"; lỗi chạy ngầm hiện thành một dòng "Lỗi: …" ở đầu màn hình. Nếu người dùng báo "bị hỏng" mà chưa có ảnh chụp, hãy xin họ chụp màn hình dòng này.
Lựa chọn nhiễu trong trò chơi bỏ các mục cùng chữ, cùng gốc từ hoặc cùng nghĩa chính với đáp án; câu gõ từ chấp nhận từ khác có cùng nghĩa chính. Tài liệu đồng bộ `known` ghi gọn (mục đã nhớ ngầm hiểu mức 3, thống kê ngày giữ 120 ngày) để dưới 256 KiB.

## Dữ liệu từ claude.ai là chỉ-đọc
Dữ liệu đọc từ db (`snap.data()`, tài liệu `known` với `lv`, `due`, `daily`, các trang) bị đóng băng: gán vào đó bị bỏ qua âm thầm và gây lỗi kiểu "undefined is not an object (evaluating 'daily[dk].n')".
Luôn sao chép (hàm `thaw`) trước khi sửa; `ensureMutable()` chạy trước mọi lần ghi vào `lv`, `due`, `daily`. Khi thử bằng giả lập, tài liệu `known` trả về phải được `Object.freeze` sâu như trình xem thật.

## Xuất bản offline
`python3 tools/build.py --offline --seed <known.json>` tạo thêm `app/so-tay-offline.html`: một tệp HTML tự chứa (dữ liệu các sách từ `sach/*/du-lieu.json`, không dùng phông Google), mở được không cần mạng.
Bản offline đọc, ôn tập, chơi trò chơi và xem Kindle được; không có tab "+ Thêm", không dịch trang mới, chỉ tra được từ đã có trong danh sách. Tệp này được bỏ qua trong git (`.gitignore`).
Khi người dùng nhắc "xuất offline": đồng bộ db vào repo trước, đọc `data/users/me/known` bằng ArtifactData (out_dir) để làm `--seed` mang theo tiến độ học, build rồi gửi tệp bằng SendUserFile.

## Xuất EPUB (đọc offline trên iPhone)
`python3 tools/export_epub.py --seed <known.json>` tạo `app/<id-sách>.epub` cho từng cuốn: bản gốc và bản dịch xen kẽ, từ mới chưa nhớ được tô màu và chạm vào hiện nghĩa dạng chú thích bật lên (Apple Books, Kobo...), cuối mỗi trang có từ vựng, mẫu câu, câu khó và ý nghĩa sâu xa.
Tệp `.epub` bị bỏ qua trong git. Khi người dùng nhắc "xuất EPUB" hoặc cần đọc khi không có mạng: đồng bộ db vào repo, đọc `data/users/me/known` làm `--seed`, chạy lệnh trên rồi gửi tệp bằng SendUserFile (display "attach").

## Ứng dụng cài lên màn hình chính (PWA, chạy offline)
`python3 tools/build.py --pwa` tạo thư mục `docs/` (index.html, sw.js, manifest, biểu tượng): ứng dụng đầy đủ tính năng ôn tập, KHÔNG chứa nội dung sách. Phục vụ qua HTTPS (ví dụ GitHub Pages) thì mở bằng Safari, "Thêm vào Màn hình chính", rồi dùng offline như Kindle.
Dữ liệu sách và tiến độ nhập một lần từ tệp `sach-du-lieu.json` (`python3 tools/build.py --data-file app/sach-du-lieu.json --seed <known.json>`, tệp này chứa nguyên văn sách nên bị bỏ qua trong git và chỉ gửi riêng cho người dùng bằng SendUserFile) và lưu trong IndexedDB của thiết bị.
`python3 tools/build.py --offline` tạo tệp HTML tự chứa (đã gói đủ doctype và viewport để mở trên điện thoại).

## CẢNH BÁO quyền riêng tư
Ngày 2026-11-08 kiểm tra thấy repo `TerryTuan/ThanhNam` đang CÔNG KHAI nhưng chứa nguyên văn các trang sách người dùng đã dán (`sach/*/du-lieu.json`, `trang-NNN.md`...). Cho đến khi người dùng chuyển repo sang riêng tư hoặc quyết định khác:
không đưa thêm nguyên văn sách vào repo (khi "đồng bộ", chỉ chép bản dịch, từ vựng, mẫu câu nếu người dùng đồng ý), và không đưa nguyên văn sách vào bất kỳ thư mục nào được phục vụ công khai (như `docs/`).

## Bản dịch tiếng Việt đọc liền mạch
`tools/flow.js` (hàm `flowOf`) ghép bản dịch các trang thành một mạch như cuốn sách: bỏ phần hai trang chụp chồng lên nhau (phát hiện bằng bản gốc tiếng Anh rồi đối chiếu bản dịch), nối câu bị cắt đôi giữa hai trang (dấu "..."), không có tiêu đề trang.
`build.py` nhúng nó vào ứng dụng (nút "Liền mạch" ở tab Bản dịch và chế độ tiếng Việt của Kindle). `python3 tools/export_epub_vi.py [--data <thư mục chứa sach/*/du-lieu.json>]` xuất EPUB chỉ tiếng Việt cho từng cuốn (`app/<id>-tieng-viet.epub`, bỏ qua trong git).
Khi người dùng nhắc "xuất bản dịch tiếng Việt": lấy trang mới nhất từ db (ArtifactData, out_dir), gộp với `sach/` vào một thư mục tạm NGOÀI repo, chạy lệnh trên với `--data`, gửi tệp bằng SendUserFile; không chép nguyên văn sách mới vào repo (xem cảnh báo quyền riêng tư).

## Nhớ cuốn đang đọc và chống dán nhầm cuốn
`setBook(id)` là cách duy nhất đổi cuốn đang chọn: lưu `book` trong localStorage và trong db riêng của người dùng (tài liệu `data/users/<id>/prefs` với `book`, `at`), nên mở lại hay đổi thiết bị vẫn đúng cuốn cũ (`pullPrefs` khi mở và khi quay lại ứng dụng).
Tab + Thêm có khung "Trang mới sẽ lưu vào cuốn …"; dán trang giống một trang của cuốn khác thì cảnh báo "dán nhầm cuốn" (nút chuyển sang cuốn đó) trước khi lưu; trang vừa lưu có thể chuyển sang cuốn khác bằng nút "Chuyển trang này sang cuốn đó" (ghi trang vào cuốn đích với số trang kế tiếp rồi xoá bản cũ).

## Tự đọc khi chạm vào từ
Chạm vào từ tô màu (bản gốc, cụm tiếng Việt, Kindle) hoặc từ bất kỳ trong bản gốc thì đọc luôn từ tiếng Anh (`speakWordNow`, giọng của thiết bị, gọi ngay trong lần chạm vì iPhone chỉ cho phát âm khi có thao tác người dùng); từ tra bằng Claude trả về cụm khác thì đọc thêm cụm đó.
Có ô "Tự đọc" trong khung giải nghĩa để tắt/bật (lưu trong localStorage `autoSpeak`).

Sửa 2026-11: chỉ tự đọc TỪ MỚI (mục từ vựng chưa nhớ, tức từ được tô màu). Từ đã nhớ và từ thường chạm vào để tra thì không tự đọc (tránh đọc ngoài ý muốn khi chạm vào chữ); muốn nghe thì bấm nút Nghe. Ô "Tự đọc từ mới" tắt/bật được.

Sửa 2026-11 (lần 2): chạm vào từ thường mặc định KHÔNG làm gì (không mở khung, không gọi Claude), để khỏi cắt ngang lúc đọc. Chỉ từ tô màu (từ mới) phản hồi khi chạm. Ai cần tra từ bất kỳ thì bật nút "Tra từ thường" (`tapLookup`, lưu trong localStorage); chế độ Kindle có nút "Chạm để tra" riêng (`rdLookup`), mặc định tắt.

## Hình ảnh và bảng biểu
Khi dán ảnh chụp trang, ảnh được thu nhỏ (tối đa 2000 px, JPEG) và lưu bằng capability `assets` của artifact (chỉ chủ sổ tay), id ảnh nằm trong tài liệu trang: `img: {id, w, h}`; cờ `fig: true` khi trang có bảng/hình/biểu đồ.
Ảnh phục vụ qua `/_blob/<id>`, hiển thị gập lại ("Ảnh gốc của trang") ở tab Bản dịch, tab + Thêm và ở chế độ Liền mạch (chỉ trang có `fig`). Trang cũ chưa có ảnh dùng nút "Gắn ảnh gốc" để thêm sau.
Bảng được Claude chép thành bảng markdown (hàng `| a | b |`, dòng `|---|---|`) cả ở bản gốc lẫn bản dịch; hình được mô tả thành dòng `[Hình: ...]` / `[Figure: ...]`. Khối bảng giữ nguyên xuống dòng trong `source`/`translation`, `isTable`/`tableHTML`/`paraHTML` hiển thị thành bảng, `flow.js` không nối hay xoá bảng như văn xuôi, các tệp EPUB đổi thành thẻ `<table>`.
Chưa có: ảnh gốc trong EPUB, bản offline và PWA (chỉ tải được từ claude.ai); lấy ảnh bằng Artifact read với `path` là id asset nếu cần nhúng sau.

## Nút riêng "Dán trang mới" / "Về chỗ đang đọc"
Góc trái dưới (`#fab2`): nút "＋ Dán trang mới" (`goPaste`) nhảy tới ô dán ở tab + Thêm và đưa con trỏ vào đó; ở tab Thêm chỉ hiện khi đã cuộn xuống (khỏi phải cuộn ngược lên).
Nút "↩ Về chỗ đang đọc (trang N)" (`goRead`, chỉ ở tab Thêm) quay về tab Bản dịch đúng trang đang đọc. Chỗ đang đọc lưu theo từng cuốn trong localStorage (`pos`: `{id sách: {n, at}}`), cập nhật khi cuộn tab Bản dịch (`currentReadPage`), khôi phục khi vào lại tab, đổi cuốn hoặc mở lại ứng dụng (`state.restore`, `goRestore`).

## Bố cục gọn của tab + Thêm
Tab Thêm phải dán được ngay cả khi bàn phím iPhone đang mở: `body.addmode` ẩn hàng tên sách và cỡ chữ ở đầu trang, ô dán (`#draft`) nằm ngay dưới dòng "Lưu vào cuốn [chọn sách] · trang N", nút "Dán và dịch" / "Dịch" nằm dưới ô; ảnh chụp và số trang sách gom trong mục "Tuỳ chọn". `keepDraftVisible` cuộn để ô dán không bị bàn phím che (theo `visualViewport`).

## Nhớ trang đang đọc ở chế độ Kindle, ẩn nút dán khi chơi
Vị trí Kindle lưu theo mốc đoạn văn (`rdpos2`: `{id sách:ngôn ngữ: {i, f, at}}`, `anchorAt`), nên bền khi đổi cỡ chữ; chỉ lưu khi người đọc lật trang (bố cục dựng lại không ghi đè, `goPage(n, anim, save)`).
`store` giữ thêm bản sao trong bộ nhớ và các khoá `SYNCED` (`rdpos2`, `pos`, `tab`, `view`, `rdLang`, `rdSize`, `rs`) được đẩy lên db riêng (`data/users/<id>/prefs`: `book`, `at`, `reader`, `pos`, `ui`) sau 1,5 giây và khi ứng dụng bị ẩn; `pullPrefs` gộp từng mục theo `at` mới hơn, nên xoá localStorage hay đổi thiết bị vẫn đọc tiếp đúng chỗ.
Nút nổi `#fab2` (Dán trang mới / Về chỗ đang đọc) chỉ hiện ở tab Bản dịch và Thêm; tab Từ vựng, Mẫu câu (kể cả lúc chơi) không hiện.

Cỡ chữ (`rs`, nút A−/A+) áp cho cả `html` (`font-size: calc(16px * var(--rs))`) nên mọi đơn vị rem (ô dán, kết quả dịch, từ vựng, trò chơi) đều theo cùng một cỡ ở mọi tab, kể cả khi hàng nút cỡ chữ bị ẩn ở tab Thêm; `rs` được lưu và đồng bộ qua db riêng (xem mục trên).

Khung giải nghĩa (`.sheet`, `state.pop` / `state.tap`) đóng ngay khi chạm ra ngoài (vào vùng chữ hay nền, không phải nút, từ tô màu hay chính khung): bộ lắng nghe click pha capture ở trước `tapAt`, chặn lần chạm đó để không mở khung khác.

## Hình / đồ thị cắt riêng và hiện đúng chỗ
Khi dán ảnh trang có hình, Claude trả thêm `===FIGBOX===` (mỗi hình một dòng `x0 y0 x1 y1`, thang 0–1000, theo thứ tự các dòng `[Hình: ...]`); `parseBoxes` đổi thành `page.figBox = [{x, y, w, h}]` (tỉ lệ 0–1). `figCrop(p, i)` cắt đúng vùng hình từ ảnh trang đã lưu (`/_blob/<id>`, bằng CSS, không tạo ảnh mới) và hiện ngay dưới dòng `[Hình: ...]` ở tab Bản dịch (song ngữ, tiếng Việt, liền mạch), kết quả tab Thêm và Kindle. Chữ trong hình không dịch.
Trang cũ có ảnh nhưng chưa có `figBox`: nút "Cắt hình ra khỏi ảnh trang" (`locateFigs`) nhờ Claude tìm vùng hình rồi lưu; trong lúc chưa cắt, ảnh gốc của trang tự mở sẵn thay vì gập lại. Trang không có ảnh gốc thì không có hình để hiện (dùng "Gắn ảnh gốc"). Chưa có trong bản offline/PWA/EPUB.

Trang cũ có ảnh gốc, có dòng `[Hình: ...]` nhưng chưa có `figBox` được cắt tự động (`autoLocate`, lần lượt từng trang, mỗi trang thử một lần mỗi phiên, chỉ chủ sổ tay); ảnh gốc cả trang vẫn gập lại (không tự mở, vì ảnh trắng cao làm trống cả màn hình khi chưa tải xong).

## Chụp sách giấy trong phần mềm (không lưu vào Thư viện ảnh)
Tab + Thêm có nút "📷 Chụp trang sách" (`openCamera`, cần `sample` có `images`): mở khung xem trực tiếp bằng camera sau (`getUserMedia`, lớp phủ `#cam`), bấm "Chụp" lấy một khung hình thành `File` trong bộ nhớ trang (`state.file`) rồi dịch ngay nếu bật "Tự dịch ngay khi dán"; ảnh không đi qua Thư viện ảnh của điện thoại.
Nếu khung nhúng của claude.ai không cho dùng camera thì dùng ô chọn ảnh có `capture="environment"` và nhắc người dùng. Ảnh trang vẫn được lưu trong kho `assets` của sổ tay (không phải Thư viện ảnh) để xem lại hình/bảng; muốn bỏ ảnh thì nút "Bỏ ảnh" trước khi dịch.

## Bìa sách
Mỗi cuốn có thể có ảnh bìa: collection `books`, id = id sách, `{cover: {id, w, h, box?}, at}` (`id` là ảnh trong kho `assets`, `box` là khung bìa `{x, y, w, h}` tỉ lệ 0–1 do Claude tìm trong ảnh chụp; không có box thì dùng cả ảnh). Ở tab + Thêm, mục "Tuỳ chọn" có "📘 Chụp bìa sách" (dùng camera trong phần mềm, `openCamera(saveCover)`, không lưu vào Thư viện ảnh) và "Chọn ảnh bìa".
`coverHTML` cắt bìa bằng CSS; hiện thẻ sách (bìa + tên + tác giả, `bookCard`) ở đầu tab Bản dịch và làm trang đầu của chế độ Kindle (`readerHTML`, `.rd-cover`). Chưa có trong bản offline/PWA/EPUB (ảnh chỉ tải được từ claude.ai); thêm bìa làm các mốc `rdpos2.i` của Kindle lệch một khối một lần.

Ảnh gửi cho Claude (`sample`) luôn qua `shrinkFile` (tối đa 1600 px, JPEG 0.8): ảnh chụp thẳng từ camera rất lớn làm lời gọi bị từ chối với lỗi "invalid_request" (không dịch được). Ảnh lưu vào `assets` vẫn tối đa 2000 px (`packImage`).

Dịch ảnh bị `invalid_request` / `image_rejected` thì tự thử lại một lần với ảnh nhỏ hơn (1100 px, JPEG 0.7); thông báo lỗi hiện thêm `message` và kích cỡ/định dạng ảnh để chẩn đoán (nhờ người dùng chụp màn hình dòng này).

Kiểm tra đủ chữ khi dịch ảnh (`completeFromImage`): sau lần dịch đầu, hỏi Claude lần hai xem phần cuối trang (đoạn cuối, tiêu đề, trích dẫn) có còn thiếu không; thiếu thì nối thêm vào `source`/`translation` (và bỏ dấu "..." dừng dở). Lần kiểm tra lỗi thì giữ bản dịch đã có. Lời nhắc dịch cũng yêu cầu chép TOÀN BỘ chữ đến cuối trang. Trang cũ bị thiếu thì sửa trực tiếp trong db (`ArtifactData update`).
