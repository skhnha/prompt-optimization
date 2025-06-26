
# ... 이하 동일
# ...


# app.py
import streamlit as st
from prompt_templates import get_stage1_prompt, get_stage2_prompt
from llm_client import call_openai_chat
from tests.testset_loader import load_testset
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

if st.session_state.stage2_output:
    st.markdown("---")
    st.markdown("### 🧪 Step 3: 테스트 세트 기반 자동 평가")

    if st.button("📊 3단계 테스트 세트 실행"):
        with st.spinner("테스트 세트 실행 중..."):
            try:
                testset = load_testset()
                results = []

                for idx, test in enumerate(testset, start=1):
                    sys_msg = {"role": "system", "content": st.session_state.stage2_output}
                    user_msg = {"role": "user", "content": test["input"]}
                    output = call_openai_chat([sys_msg, user_msg])
                    results.append({
                        "No": idx,
                        "질문": test["input"],
                        "응답": output.strip(),
                        "기준": test["expected_criteria"]
                    })

                st.success("✅ 테스트 완료")
                for row in results:
                    st.markdown(f"**{row['No']}. 질문:** {row['질문']}")
                    st.markdown(f"📝 **기준:** {row['기준']}")
                    st.code(row['응답'], language="markdown")
                    st.markdown("---")

                # 평가 요청
                if st.button("🤖 LLM으로 응답 품질 평가 요청"):
                    with st.spinner("LLM이 응답 품질을 평가 중..."):
                        review_prompt = "아래의 응답들과 기준을 참고해 각 응답의 품질을 1~5점으로 평가하고 JSON으로 정리해줘:\n\n"
                        for r in results:
                            review_prompt += f"[질문]: {r['질문']}\n[기준]: {r['기준']}\n[응답]: {r['응답']}\n\n"
                        eval_result = call_openai_chat(review_prompt)
                        st.markdown("### 📈 응답 품질 평가 결과")
                        st.code(eval_result.strip(), language="json")
            except Exception as e:
                st.error(f"테스트 실패: {e}")