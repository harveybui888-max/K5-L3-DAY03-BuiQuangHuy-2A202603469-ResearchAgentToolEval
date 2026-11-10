# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team:
- Members:
- Provider/model:

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

**Bản demo v1 (OpenRouter / `openai/gpt-4o-mini`):** Research Agent tìm tin trên web và mạng xã hội, xem bài đăng của tài khoản, đọc URL, tra cứu paper arXiv hoặc chính sách nội bộ, rồi tổ chức kết quả thành digest. Prompt v1 yêu cầu hỏi lại khi thiếu thông tin, không tự đoán username/URL, và cần người dùng xác nhận trước hành động gửi; gửi Telegram hiện bị chặn trong UI demo. Tool `deduplicate` mới loại URL nguồn trùng khỏi các item đã có mà không tìm kiếm hay thay đổi nội dung nguồn.

**Link dùng thử:** [https://d01f-14-0-22-183.ngrok-free.app](https://d01f-14-0-22-183.ngrok-free.app)

Link ngrok phụ thuộc vào phiên tunnel đang chạy; nếu tunnel dừng hoặc URL thay đổi, hãy cập nhật link này.

Trong UI, mục **Version để xem** cho phép chọn v0–v3 để xem metric/run đã lưu. Version chưa có run sẽ hiện trạng thái chưa có bằng chứng; phần chat luôn dùng prompt/tools hiện có trong workspace, không tự khôi phục snapshot lịch sử.

## A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại khi thiếu thông tin hoặc cần xác nhận rõ ràng | Không |
| `timeline` | Lấy bài đăng gần đây từ username tài khoản đã được cung cấp | Không |
| `social_search` | Tìm bài đăng công khai theo chủ đề, mới nhất hoặc phổ biến | Không |
| `lookup` | Tìm kiếm web; hỗ trợ tìm tin tức theo khoảng thời gian | Không |
| `fetch` | Đọc nội dung của URL đã được cung cấp hoặc tìm thấy từ nguồn đáng tin | Không |
| `format` | Trình bày các item đã có thành digest; không tự tìm dữ liệu | Không |
| `send` | Gửi nội dung ra ngoài sau khi xác nhận; bị chặn trong UI demo | Không |
| `policy` | Tìm trong bộ tài liệu chính sách nội bộ của project | Không |
| `papers` | Tìm paper học thuật trên arXiv | Không |
| `paper_text` | Lấy nội dung văn bản của paper arXiv theo ID hoặc URL | Không |
| `deduplicate` | Loại URL trùng khỏi danh sách item có sẵn, giữ lại thứ tự và metadata của nguồn đầu tiên | Có — tool mới v1 |

## A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. “Tìm tin tức AI trong ngày hôm nay và tóm tắt các nguồn chính.”
2. “Tìm các bài đăng phổ biến về OpenAI trên mạng xã hội.”
3. “Đọc và tóm tắt bài này: https://openai.com/research/”
4. “Tìm paper arXiv về đánh giá AI agent.”
5. “Loại URL trùng khỏi các nguồn vừa tìm rồi tạo digest.” (Thử sau khi đã yêu cầu agent tìm nguồn.)

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy |  |  |  |
| UI |  |  |  |
| Tool unit tests (`tests/`) | `pytest` output |  |  |

Tool unit tests: số test đã viết, số bug tìm được trong tool có sẵn (nếu có), và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?

## B7. Small Local Model Challenge (bonus)

Only fill if your team did the local model challenge.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?
