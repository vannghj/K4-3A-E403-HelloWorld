#!/usr/bin/env node
/**
 * Server demo cho giao diện web — nối web-demo.html với module quyết định
 * trung tâm classify.mjs (gọi LLM thật), để có giao diện đẹp mà vẫn là AI thật,
 * không phải heuristic phía client như prototype/dung-trang.html.
 *
 * Chạy: node codebase/server.mjs
 * Mở:  http://localhost:8787
 */
import { createServer } from "node:http";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { classify } from "./classify.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LECTURES = JSON.parse(readFileSync(path.join(__dirname, "lectures.json"), "utf8"));
const PORT = process.env.PORT || 8787;

function send(res, status, body, contentType = "application/json") {
  res.writeHead(status, { "content-type": contentType, "access-control-allow-origin": "*" });
  res.end(typeof body === "string" ? body : JSON.stringify(body));
}

const server = createServer(async (req, res) => {
  try {
    if (req.method === "GET" && req.url === "/") {
      const html = readFileSync(path.join(__dirname, "web-demo.html"), "utf8");
      return send(res, 200, html, "text/html; charset=utf-8");
    }

    if (req.method === "GET" && req.url.startsWith("/api/lecture")) {
      const id = new URL(req.url, "http://x").searchParams.get("id") || "day04";
      const lecture = LECTURES[id];
      if (!lecture) return send(res, 404, { error: "không có bài giảng " + id });
      return send(res, 200, { id, ...lecture });
    }

    if (req.method === "POST" && req.url === "/api/classify") {
      let body = "";
      for await (const chunk of req) body += chunk;
      const { lectureId, question } = JSON.parse(body || "{}");
      if (!lectureId || typeof question !== "string") {
        return send(res, 400, { error: "cần lectureId và question" });
      }
      const result = await classify({ lectureId, question });
      return send(res, 200, result);
    }

    send(res, 404, { error: "not found" });
  } catch (err) {
    console.error(err);
    send(res, 500, { error: String(err && err.message ? err.message : err) });
  }
});

server.listen(PORT, () => {
  console.log(`Server demo đang chạy: http://localhost:${PORT}`);
  console.log(`Mở link trên bằng trình duyệt để dùng giao diện thật (gọi AI thật, không phải mock).`);
});
