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
   - Cập nhật danh sách sách và số trang trong `sach/README.md`.
4. Commit (message dạng `<ten-sach>: trang NNN`) và push lên nhánh đang làm việc.
