# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: K5-L3-DAY03
- Members: BuiQuangHuy (2A202603469)
- Provider/model: OpenRouter / `openai/gpt-4o-mini`

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

Nguồn: `artifacts/version_log.csv` + `runs/*.json`. Provider thống nhất `openrouter` / `openai/gpt-4o-mini` trên toàn bộ v0–v3.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---:|---:|---|
| v0 | baseline (starter prompt/tools) | Đo hành vi chưa tối ưu trước khi sửa | — | 0.70 | `runs/v0_B_base_openrouter_20261110T101549588314.json` |
| v1 | `system_prompt.md`, `tools.yaml`, tool `deduplicate` | Rule routing + clarify + xác nhận + out-of-scope rõ ràng, thêm tool dedup giúp tăng độ chính xác base | 0.70 | 0.80 | `runs/v1_B_base_openrouter_20261110T123637404079.json` |
| v2 | `data/eval_group.json`, `tests/` | Thêm 10 case nhóm + hoàn thiện unit test (151 pass); prompt/tools giữ nguyên v1 nên base giữ mức | 0.80 | 0.80 | `runs/v2_B_base_openrouter_20261110T143018101594.json` |
| v3 | `system_prompt.md`, `tools.yaml` | Làm rõ required args, multi-turn carryover, yêu cầu input của `deduplicate`, xác nhận `send` | 0.80 | 0.90 | `runs/v3_B_base_openrouter_20261110T185942598716.json` |

**Chi tiết metric theo từng version (suite base, 20 case):**

| Version | case_accuracy | tool_routing_accuracy | argument_accuracy | multiturn_accuracy | provider_error |
|---|---:|---:|---:|---:|---:|
| v0 | 0.70 | 0.75 | 0.70 | 1.0 | 0 |
| v1 | 0.80 | 0.95 | 0.80 | 0.8333 | 0 |
| v2 | 0.80 | 1.0 | 0.80 | 0.8333 | 0 |
| v3 | 0.90 | 0.95 | 0.90 | 0.8333 | 0 |

**Suite group (10 case nhóm):** v2 = 0.80 (8/10) → v3 = **1.0 (10/10)**. Run: `runs/v2_B_group_openrouter_20261110T143124579452.json`, `runs/v3_B_group_openrouter_20261110T190006345337.json`.

## B2. Failure Analysis

Nguồn: `results[*].result.failures` + `observed_mismatch` trong run JSON.

### 2.1 Lỗi baseline v0 (6 case FAIL)

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix (đưa vào phiên bản nào) |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send(text=giải tích phân)` | Câu toán ngoài phạm vi bị gọi `send` thay vì từ chối | Rule out-of-scope + cấm route bừa (v1) |
| R10_missing_handle | missing_info | `timeline(screenname="sama")` | Đoán handle `sama` thay vì `clarify` | Rule "never guess username" + clarify (v1) |
| R11_missing_url | missing_info | `fetch(url=example.com/article)` | Bịa URL thay vì `clarify` | Rule "never invent URL" + clarify (v1) |
| R12_confirm_before_send | wrong_boundary | `send(text=...)` | Gửi ngay không xác nhận | Rule xác nhận trước khi gửi (v1) |
| R13_parallel_web_and_tweets | wrong_tool | `lookup(query="AI news")` + `social_search` | query bị viết dài (`"AI news"` thay vì `"AI"`) + thiếu `topic="news"` | Rõ convention args lookup (v1) |
| R14_out_of_scope_coding | out_of_scope | `send(text=code Fibonacci)` | Câu coding bị gọi `send` thay vì từ chối | Rule out-of-scope (v1) |

### 2.2 Lỗi còn lại sau mỗi vòng

| Version | Case còn FAIL | Nguyên nhân |
|---|---|---|
| v1 (4 fail) | R10, R11, R12, M06 | `clarify` gọi đúng tool nhưng **thiếu `response_type`**; M06 gọi thêm `social_search` dù đã chuyển sang web |
| v2 (4 fail) | R10, R11, R12, M02 | Vẫn thiếu `response_type` trong `clarify`; M02 thiếu `timeframe="day"` khi carryover |
| v3 (2 fail) | R12, M06 | R12: `clarify` dùng `response_type="text"` thay vì `"yes_no"` (hỏi nội dung thay vì xác nhận). M06: vẫn gọi thêm `social_search` (extra tool call) |

**Kết luận:** 4/6 lỗi v0 đã được fix triệt để. Hai lỗi còn lại ở v3 (R12, M06) đều thuộc nhóm "tinh tế" — phân biệt câu hỏi nội dung vs câu xác nhận, và tuân thủ "chuyển kênh" ở multi-turn — xem phản ánh ở B6.

## B3. Team Eval Cases

10 case trong `data/eval_group.json` (5 single-turn + 5 multi-turn), có case kiểm tra tool mới `deduplicate`.

| Case ID | Loại | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|---|
| G01_arxiv_papers_routing | single | Tìm paper/preprint → arXiv | `papers` | PASS (v3) |
| G02_arxiv_paper_text_arg | single | arXiv ID + "3 trang đầu" | `paper_text(arxiv_url, max_pages=3)` | PASS (v3) |
| G03_policy_external_publishing | single | Policy xuất bản ra ngoài | `policy(policy_area="external_publishing")` | PASS (v3) |
| G04_dedup_missing_items_clarify | single | `deduplicate` thiếu items → hỏi lại | `clarify` | PASS (v3; fail v2) |
| G09_dedup_tracking_params | single | Lọc trùng khi URL chỉ khác tracking param/fragment | `deduplicate` | Chưa chạy (mới) |
| G05_multiturn_papers_to_paper_text | multi | Chuyển từ tìm paper → đọc paper cụ thể | `paper_text` | PASS (v3) |
| G06_multiturn_send_confirmation | multi | Gửi cần xác nhận trước | `send(confirmed=true)` | PASS (v3; fail v2) |
| G07_multiturn_papers_limit_correction | multi | Carry chủ đề + sửa `max_results=3` | `papers(max_results=3)` | PASS (v3) |
| G08_multiturn_dedup_after_items | multi | Thiếu items → có items → route `deduplicate` | `deduplicate` | PASS (v3) |
| G10_multiturn_dedup_no_format | multi | Có items + chỉ lọc trùng (không format) | `deduplicate` | Chưa chạy (mới) |

Kết quả PASS lấy từ run suite `group` v3 (`runs/v3_B_group_openrouter_20261110T190006345337.json`, 10/10 cho bộ case G01–G08 + TOOLV2_DEDUP_01/02). Ở v2, `G04` (model gọi `deduplicate(items=[])` thay vì `clarify`) và `G06` (gọi `send` thiếu `confirmed=true`) bị FAIL; v3 sửa rule đã pass cả hai. `G09`/`G10` là 2 case mới thay thế `TOOLV2_DEDUP_01/02`, chưa chạy lại suite group.

## B4. Live Chat Evidence

Nguồn: `transcripts/v3_openrouter_20261110T190641216154.transcript.json` (`v3+p59c08e5c7e09+t7d8f4bdd2f89`).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Find today's AI news and briefly summarize a few notable sources. | `lookup(query="AI news", topic="news", timeframe="day", max_results=5)` | v3, `openai/gpt-4o-mini` | Trả về tóm tắt 5 nguồn tin AI trong ngày |
| 2 | Summarize the 3 latest posts from an X account for me. | Không gọi tool | v3, `openai/gpt-4o-mini` | Hỏi lại username thay vì đoán |
| 3 | The username is @OpenAI; get exactly 3 latest posts. | `timeline(screenname="OpenAI", limit=3)` | v3, `openai/gpt-4o-mini` | Trả về 3 bài đăng mới nhất của @OpenAI |
| 4 | Please send the message 'AI news digest' to Telegram. | Không gọi tool | v3, `openai/gpt-4o-mini` | Yêu cầu xác nhận trước; không gửi (thiếu Telegram credentials khi test) |

Điểm quan sát: agent v3 hỏi lại đúng chỗ thiếu thông tin (turn 2) và chặn đúng hành động gửi khi chưa xác nhận (turn 4) — khớp với các rule trong `system_prompt.md` v3.

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới `deduplicate` | `tools/deduplicate/tool.py` + `TOOL.md`, đăng ký trong `tools/__init__.py` + `tools.yaml` | Loại URL trùng (chuẩn hoá tracking param/fragment, giữ metadata) | Không tự bịa item; `TOOL.md` ghi rõ "ask clarify if missing" |
| Unit tests | `pytest` → **151 passed, 0 failed, 0 skipped** | `test_deduplicate.py` (110 dòng) + `test_tools_todo.py` không còn `skip` + `test_tool_contract.py` (60 test) giữ sync | — |
| UI | `app.py` (Streamlit) | Chọn version để xem metric/run, chat trực tiếp | Link ngrok tạm thời; `send` bị chặn trong UI demo |
| send (Telegram) | `transcripts/v3_...turn 4` | Guardrail xác nhận trước khi gửi hoạt động | Không có TELEGRAM keys khi test → không gửi thật |
| arXiv + company policy | `tools/papers`, `tools/paper_text`, `tools/policy` | Hoạt động (case G01–G03, G05, G07) | arXiv rate-limit được xử lý bằng sleep + retry |

Ví dụ lỗi unit test bắt được mà eval KHÔNG bắt được: eval chỉ chấm tên tool + args subset, nên `deduplicate` được gọi đúng tên vẫn PASS dù tool có bug. `tests/test_deduplicate.py` kiểm tra hành vi thật (giữ item đầu, chuẩn hoá `utm_*`/`fbclid`/`gclid`/fragment, không mutate input, trả error dict khi input sai) — những thứ eval routing không đo được.

## B6. Reflection

- **Fix nào thuộc `system_prompt.md`?** Hầu hết lỗi v0 là lỗi *chính sách* của agent, không phải lỗi mô tả tool: đoán username/URL, gửi không xác nhận, route câu out-of-scope vào `send`. Tất cả được sửa bằng các rule trong prompt (Section 2 "Missing Information", Section 3 "Tool Selection", Section 4 "Multiple Tool Usage", Section 5 "Out-of-Scope"). V3 thêm rule cụ thể cho `response_type` (text vs yes_no), multi-turn carryover và yêu cầu input của `deduplicate`.
- **Fix nào thuộc `tools.yaml`?** Mô tả tool mới `deduplicate` (local only, không search/fetch/format, không bịa items) và các convention args (handle không có `@`, `topic=news`, `timeframe`, `search_type=Top/Latest`, `send` chỉ gửi khi `confirmed=true`).
- **Failure nào cần review thủ công thay vì chấm tự động?** R12 (phân biệt "hỏi nội dung" vs "hỏi xác nhận" qua `response_type`) và M06 (model gọi thêm `social_search` sau khi user nói "chuyển sang web"). Đây là lỗi ngữ nghĩa/nuance, khó bắt bằng rule tĩnh; cần đọc `observed_mismatch` + `actual_tool_calls` để hiểu.
- **Cải thiện tiếp theo?** (1) Thêm vài few-shot example trong prompt cho `send` confirm và switch-tool để fix nốt R12/M06; (2) chạy lại suite group với `eval_group.json` hiện tại nếu có case mới thay thế; (3) thử Small Local Model Challenge (Step 7) để đo độ bền của prompt khi chạy model nhỏ.

## B7. Small Local Model Challenge (bonus)

Chưa thực hiện (nhóm chưa chạy model local qua Ollama). Nếu làm, điền bảng dưới và ghi run vào `version_log.csv`.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | `openai/gpt-4o-mini` (openrouter) | v3 | 0.90 | 0.95 | 0.90 | 0.8333 | `runs/v3_B_base_openrouter_20261110T185942598716.json` |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON): *(chưa có dữ liệu)*

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? *(chưa thực hiện)*
- Bản prompt tối ưu cho local chạy trên model cloud thì sao? *(chưa thực hiện)*
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này? *(chưa thực hiện)*
