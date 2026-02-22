import math
from typing import Dict, Any, List


# ===============================
# 工具函数
# ===============================

def _mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _cv(values: List[float]) -> float:
    if not values:
        return 0.0

    mean_val = _mean(values)
    if mean_val == 0:
        return 0.0

    squared_diff_sum = sum((x - mean_val) ** 2 for x in values)
    variance = squared_diff_sum / len(values)
    std = math.sqrt(variance)
    return std / mean_val


# ===============================
# 主函数：评估 exported_schemes
# ===============================

def evaluate_exported_schemes(
    exported_schemes: Dict[str, Dict[str, Any]],
    num_tasks: int = 10,
    rounds: List[str] = ['A', 'B', 'C', 'D', 'E']
) -> Dict[str, Any]:

    # ===============================
    # 1️⃣ 数据收集
    # ===============================

    is_valids_baseline = []
    is_valids_agent = []

    npvs_baseline = []
    npvs_agent = []

    npvs_agent_1 = []
    npvs_agent_2 = []
    npvs_agent_3 = []

    is_valids_agent_round = {
        f"task_{i+1}_{char}": False
        for i in range(num_tasks)
        for char in rounds
    }

    for var_name, var_value in exported_schemes.items():

        # ===============================
        # Baseline
        # ===============================
        if "baseline" in var_name:

            is_valid = var_value["is_valid"]
            is_valids_baseline.append(is_valid)

            if is_valid:
                npvs_baseline.append(var_value["npv"])

        # ===============================
        # Agent
        # ===============================
        elif "agent" in var_name:

            is_valid = var_value["is_valid"]
            is_valids_agent.append(is_valid)

            if is_valid:
                npvs_agent.append(var_value["npv"])

            # 轮级成功率
            for i in range(num_tasks):
                for char in rounds:
                    if f"task_{i+1}_agent" in var_name and char in var_name:
                        if is_valid:
                            is_valids_agent_round[f"task_{i+1}_{char}"] = True

            # 分策略
            for i in range(num_tasks):
                for char in rounds:

                    if f"task_{i+1}_agent" in var_name and f"{char}1" in var_name:
                        if is_valid:
                            npvs_agent_1.append(var_value["npv"])

                    elif f"task_{i+1}_agent" in var_name and f"{char}2" in var_name:
                        if is_valid:
                            npvs_agent_2.append(var_value["npv"])

                    elif f"task_{i+1}_agent" in var_name and f"{char}3" in var_name:
                        if is_valid:
                            npvs_agent_3.append(var_value["npv"])

    # ===============================
    # 2️⃣ 可行率
    # ===============================

    sample_feasibility_baseline = (
        sum(is_valids_baseline) / len(is_valids_baseline)
        if is_valids_baseline else 0
    )

    sample_feasibility_agent = (
        sum(is_valids_agent) / len(is_valids_agent)
        if is_valids_agent else 0
    )

    round_success_agent = (
        sum(is_valids_agent_round.values()) / len(is_valids_agent_round)
        if is_valids_agent_round else 0
    )

    # ===============================
    # 3️⃣ 平均 NPV
    # ===============================

    mean_npv_baseline = _mean(npvs_baseline)
    mean_npv_agent = _mean(npvs_agent)

    mean_npv_agent_1 = _mean(npvs_agent_1)
    mean_npv_agent_2 = _mean(npvs_agent_2)
    mean_npv_agent_3 = _mean(npvs_agent_3)

    # ===============================
    # 4️⃣ 收益稳定性 CV
    # ===============================

    cv_baseline = _cv(npvs_baseline)
    cv_agent_1 = _cv(npvs_agent_1)
    cv_agent_2 = _cv(npvs_agent_2)
    cv_agent_3 = _cv(npvs_agent_3)

    # ===============================
    # 5️⃣ 相对提升率
    # ===============================

    def improvement(mean_agent):
        if mean_npv_baseline == 0:
            return 0.0
        return (mean_agent - mean_npv_baseline) / mean_npv_baseline

    improvement_all = improvement(mean_npv_agent)
    improvement_strategy_1 = improvement(mean_npv_agent_1)
    improvement_strategy_2 = improvement(mean_npv_agent_2)
    improvement_strategy_3 = improvement(mean_npv_agent_3)

    # ===============================
    # 汇总输出
    # ===============================

    return {
        "sample_feasibility_baseline": round(sample_feasibility_baseline, 2),
        "sample_feasibility_agent": round(sample_feasibility_agent, 2),
        "round_success_agent": round(round_success_agent, 2),

        "mean_npv_baseline": round(mean_npv_baseline, 2),
        "mean_npv_agent": round(mean_npv_agent, 2),

        "cv_baseline": round(cv_baseline, 2),
        "cv_agent_1": round(cv_agent_1, 2),
        "cv_agent_2": round(cv_agent_2, 2),
        "cv_agent_3": round(cv_agent_3, 2),

        "improvement_all": round(improvement_all, 2),
        "improvement_strategy_1": round(improvement_strategy_1, 2),
        "improvement_strategy_2": round(improvement_strategy_2, 2),
        "improvement_strategy_3": round(improvement_strategy_3, 2)
    }