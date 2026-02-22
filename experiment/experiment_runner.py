import time
import logging
import pandas as pd
from typing import Dict, Tuple

from llm import baseline_generate_qwen, agent_generate_qwen
from scheme_validator import verify_scheme
from scheme_parser import safe_parse_scheme
from fallback import build_fallback
from experiment import extract_metrics

logger = logging.getLogger(__name__)

def run_experiment(
    building_params: Dict,
    target_params: Dict,
    rounds: int = 5
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    # ================= Baseline =================
    start = time.time()
    raw = baseline_generate_qwen(building_params, target_params)

    if not raw:
        baseline_scheme = build_fallback()
    else:
        baseline_scheme = safe_parse_scheme(raw, building_params, target_params)

    is_valid, problems = verify_scheme(
        baseline_scheme,
        target_params,
        building_params
    )

    if is_valid is True:
        baseline_scheme["is_valid"] = True
    else:
        baseline_scheme["is_valid"] = False
        logger.info("Baseline 方案异常：", problems)

    logger.info(
        extract_metrics(
            baseline_scheme,
            is_valid,
            time.time() - start
        )
    )

    # ================= Agent =================
    start = time.time()

    agent_result = agent_generate_qwen(
        building_params,
        target_params,
    )

    agent_schemes = agent_result.get("schemes", [])

    for s in agent_schemes:
        is_valid, problems = verify_scheme(
            s,
            target_params,
            building_params
        )
        if is_valid is True:
            s["is_valid"] = True
        else:
            s["is_valid"] = False
            logger.info("Agent 方案异常：", problems)

        logger.info(
            extract_metrics(
                s,
                is_valid,
                time.time() - start
            )
        )

    return (
        baseline_scheme,
        agent_schemes
    )