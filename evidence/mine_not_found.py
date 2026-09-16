#!/usr/bin/env python3
"""
Mining bằng chứng cho §1/§2 của spec — lát cắt "tutor không tra được nội dung".

Chạy:  python3 evidence/mine_not_found.py > evidence/mine_not_found.log
Nguồn: data/tutor_turns.csv (13.494 lượt, 22/07→15/09/2026). Chỉ đọc, không sửa dữ liệu.
data/ không được đẩy lên repo công khai (xem .gitignore) — chỉ script + log này ở lại.

Hai bộ nhận diện:
  LOOSE  — bắt cả lời xin lỗi xã giao. Độ chính xác chấm tay 33/35 = 94% trên tập gộp,
           nhưng chỉ ~2/12 trên khoá K4 vì câu trả lời K4 dài và lịch sự hơn. KHÔNG dùng để báo số.
  STRICT — đòi câu nói rõ là không tra được nội dung; loại câu từ chối vì ngoài phạm vi
           (đếm riêng) và loại bẫy "không chỉ … mà còn". Đây là bộ dùng để báo số.
           Độ chính xác chấm tay: 17/20 (85%) trên K3, 11/20 (55%) trên K4.
"""
import csv, re, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime

csv.field_size_limit(10**9)
CSV = "data/tutor_turns.csv"

STRICT = re.compile(
    r"(không tìm thấy (nội dung|thông tin|slide|trang|kết quả|dữ liệu|tài liệu|bất kỳ|gì)"
    r"|không tìm được (nội dung|thông tin|slide|trang)"
    r"|(không|chưa) thể (truy xuất|truy cập|tra cứu|tìm thấy|hiển thị)"
    r"|(tài liệu|slide|bài giảng|hệ thống|nội dung)[^.?!]{0,40}không (có|chứa|bao gồm|hiển thị|ghi nhận|đề cập)"
    r"|không có (thông tin|nội dung|dữ liệu|slide|trang|kết quả)[^.?!]{0,30}(nào|cụ thể|chi tiết|về|cho|trong|tại|liên quan)"
    r"|(không|chưa) (được )?đề cập (đến|tới|chi tiết|cụ thể)"
    r"|hệ thống (không|chưa) (tìm|trả về|ghi nhận)"
    r"|kết quả (tìm kiếm|tra cứu)[^.?!]{0,30}không)", re.I)
NEG   = re.compile(r"không chỉ[^.?!]{0,60}mà còn", re.I)
SCOPE = re.compile(r"(nằm ngoài phạm vi|ngoài phạm vi (hỗ trợ|nội dung|bài học|khóa|khoá)"
                   r"|không thuộc phạm vi|chỉ (hỗ trợ|tập trung)[^.?!]{0,40}(nội dung|bài học|khóa|khoá))", re.I)
PAGE  = re.compile(r"(trang|slide)\s*\d+", re.I)

def tf(v): return str(v).strip().lower() == "true"
def dt(s): return datetime.strptime(s, "%Y-%m-%d %H:%M")

rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
for r in rows:
    t = r["tutor_reply"] or ""
    r["_dt"]    = dt(r["asked_at_vn"])
    r["_scope"] = bool(SCOPE.search(t))
    r["_nf"]    = bool(STRICT.search(t)) and not NEG.search(t) and not r["_scope"]
    r["_q"]     = "?" in t                       # câu trả lời có hỏi ngược lại không
    r["_page"]  = bool(PAGE.search(r["student_question"] or ""))

def hdr(s): print(f"\n{'='*78}\n{s}\n{'='*78}")

hdr("0 · TOÀN CẢNH")
print(f"lượt {len(rows)} | học viên {len(set(r['student'] for r in rows))} | "
      f"{min(r['asked_at_vn'] for r in rows)} → {max(r['asked_at_vn'] for r in rows)}")
print(f"câu bấm sẵn {sum(1 for r in rows if tf(r['is_preset']))} "
      f"({100*sum(1 for r in rows if tf(r['is_preset']))/len(rows):.1f}%)")
print("move_used:", Counter(r["move_used"] for r in rows).most_common())
print("rating:", Counter(r["rating"] for r in rows).most_common())
print(f"không trích dẫn: {sum(1 for r in rows if not tf(r['has_citation']))} "
      f"({100*sum(1 for r in rows if not tf(r['has_citation']))/len(rows):.1f}%)")

hdr("1 · TỈ LỆ NOT_FOUND THEO TỪNG LÁT (bộ STRICT)")
def rate(sub, name):
    if not sub: return
    nf = [r for r in sub if r["_nf"]]; sc = [r for r in sub if r["_scope"]]
    hv = len(set(r["student"] for r in nf)); hvt = len(set(r["student"] for r in sub))
    print(f"{name:24s} n={len(sub):6d} | NOT_FOUND {len(nf):5d} ({100*len(nf)/len(sub):5.1f}%)"
          f" | ngoài phạm vi {len(sc):4d} ({100*len(sc)/len(sub):4.1f}%)"
          f" | học viên chạm {hv:4d}/{hvt}")
rate(rows, "TẤT CẢ")
rate([r for r in rows if r["cohort_hint"] == "K4"], "K4 (khoá hiện tại)")
rate([r for r in rows if r["cohort_hint"] == "K3"], "K3 (khoá trước)")
rate([r for r in rows if r["asked_at_vn"][:10] != "2026-07-30"], "BỎ ngày 30/07")
rate([r for r in rows if r["asked_at_vn"][:10] == "2026-07-30"], "CHỈ ngày 30/07")

hdr("2 · TUTOR CÓ HỎI NGƯỢC LẠI KHÔNG, VÀ HỎI CÓ GỠ ĐƯỢC KHÔNG")
print("Ghi chú nhân quả: hai nhóm KHÔNG so sánh được trực tiếp — tutor hỏi lại đúng vào")
print("những câu vốn mơ hồ hơn. Chỉ kết luận 'hỏi lại không cải thiện', không nói 'kém hơn'.")
def recover(sub, name, gap=30):
    by = defaultdict(list)
    for r in sub: by[r["student"]].append(r)
    for s in by: by[s].sort(key=lambda r: r["_dt"])
    c = defaultdict(Counter)
    for s, lst in by.items():
        for i, r in enumerate(lst):
            if not r["_nf"]: continue
            k = "NF + có hỏi lại" if r["_q"] else "NF + ngõ cụt"
            c[k]["tổng"] += 1
            nxt = lst[i+1] if i+1 < len(lst) and (lst[i+1]["_dt"]-r["_dt"]).total_seconds()/60 <= gap else None
            if nxt:
                c[k]["hỏi tiếp"] += 1
                c[k]["gỡ được" if not nxt["_nf"] else "lại trượt"] += 1
            else:
                c[k]["dừng phiên"] += 1
    print(f"\n-- {name} --")
    for k, v in sorted(c.items()):
        t, ht = v["tổng"], max(v["hỏi tiếp"], 1)
        print(f"   {k:18s} n={t:5d} | dừng phiên {v['dừng phiên']:4d} ({100*v['dừng phiên']/max(t,1):4.1f}%)"
              f" | hỏi tiếp {v['hỏi tiếp']:4d} → gỡ được {v['gỡ được']:4d} ({100*v['gỡ được']/ht:4.1f}%)"
              f", lại trượt {v['lại trượt']:4d} ({100*v['lại trượt']/ht:4.1f}%)")
recover(rows, "TẤT CẢ"); recover([r for r in rows if r["cohort_hint"]=="K4"], "K4")
recover([r for r in rows if r["asked_at_vn"][:10]!="2026-07-30"], "BỎ ngày 30/07")

hdr("3 · TÁI PHÁT: SAU MỘT LƯỢT TRƯỢT THÌ LƯỢT SAU CÓ TRƯỢT TIẾP KHÔNG")
def relapse(sub, name, gap=30):
    by = defaultdict(list)
    for r in sub: by[r["student"]].append(r)
    for s in by: by[s].sort(key=lambda r: r["_dt"])
    c = Counter()
    for s, lst in by.items():
        for i, r in enumerate(lst):
            if i+1 >= len(lst) or (lst[i+1]["_dt"]-r["_dt"]).total_seconds()/60 > gap: continue
            k = "NF" if r["_nf"] else "OK"
            c[k+"_cont"] += 1
            if lst[i+1]["_nf"]: c[k+"_again"] += 1
    print(f"{name:16s} sau NF: {c['NF_again']}/{c['NF_cont']} ({100*c['NF_again']/max(c['NF_cont'],1):.1f}%)"
          f" | sau lượt thường: {c['OK_again']}/{c['OK_cont']} ({100*c['OK_again']/max(c['OK_cont'],1):.1f}%)")
relapse(rows, "TẤT CẢ"); relapse([r for r in rows if r["cohort_hint"]=="K4"], "K4")
relapse([r for r in rows if r["asked_at_vn"][:10]!="2026-07-30"], "BỎ 30/07")

hdr("4 · CO CỤM THEO TÀI LIỆU — kiểm tra nhiễu do một vài bộ slide không index được")
g = defaultdict(list)
for r in rows: g[(r["course_id"], r["lecture_code"])].append(r)
st = sorted([(k, len(v), sum(1 for x in v if x["_nf"])) for k, v in g.items() if len(v) >= 100],
            key=lambda x: -x[2]/x[1])
for k, n, f in st[:6]:  print(f"   cao nhất  {k[0]:22s} {k[1]:4s} n={n:5d} NF={f:4d} ({100*f/n:5.1f}%)")
for k, n, f in st[-4:]: print(f"   thấp nhất {k[0]:22s} {k[1]:4s} n={n:5d} NF={f:4d} ({100*f/n:5.1f}%)")
tot, tfq = sum(n for _, n, _ in st), sum(f for _, _, f in st)
top5 = sorted(st, key=lambda x: -x[2])[:5]
print(f"   {len(st)} tài liệu (n>=100) phủ {tot} lượt, NF {tfq} ({100*tfq/tot:.1f}%);"
      f" 5 tài liệu nhiều NF nhất chiếm {sum(f for _,_,f in top5)}/{tfq} = {100*sum(f for _,_,f in top5)/tfq:.1f}% số NF")

hdr("5 · CÂU HỎI NEO THEO SỐ TRANG")
for sub, nm in [(rows, "TẤT CẢ"), ([r for r in rows if r["cohort_hint"]=="K4"], "K4")]:
    s_nf = [r for r in sub if r["_nf"]]; s_pg = [r for r in sub if r["_page"]]
    if not s_nf: continue
    print(f"{nm:8s} NF có 'trang/slide N': {sum(1 for r in s_nf if r['_page'])}/{len(s_nf)}"
          f" ({100*sum(1 for r in s_nf if r['_page'])/len(s_nf):.1f}%)"
          f" | tỉ lệ trượt khi hỏi theo số trang {100*sum(1 for r in s_pg if r['_nf'])/max(len(s_pg),1):.1f}%"
          f" vs nền {100*len(s_nf)/len(sub):.1f}%")

hdr("6 · ỨNG VIÊN KHÁC, ĐO TRÊN K4 (khoá đang chạy)")
K4 = [r for r in rows if r["cohort_hint"] == "K4"]
for name, sel in [("không trích dẫn", lambda r: not tf(r["has_citation"])),
                  ("câu bấm sẵn",     lambda r: tf(r["is_preset"])),
                  ("chỉ review_concept", lambda r: r["move_used"] == "review_concept"),
                  ("grade_missing",   lambda r: tf(r["grade_missing"]))]:
    s = [r for r in K4 if sel(r)]
    print(f"   {name:20s} {len(s):5d} ({100*len(s)/len(K4):5.1f}%) | học viên {len(set(r['student'] for r in s)):4d}/448")
ms = sorted(int(r["reply_ms"]) for r in K4 if r["reply_ms"].isdigit())
print(f"   reply_ms K4: median {statistics.median(ms):.0f} p90 {ms[int(.9*len(ms))]} p99 {ms[int(.99*len(ms))]}"
      f" | >10s: {sum(1 for x in ms if x>10000)} ({100*sum(1 for x in ms if x>10000)/len(ms):.1f}%)")
by = defaultdict(list)
for r in K4: by[r["student"]].append(r)
for s in by: by[s].sort(key=lambda r: r["_dt"])
rep = tot2 = 0
for s, lst in by.items():
    for i in range(len(lst)-1):
        if (lst[i+1]["_dt"]-lst[i]["_dt"]).total_seconds()/60 > 30: continue
        tot2 += 1
        a = set(re.findall(r"\w+", (lst[i]["student_question"] or "").lower()))
        c = set(re.findall(r"\w+", (lst[i+1]["student_question"] or "").lower()))
        if a and c and len(a & c)/len(a | c) >= 0.6: rep += 1
print(f"   K4 hỏi lại gần trùng câu trước (Jaccard>=0.6): {rep}/{tot2} ({100*rep/max(tot2,1):.1f}%)")

hdr("7 · TURN_ID ĐƯỢC TRÍCH TRONG SPEC §1")
for tid in ["T00445","T03818","T01411","T00362","T00636","T10381","T11883","T10416","T00758","T03815","T03816","T03817","T00185","T00451"]:
    r = next((x for x in rows if x["turn_id"] == tid), None)
    if r: print(f"   {tid} {r['asked_at_vn']} {r['student']} {r['course_id']}/{r['lecture_code']} "
                f"preset={r['is_preset']} rating={r['rating']!r} NF={r['_nf']}")
