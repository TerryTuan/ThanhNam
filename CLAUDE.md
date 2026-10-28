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

## Trang thêm từ phần mềm (tab "+ Thêm trang")
Người dùng có thể tự dán chữ hoặc ảnh trang sách vào tab "+ Thêm trang" của trang học. Trang được dịch ngay trong phần mềm
và lưu vào cơ sở dữ liệu của artifact (collection `pages`, id `<ten-sach>-NNN`, cùng cấu trúc với một phần tử `pages` trong `du-lieu.json`, thêm trường `hard`).
Khi người dùng nhắc "đồng bộ", hoặc trước khi lưu một trang mới qua chat: đọc collection `pages` bằng ArtifactData,
chép các trang chưa có vào repo (trang-NNN.md, ban-dich-tieng-viet.md, tu-vung.md, mau-cau.md, du-lieu.json), build lại, xuất bản lại rồi commit.
Không xoá document trong db trừ khi người dùng yêu cầu (trang trong repo luôn được ưu tiên khi trùng số thứ tự).

## Nhiều cuốn sách
Mỗi cuốn có thư mục riêng `sach/<ten-sach-khong-dau>/` (cùng tên với `slug` của tên sách trong phần mềm: bỏ dấu, chữ thường, gạch ngang) và id `book` trong db trùng tên thư mục.
Số trang, từ vựng, mẫu câu, dấu "đã nhớ" và vị trí đọc Kindle đều tính riêng cho từng cuốn. Khi đồng bộ, trang nào thuộc `book` nào thì chép vào thư mục sách đó,
tạo `du-lieu.json` mới cho sách chưa có (id, title, original, author, lang, pages) và thêm dòng vào `sach/README.md`.
