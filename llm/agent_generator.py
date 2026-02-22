from typing import Dict, Any
import logging

from llm import call_qwen, build_agent_prompt, baseline_generate_qwen
from scheme_parser import parse_agent_output

logger = logging.getLogger(__name__)

def agent_generate_qwen(
    building_params: Dict[str, Any],
    target_params: Dict[str, Any],
) -> Dict[str, Any]:

    # ===== 1. 构建 Prompt（原逻辑完全保留）=====
    prompt = build_agent_prompt(building_params, target_params)

    # ===== 2. 调用 LLM =====
    output_text = call_qwen(prompt, max_tokens=2048)

    # ===== 3. 解析 =====
    scheme_list = parse_agent_output(
        output_text,
        building_params,
        target_params
    )

    # ===== 4. 兜底 =====
    if not scheme_list:
        fallback = baseline_generate_qwen(
            building_params,
            target_params
        )
        return {
            "scheme": fallback,
            "source": "fallback"
        }

    # ===== 5. 预算边界保护（原逻辑保留）=====
    min_budget = target_params["budget_min"]
    max_budget = target_params["budget_max"]

    for scheme in scheme_list:
        budget_val = scheme.get("budget", min_budget)
        scheme["budget"] = max(min_budget, min(budget_val, max_budget))

    return {
        "schemes": scheme_list,
        "source": "agent"
    }