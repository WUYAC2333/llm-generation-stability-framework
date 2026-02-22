from config import init_dashscope
from llm import build_baseline_prompt, call_qwen
from scheme_parser import parse_baseline_output
from fallback import build_fallback

def baseline_generate_qwen(building_params, target_params):

    init_dashscope()

    prompt = build_baseline_prompt(building_params, target_params)

    try:
        raw_text = call_qwen(prompt)
        scheme = parse_baseline_output(raw_text, building_params, target_params)

        if scheme:
            return scheme

    except Exception:
        pass

    return build_fallback(building_params, target_params)