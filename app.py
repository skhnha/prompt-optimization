
# ... 이하 동일
# ...


# app.py
import streamlit as st
from prompt_templates import get_stage1_prompt, get_stage2_prompt
from llm_client import call_openai_chat
import re

model_options = [
    "llama3.3",
    "llama4-scout",
    "llama4-maverick",
    "qwen2.5"
]

st.set_page_config(page_title="🧠 System Prompt Optimizer (2단계 포함)", layout="wide")
st.title("🧠 Meta-Prompt 기반 System Prompt 최적화기")

st.markdown("### 🎯 Step 1: 사용자 초안 → 구조화된 최적 프롬프트")
st.info("""
Step 1에서는 다국어와 복잡한 문장 구조를 잘 처리하는 Qwen 2.5를 사용합니다.
""")

user_input = st.text_area("✏️ 사용자 작성 초안 시스템 프롬프트", height=200)

if 'stage1_output' not in st.session_state:
    st.session_state.stage1_output = None
if 'stage2_output' not in st.session_state:
    st.session_state.stage2_output = None

if st.button("🔁 1단계 최적화 시작"):
    if not user_input.strip():
        st.warning("초안 프롬프트를 입력해주세요.")
    else:
        with st.spinner("1단계 메타 프롬프트 최적화 중..."):
            stage1_prompt = get_stage1_prompt(user_input)
            try:
                result = call_openai_chat(stage1_prompt)
                match = re.search(r"<optimized_system_prompt>(.*?)</optimized_system_prompt>", result, re.DOTALL)
                optimized_prompt = match.group(1).strip() if match else result
                st.session_state.stage1_output = optimized_prompt
                st.success("✅ 1단계 최적화 완료!")
                st.subheader("📘 최적화된 시스템 프롬프트 (1단계)")
                st.code(optimized_prompt, language="markdown")
            except Exception as e:
                st.error(f"1단계 실패: {e}")                

# 2단계 시작
if st.session_state.stage1_output:
    st.markdown("---")
    st.markdown("### 🤖 Step 2: 타겟 LLM Self-Reflection 기반 최적화")
    target_model = st.selectbox("🧠 타겟 LLM 모델 선택", model_options, index=0)

    if st.button("✨ 2단계 Self-Evolution 수행"):
        with st.spinner("2단계 Self-Reflection 최적화 중..."):
            stage2_prompt = get_stage2_prompt(
                st.session_state.stage1_output,
                target_model,
            )
            try:
                result2 = call_openai_chat(stage2_prompt)
                match2 = re.search(r"<final_model_specific_prompt>(.*?)</final_model_specific_prompt>", result2, re.DOTALL)
                final_prompt = match2.group(1).strip() if match2 else result2
                st.session_state.stage2_output = final_prompt
                st.success("✅ 2단계 최적화 완료!")
                st.subheader(f"🧩 {target_model} 전용 최적화된 시스템 프롬프트")
                st.code(final_prompt, language="markdown")
                st.download_button("📥 다운로드", final_prompt, file_name=f"{target_model}_final_prompt.txt")
            except Exception as e:
               st.error(f"2단계 실패: {e}")