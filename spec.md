# AI SPEC — [Tên lát cắt] · Nhóm [HelloWorld] · Zone [2]
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tối ưu tính năng có sẵn  [ ] Tính năng mới

## §1. User & Job
- Job executor + workflow: học viên đang tự học trên VLearn, bôi đen một đoạn slide/transcript và hỏi tutor để hiểu hoặc xác nhận lại nội dung.
- Core JTBD: khi đọc tài liệu mà chưa chắc mình hiểu đúng, muốn hỏi ngay tại chỗ và được dẫn dắt tới đúng phần cần xem, thay vì tự đoán hoặc bỏ qua.
- Problem statement: khi không khớp được đoạn hỏi với nội dung tài liệu, tutor báo "không tìm thấy" rồi dừng, không giúp học viên diễn đạt lại đúng chỗ cần hỏi — học viên phải tự đoán từ khoá khác hoặc bỏ dở.
- Evidence (mining `data/tutor_turns.csv`, script + log đầy đủ ở `evidence/mine_not_found.py|.log`):
  - n = 13.494 lượt hỏi–đáp thật, 1.617 học viên (22/07–15/09/2026), sau khi tách 22,7% câu bấm sẵn.
  - Bộ nhận diện "không tìm thấy" (siết, chấm tay ~85–94% đúng, xem log §1): **9,1%** lượt (1.223/13.494) là tutor báo không tra được nội dung, chạm **526/1.617 học viên**. Loại ngày 30/07 (một buổi hoạt động trên lớp, đột biến) còn **4,5%**.
  - Không phải lỗi ngẫu nhiên: sau một lượt "không tìm thấy", lượt hỏi tiếp theo của cùng học viên lại trượt tiếp **33,0%**, so với **7,4%** sau một lượt trả lời bình thường (gấp ~4,5 lần) — cho thấy học viên loay hoay chứ không tự sửa được.
  - 85,3% các lượt trượt là câu hỏi neo theo số trang/slide cụ thể ("trang 26", "slide 9") — đúng kiểu câu VLearn khuyến khích (bôi đen rồi hỏi), không phải câu hỏi vu vơ.
  - 5 quote nguyên văn (tutor trả lời, học viên chấm `down`, log xác nhận trong `evidence/mine_not_found.log`):
    - T00185: "Rất tiếc, tôi không tìm thấy nội dung cụ thể nào tại trang 37... Bạn có thể cho biết thêm về chủ đề hoặc khái niệm mà bạn đang muốn tìm hiểu tại đó không?"
    - T00362: "Xin lỗi bạn, vì hệ thống slide hiện tại không có dữ liệu cho 'slide 26' nên tôi không thể giải thích nội dung cụ thể đó..."
    - T00636: "Rất tiếc, tôi đã tra cứu trong tài liệu ngày học nhưng không tìm thấy thông tin cụ thể tại trang 43..."
    - T00758: "Xin lỗi bạn, nội dung tài liệu tôi nhận được không bao gồm trang 32. Hiện tại tôi chỉ có thể truy cập được các trang khác..."
    - T00451: "Rất tiếc, tôi không thể truy cập trực tiếp vào tệp PDF của buổi học để tóm tắt cho bạn..."

## §2. Impact & quyết định chọn
| Ứng viên | Bao nhiêu người | Tần suất | Tốn gì mỗi lần | Khả thi |
|---|---|---|---|---|
| **Tutor "không tìm thấy" rồi dừng** | 526/1.617 học viên (32,5%) | 9,1% lượt hỏi (4,5% sau khi bỏ ngày 30/07) | Học viên loay hoay, 33% khả năng lượt tiếp theo lại trượt | Cao — sửa được bằng một câu hỏi lại có mục tiêu, không cần đổi hạ tầng retrieval |
| Câu trả lời không trích dẫn nguồn (`has_citation=False`) | 933 học viên (28,0% lượt) | 28,0% lượt | Học viên không tự kiểm chứng được câu trả lời | Trung bình — cần thay đổi prompt/format trích dẫn, không rõ học viên có thực sự cần |
| Tutor luôn dùng một nước đi sư phạm (`review_concept`, 89,9% lượt) | 1.565/1.617 học viên | 89,9% lượt | Có thể học viên không được dẫn dắt đa dạng, nhưng chưa có bằng chứng học viên bị hại | Thấp — quá rộng, không phải "một quyết định AI" rõ ràng, khó đo pass/fail |

- Ứng viên ĐÃ LOẠI:
  - **Không trích dẫn nguồn**: tỉ lệ cao nhưng không có tín hiệu hệ quả rõ (rating quá thưa để so downstream); rủi ro chọn nhầm việc "trông có vẻ AI hơn" chứ không chắc là nỗi đau thật.
  - **Chỉ dùng một nước đi sư phạm**: phủ gần như toàn bộ log nên không tách được thành một lát cắt cụ thể, không có ngưỡng pass/fail rõ để làm golden set.
  - Có cân nhắc quy vấn đề về lỗi retrieval (5 tài liệu chiếm 53,2% số lượt "không tìm thấy" trong nhóm tài liệu ≥100 lượt) nhưng đó là vấn đề hạ tầng lập chỉ mục, ngoài phạm vi một lát cắt hội thoại — không chọn.
- Ứng viên CHỌN: **tutor phải hỏi lại khi không tìm thấy nội dung, thay vì xin lỗi rồi dừng.** Vì: chạm 1/3 học viên, có bằng chứng hệ quả đo được (trượt lặp gấp 4,5 lần), phần lớn (85,3%) rơi vào đúng thao tác lõi VLearn khuyến khích (bôi đen đoạn cụ thể), và sửa nằm gọn trong tầm một lát cắt hội thoại (một quyết định AI: hỏi lại có mục tiêu) chứ không đòi build lại retrieval.

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU: **[Học viên đang tự học trên VLearn] cần [hỏi về một đoạn/trang tài liệu cụ thể không khớp được với nội dung có sẵn] được [gợi ý 2–3 đoạn/trang gần đúng nhất để chọn thay vì báo "không tìm thấy" rồi dừng] giúp [học viên tiếp tục được đúng mạch, không phải tự đoán từ khoá khác hay bỏ dở].**
  - Lý do chọn đúng chỗ này: 50% lượt "không tìm thấy" hiện đã kết bằng một câu hỏi, nhưng không cải thiện rõ tỉ lệ gỡ được (63,8% vs 70,4% khi không hỏi) — vấn đề không phải "có hỏi lại hay không" mà là câu hỏi lại **không neo vào gì cụ thể**. 85,3% lượt trượt là câu hỏi neo theo số trang/slide, nên hệ thống thường có sẵn top-k đoạn gần đúng để gợi ý thay vì hỏi mở.
- Non-goals (KHÔNG build ở lát cắt này):
  - Không sửa retrieval/indexing (5 tài liệu chiếm 53,2% số lượt trượt trong log — đây là lỗi hạ tầng, đã loại ở §2).
  - Không tự "đoán" và trả lời khi không đủ căn cứ, kể cả khi có gợi ý gần đúng nhưng độ tin cậy thấp.
  - Không xử lý case "hỏi ngoài phạm vi tài liệu" (nhánh ③ ở §6) — khác cơ chế với "không khớp được vì diễn đạt mơ hồ".
  - Không đổi UI bấm câu mẫu hay cơ chế rating của VLearn.
- Mức prototype nhắm tới: [ ] Sketch [x] Mock [ ] Working — mock giao diện chọn gợi ý (2–3 trang/đoạn gần đúng); logic chọn gợi ý và sinh câu hỏi lại chạy thật trên golden set trích từ `data/tutor_turns.csv`.
- Automation: [ ] augment [x] conditional [ ] automate — cost-of-error hai chiều: tự trả lời khi không chắc → học viên tin sai kiến thức; hỏi lại tràn lan khi thực ra tìm được → gây phiền. Nên có điều kiện: dưới ngưỡng tin cậy rõ ràng mới hỏi lại có gợi ý, trên ngưỡng thì trả lời kèm trích dẫn như bình thường.
- §4b. Nguyên tắc đã áp dụng (HAX):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | G1 — Làm rõ hệ thống làm được gì | Khi không có gợi ý nào đủ gần, nói rõ phạm vi tài liệu đang có (VD: "mình chỉ có nội dung Day 04") thay vì im lặng đoán |
  | G4 — Hiển thị thông tin đúng ngữ cảnh | Câu hỏi lại liệt kê top-k đoạn/trang gần đúng nhất tìm được, dùng chính ngữ cảnh trang học viên đang mở |
  | G9 — Hỗ trợ sửa nhanh, ít thao tác | Học viên bấm chọn 1 trong các gợi ý thay vì phải gõ lại từ khoá từ đầu |
  | G11 — Giải thích vì sao hệ thống làm vậy | Khi trả lời "không có căn cứ", nói rõ đã tra ở đâu/phạm vi nào để học viên biết giới hạn thật, không nghĩ là lỗi ngẫu nhiên |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- **Happy path**: câu hỏi neo rõ vào một trang/đoạn (VD "Trang 15 nói cấu trúc prompt gồm phần nào?") khớp đủ tin cậy với tài liệu → tutor trả lời thẳng, kèm trích dẫn `[trang N]`, không cần hỏi lại.
- **Low-confidence (②)**: câu hỏi ngắn/mơ hồ (VD "phạm vi ở phần này là sao vậy") khớp một phần với ≥2 trang → tutor không đoán bừa, không hỏi mở chung chung, mà liệt kê 2–3 trang/đoạn gần đúng nhất để học viên bấm chọn (đúng cơ chế đã build ở prototype `Đúng Trang`).
- **Failure/không có căn cứ (①)**: câu hỏi không khớp từ khoá nào của buổi học (VD hỏi cách deploy Docker trong buổi Prompt Engineering) → tutor nói rõ đã tra nhưng không thấy, nêu tên buổi học đang có, không bịa nội dung.
- **Correction (user sửa)**: học viên từ chối hết các gợi ý hoặc gõ lại câu hỏi cụ thể hơn sau khi tutor gợi ý sai hướng → hệ thống coi là câu hỏi mới, phân loại lại từ đầu, không lặp lại đúng bộ gợi ý cũ.
- **Khi bị đòi ngoài phạm vi (③)**: học viên hỏi thứ ngoài nội dung khoá học (nhờ làm hộ bài tập, hỏi ý kiến cá nhân ngoài bài giảng) → tutor từ chối lịch sự, nói rõ phạm vi hỗ trợ; tách biệt với case "không khớp vì diễn đạt mơ hồ" ở trên (đã ghi rõ là non-goal của lát cắt này ở §4).
- **Case đặc thù domain (④)**: câu hỏi neo đúng số trang nhưng số trang trên VLearn lệch với số trang tài liệu gốc (hiện tượng thấy trong log thật, VD hỏi "trang 26" mà hệ thống đánh số khác) → tutor không chỉ báo "không có trang 26", mà gợi ý theo tiêu đề/nội dung gần nhất, tránh học viên tưởng mình hỏi sai.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |