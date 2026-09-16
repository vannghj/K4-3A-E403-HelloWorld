# Kết quả chạy Golden Set — Lượt 1

**Ngày chạy**: xem `ran_at` trong `eval/run1_raw.json`. **Đường gọi model**: `claude_cli` (không có `ANTHROPIC_API_KEY` trong môi trường chạy lượt này — module tự fallback sang CLI `claude -p` của phiên Claude Code đã đăng nhập sẵn trên máy). Toàn bộ 20 lượt gọi là lệnh gọi LLM thật, không có phản hồi gán cứng — xem log đầy đủ (prompt gửi đi + phản hồi thô) trong `eval/call_log.jsonl`, đối chiếu từng dòng với `case_id`.

## Kết quả tổng

**12/20 ĐẠT (60,0%)**

Nhãn `expected_tier` trong `eval/golden_set.json` được chốt và commit **trước khi chạy** (commit riêng, xem lịch sử git) — không sửa sau khi thấy kết quả.

## Bảng chi tiết

| Ca | Lớp | Nguồn | Kỳ vọng | Thực tế | Kết quả |
|---|---|---|---|---|---|
| C1 | ① | tự tạo | found / tr.15 | found / tr.15 | ĐẠT |
| C2 | ① | T00636 | notfound | notfound | ĐẠT |
| C3 | ② | tự tạo | clarify | clarify | ĐẠT |
| C4 | ② | T12536 | notfound | notfound | ĐẠT |
| C5 | ③ | T00224 | out_of_scope | out_of_scope | ĐẠT |
| C6 | ③ | T12523 | out_of_scope | out_of_scope | ĐẠT |
| C7 | ④ | tự tạo | found / tr.15 | notfound | **TRƯỢT** |
| C8 | ④ | T00758 | notfound | notfound | ĐẠT |
| P1 | ① | tự tạo | found / tr.24 | found / tr.24 | ĐẠT |
| P2 | ① | tự tạo | found / tr.14 | found / tr.14 | ĐẠT |
| P3 | ① | T00881 | found / tr.22 | found / tr.22 | ĐẠT |
| P4 | ② | T00692 | notfound | clarify | **TRƯỢT** |
| P5 | ① | tự tạo | found / tr.31 | found / tr.31 | ĐẠT |
| P6 | ① | T11866 | found / tr.31 | notfound | **TRƯỢT** |
| P7 | ① | tự tạo | found / tr.30 | found / tr.30 | ĐẠT |
| P8 | ② | T00107 | notfound | clarify | **TRƯỢT** |
| P9 | ② | T01411 | notfound | clarify | **TRƯỢT** |
| H1 | ② | T00185 | notfound | out_of_scope | **TRƯỢT** |
| H2 | ② | tự tạo | notfound | out_of_scope | **TRƯỢT** |
| H3 | ② | tự tạo | found / tr.14 | clarify | **TRƯỢT** |

## Phân tích 8 ca trượt — không làm đẹp, nói thẳng nguyên nhân

Đọc kỹ `reason` model trả về (log đầy đủ trong `call_log.jsonl`) thì 8 ca trượt chia làm 3 nhóm nguyên nhân **rất khác nhau về mức độ nghiêm trọng** — không phải cả 8 đều là "model sai".

### Nhóm A — Nhãn kỳ vọng của mình đặt quá khắt khe, model thực ra xử lý hợp lý (5 ca: P4, P6, P8, P9, H3)

Đây là nhóm nghiêm trọng nhất về mặt phương pháp: golden set được gán nhãn dựa trên trực giác + heuristic đếm từ khoá kiểu cũ (từ prototype `dung-trang.html`), nhưng model thật áp dụng chuẩn "có căn cứ" **chặt hơn** dự đoán:

- **P6** — hỏi con số cụ thể "2tr vs 500" của OpenAI API. Trang 31 chỉ nói khái niệm context window chung, không có con số đó. Model từ chối trả lời thay vì suy diễn — **đây chính xác là hành vi "không bịa" mà §1 của spec đang đòi hỏi**. Nhãn `found` của mình sai, không phải model sai.
- **P8, P9** — câu hỏi "tóm tắt toàn bộ buổi học" / "trang này" quá mơ hồ để chọn 1 trang. Model chọn `clarify` (mời học viên chọn trong nhiều trang) thay vì từ chối thẳng — đây là hành vi tốt hơn `notfound`, không tệ hơn.
- **P4, H3** — model phát hiện chồng lấn ngữ nghĩa hợp lý giữa nhiều trang mà nhãn ban đầu không tính tới (VD H3 nhắc cả "vòng lặp" lẫn "thought/action" nên khớp cả trang 6 lẫn trang 14, không chỉ trang 14 như mình giả định).

**Kết luận nhóm A**: không sửa nhãn của lượt 1 (đã chốt trước khi chạy), nhưng golden set v2 nên gán lại các nhãn này thành `clarify` thay vì `notfound`/`found`.

### Nhóm B — Ranh giới mơ hồ giữa `notfound` và `out_of_scope` cho input vô nghĩa (2 ca: H1, H2)

Câu hỏi "r" và câu hỏi rỗng: model gọi là `out_of_scope` ("không phải câu hỏi rõ ràng về bài giảng"), mình kỳ vọng `notfound`. Đây là lỗi thiết kế prompt thật: `codebase/classify.mjs` mô tả `out_of_scope` là "câu hỏi không phải về nội dung bài giảng" — input rỗng/vô nghĩa khớp cả hai mô tả một cách hợp lý, prompt chưa phân biệt rõ "hỏi sai chủ đề" với "hỏi không đủ thông tin để hiểu là gì". **Đây là điểm cần sửa prompt** trước khi chạy lượt 2.

### Nhóm C — Model over-anchor vào số trang literal, bỏ qua nội dung khớp (1 ca: C7)

Ca thiết kế riêng để kiểm tra "④ đặc thù nghiệp vụ" (VLearn đánh số trang lệch PDF gốc): câu hỏi nêu sai số trang ("trang 26") nhưng có đủ từ khoá nội dung đúng ("ràng buộc", "định dạng") để nhận ra là trang 15. Model bám chặt vào việc "không có trang 26 trong danh sách" và từ chối, **không tận dụng nội dung khớp để vượt qua số trang sai**. Đây là **phát hiện quan trọng nhất của lượt chạy này**: đúng thứ mining ở §1/§2 chỉ ra (85,3% lượt trượt thật là câu hỏi neo theo số trang) — model hiện tại **chưa giải quyết được đúng vấn đề cốt lõi** khi số trang sai nhưng nội dung đúng. Cần sửa prompt: yêu cầu model ưu tiên khớp nội dung, chỉ dùng số trang làm gợi ý phụ chứ không phải điều kiện loại trừ.

## Việc cần làm trước lượt chạy tiếp theo
1. Sửa prompt trong `classify.mjs`: tách rõ `out_of_scope` (sai chủ đề) khỏi `notfound` (đúng chủ đề, thiếu thông tin để trả lời/để hiểu câu hỏi); thêm hướng dẫn rõ "ưu tiên khớp nội dung hơn số trang nêu trong câu hỏi".
2. Xem lại 5 nhãn ở nhóm A cho golden set v2 — không sửa ngược nhãn lượt 1 này.
3. Ca C7 (nhóm C) là bằng chứng mạnh nhất nên đưa vào demo/video: cho thấy rõ khoảng cách giữa "đã có LLM thật" và "đã giải quyết đúng vấn đề mining chỉ ra".
