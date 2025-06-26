import os

def load_template(file_name: str) -> str:
    path = os.path.join(os.path.dirname(__file__), file_name)
    with open(path, encoding='utf-8') as f:
        return f.read()

def render_template(template_str: str, variables: dict) -> str:
    for key, value in variables.items():
        template_str = template_str.replace(f"{{{{{key}}}}}", value)
    return template_str

def get_stage1_prompt(user_prompt: str) -> str:
    template = load_template("stage1_prompt.md")
    return render_template(template, {"user_prompt": user_prompt})

def get_stage2_prompt(stage1_output: str, model_name: str) -> str:
    template = load_template("stage2_prompt.md")
    return render_template(template, {
        "stage1_output": stage1_output,
        "model_name": model_name,
    })