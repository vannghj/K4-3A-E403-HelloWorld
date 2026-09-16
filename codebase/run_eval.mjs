#!/usr/bin/env node
/**
 * Chạy toàn bộ eval/golden_set.json qua module quyết định trung tâm (classify.mjs),
 * gọi LLM thật cho từng ca, ghi log vào eval/call_log.jsonl, in bảng kết quả.
 *
 * Tiêu chí ĐẠT (đã chốt trước khi chạy, không đổi sau khi thấy kết quả):
 *   - expected_tier = "found"   -> đạt khi tier="found" VÀ page = expected_page
 *   - expected_tier = "clarify" -> đạt khi tier="clarify"
 *   - expected_tier = "notfound"     -> đạt khi tier="notfound"
 *   - expected_tier = "out_of_scope" -> đạt khi tier="out_of_scope"
 *
 * Chạy: node codebase/run_eval.mjs
 */
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { classify } from "./classify.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const GOLDEN_PATH = path.join(ROOT, "eval", "golden_set.json");

const cases = JSON.parse(readFileSync(GOLDEN_PATH, "utf8"));

function judge(kase, result) {
  if (result.tier === "parse_error") return false;
  if (kase.expected_tier === "found") {
    return result.tier === "found" && Number(result.page) === Number(kase.expected_page);
  }
  return result.tier === kase.expected_tier;
}

const rows = [];
for (const kase of cases) {
  process.stdout.write(`[${kase.id}] ${kase.question.slice(0, 50) || "(rỗng)"}... `);
  const result = await classify({
    lectureId: kase.lecture,
    question: kase.question,
    caseId: kase.id,
  });
  const pass = judge(kase, result);
  rows.push({ ...kase, actual_tier: result.tier, actual_page: result.page ?? null, reason: result.reason, via: result.via, pass });
  console.log(pass ? "ĐẠT" : `TRƯỢT (thực tế: ${result.tier}${result.page ? " trang " + result.page : ""})`);
}

const passCount = rows.filter((r) => r.pass).length;
console.log(`\n=== ${passCount}/${rows.length} ĐẠT (${((100 * passCount) / rows.length).toFixed(1)}%) ===`);

writeFileSync(
  path.join(ROOT, "eval", "run1_raw.json"),
  JSON.stringify({ ran_at: new Date().toISOString(), pass: passCount, total: rows.length, rows }, null, 2),
  "utf8"
);
console.log(`\nĐã ghi eval/run1_raw.json và eval/call_log.jsonl`);
