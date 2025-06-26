# llm_client.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def call_openai_chat(prompt: str, model="gpt-4o") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response['choices'][0]['message']['content']