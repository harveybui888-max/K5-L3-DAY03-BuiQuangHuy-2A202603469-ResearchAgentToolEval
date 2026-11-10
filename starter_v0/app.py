from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from chat import execute_tool_call, run_model_tool_loop
from env_loader import load_lab_env
from providers import make_provider
from providers.base import ToolCall
from tools import load_tool_declarations, to_openai_tools


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
PROVIDERS = ["openrouter", "openai", "anthropic", "gemini", "ollama"]
DEFAULT_MODELS = {
    "openrouter": "openai/gpt-4o-mini",
    "ollama": "qwen2.5:7b",
}

load_lab_env(ROOT)


def execute_demo_tool(call: ToolCall) -> dict[str, Any]:
    if call.name == "send":
        return {
            "tool": call.name,
            "args": call.args,
            "result": {
                "status": "blocked_in_demo",
                "message": "Telegram sending is disabled in this demo UI.",
            },
        }
    return execute_tool_call(call)


def main() -> None:
    st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="wide")
    st.title("🔎 Research Agent")
    st.caption("Tìm kiếm, đọc và tổng hợp thông tin từ web, mạng xã hội, arXiv và tài liệu chính sách.")

    with st.sidebar:
        st.header("Cấu hình")
        provider_name = st.selectbox("Provider", PROVIDERS, index=0)
        model = st.text_input(
            "Model (để trống dùng mặc định)",
            value=DEFAULT_MODELS.get(provider_name, ""),
        ).strip() or None
        st.caption("API keys được đọc từ starter_v0/.env. Không nhập hoặc chia sẻ API key trong chat.")
        st.warning(
            "Các tool tìm kiếm có thể gọi dịch vụ/API thật. Gửi Telegram bị tắt trong UI demo."
        )
        if st.button("Xóa hội thoại", use_container_width=True):
            st.session_state["conversation"] = []

    if "conversation" not in st.session_state:
        st.session_state["conversation"] = []

    for entry in st.session_state["conversation"]:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])
            if entry.get("tool_events"):
                with st.expander("Chi tiết tool đã gọi"):
                    for event in entry["tool_events"]:
                        st.json(event)

    user_text = st.chat_input("Bạn muốn tìm hiểu điều gì?")
    if not user_text:
        return

    conversation: list[dict[str, Any]] = st.session_state["conversation"]
    conversation.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    try:
        system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
        declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
        provider = make_provider(provider_name)
        messages = [
            {"role": "system", "content": system_prompt},
            *[
                {"role": item["role"], "content": item["content"]}
                for item in conversation[-12:]
            ],
        ]
        with st.chat_message("assistant"):
            with st.spinner("Đang nghiên cứu..."):
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=to_openai_tools(declarations),
                    model=model,
                    max_tool_rounds=4,
                    tool_executor=execute_demo_tool,
                )
            st.markdown(result["assistant_text"])
            if result["tool_events"]:
                with st.expander("Chi tiết tool đã gọi"):
                    for event in result["tool_events"]:
                        st.json(event)
        conversation.append({
            "role": "assistant",
            "content": result["assistant_text"],
            "tool_events": result["tool_events"],
        })
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        st.error(f"Không thể xử lý yêu cầu. {message}")
        conversation.append({"role": "assistant", "content": f"Lỗi: {message}"})


if __name__ == "__main__":
    main()
