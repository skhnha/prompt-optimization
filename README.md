# Meta Prompt Optimizer

## 개요

사내 다양한 오픈소스 LLM (llama3.3, llama4-scout, llama4-maverick, deepseek-r1, qwen2.5, qwen3 등)을 위한 **메타 프롬프트 기반 시스템 프롬프트 자동 최적화 서비스**입니다.

---

## 주요 기능

* **1단계: 시스템 프롬프트 구조화 및 리파인**
  사용자가 제시한 초안 프롬프트를 최신 고성능 모델(Qwen3 우선, 부재시 deepseek-r1, qwen2.5 등 대체)로 분석하여
  명확하고 다국어 지원 가능한 최적 시스템 프롬프트로 재구성합니다.

* **2단계: 타겟 LLM Self-Reflection 기반 맞춤 최적화**
  실제 사용할 모델(llama3.3, llama4, qwen2.5 등)을 선택하면, 해당 모델 특성에 맞게 프롬프트를 재작성하여 성능을 극대화합니다.

---

## 프로젝트 구조

```
.
├── app.py                   # Streamlit 웹 앱 메인
├── llm_client.py            # API 호출 모듈
├── prompt_templates/
│   ├── stage1_prompt.md     # 1단계 메타 프롬프트 템플릿
│   ├── stage2_prompt.md     # 2단계 self-reflection 템플릿
│   └── __init__.py          # 템플릿 로딩 및 렌더링 함수
├── requirements.txt
└── README.md
```

---

## 사용법

* Step 1: 사용자 초안 시스템 프롬프트를 입력
* Step 2: 1단계 템플릿을 선택하고 실행 → 최적화된 시스템 프롬프트 획득
* Step 3: 타겟 LLM 모델 선택 (llama3.3, llama4-scout, qwen2.5 등)
* Step 4: 2단계 Self-Reflection 실행 → 타겟 모델에 맞는 최종 시스템 프롬프트 획득