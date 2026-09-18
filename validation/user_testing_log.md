# Nhật ký thử nghiệm người dùng — R6 (CP5)

## Trạng thái: HOÀN THÀNH MỘT PHẦN (2/5)

Nhóm thử được **2 người** (cả hai đều thuộc danh sách willing users đăng ký từ CP1) trước hạn CP5, chưa đạt mức tối thiểu 5 người theo yêu cầu R6 — tự khai báo trung thực thay vì bịa thêm cho đủ số.

## Cách làm (nguyên tắc Mom Test)
1. Đưa cho người thử **một nhiệm vụ cụ thể**, không giải thích trước sản phẩm làm gì.
2. **Im lặng quan sát** — không gợi ý, không giải thích khi họ bị vướng.
3. Ghi lại **đúng chỗ họ khựng lại** và **trích nguyên văn câu họ nói** lúc gặp khó.
4. Không hỏi câu xã giao kiểu "bạn thấy sản phẩm thế nào?" — chỉ quan sát hành vi thật.

**Nhiệm vụ gợi ý cho người thử** (gõ vào `node codebase/classify.mjs --lecture day04`, không giải thích trước):
> "Đây là một tutor AI cho một bài giảng. Bạn hãy hỏi nó một câu như thể bạn đang học và không hiểu điều gì đó trong bài — bất kỳ câu gì bạn muốn."

Cần tối thiểu **5 người**, trong đó **≥2 người thuộc danh sách willing users** đã đăng ký ở CP1 (Cường, Đoan).

## Bảng ghi nhận

| # | Người thử | Có phải willing user? | Nhiệm vụ giao | Điểm tắc nghẽn | Trích dẫn nguyên văn | Quyết định xử lý của nhóm |
|---|---|---|---|---|---|---|
| 1 | Cường | Có | Gõ `node codebase/classify.mjs --lecture day04`, sau đó hỏi tutor AI một câu về bài giảng mà bản thân chưa hiểu. | Không biết nên hỏi câu gì vì chưa rõ tutor có thể trả lời đến mức nào. | "Mình không biết hỏi kiểu gì, cứ tưởng phải hỏi đúng nội dung trong bài." | Giữ nguyên thiết kế nhiệm vụ; bổ sung ví dụ câu hỏi mẫu trong hướng dẫn để người dùng hiểu có thể hỏi bất kỳ câu gì liên quan đến bài. |
| 2 | Đoan | Có | Gõ `node codebase/classify.mjs --lecture day04`, sau đó hỏi tutor AI một câu về bài giảng mà bản thân chưa hiểu. | Mất thời gian đọc toàn bộ output trước khi tìm ra phần trả lời chính. | "Có hơi nhiều chữ, mình không biết phần nào là câu trả lời chính." | Đổi thứ tự in kết quả trong CLI: đưa câu trả lời/kết luận lên đầu, phần lý do giải thích xuống sau — đã sửa trong `codebase/classify.mjs` (xem §9 spec.md). |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

## Tổng hợp thay đổi từ phản hồi
- **Đã sửa**: thứ tự hiển thị kết quả trong `codebase/classify.mjs` — trả lời/kết luận hiện lên trước, lý do xuống dưới (theo phản hồi của Đoan).
- **Chưa sửa, ghi nhận cho vòng sau**: bổ sung câu hỏi mẫu trong hướng dẫn sử dụng cho người mới (theo phản hồi của Cường) — chưa có tài liệu hướng dẫn riêng ở mốc này.
- **Còn thiếu**: 3/5 người thử theo yêu cầu tối thiểu — chưa thực hiện được trước hạn CP5.
