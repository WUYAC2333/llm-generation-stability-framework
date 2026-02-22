from .metrics import (
    calc_area_metrics,
    calc_cost,
    calc_duration,
    check_constraints
)
from engineering import compile_target_constraints, normalize_scheme_fields
import logging
from typing import Dict, Any


logger = logging.getLogger(__name__)

def verify_scheme(scheme: Dict[str, Any], target_params, building_params):
    compiled_constraints = compile_target_constraints(target_params, building_params)

    # 先检查约束是否可行，如果完全不可行就直接返回“任务参数不合理”
    expansion_allowed = target_params["expansion_allowed"]
    required_expansion = target_params["max_expansion_ratio"]
    if not expansion_allowed and required_expansion > 0:
        return False, "任务参数冲突：禁止扩容，但预算/工期/容积率要求无法满足"

    try:
        scheme = normalize_scheme_fields(scheme)

        # ===== 1. 从方案中提取数值 =====
        building_area = building_params["building_area"]
        land_area = building_params["land_area"]

        expansion_area = scheme.get("expansion_area", 0)

        # 电梯增加量（防御写法）
        existing_elevator = building_params.get("elevator_config", 0)
        elevator_after = scheme.get("elevator_after", existing_elevator)
        elevator_add = max(0, elevator_after - existing_elevator)

        # 成本系数（城市差异）
        cost_factor = compiled_constraints["cost_factor"]

        # ===== 2. 工程模型评估 =====
        metrics = calc_area_metrics(
            building_area,
            land_area,
            expansion_area
        )

        cost = calc_cost(
            building_area,
            expansion_area,
            elevator_add,
            cost_factor
        )

        duration = calc_duration(
            building_area,
            expansion_area
        )

        result = check_constraints(
            metrics,
            cost,
            duration,
            compiled_constraints
        )

        # ===== 3. 写回真实评估结果（关键！）=====
        scheme["estimated_total_cost"] = cost["total_cost"]
        scheme["estimated_duration"] = duration
        scheme["far_after"] = metrics["far_after"]
        scheme["expansion_ratio"] = metrics["expansion_ratio"]

        if result["pass"]:
            return True, "所有约束满足"

        # ===== 4. 生成可学习的反馈 =====
        feedback = []
        if not result["budget"]:
            feedback.append(f"预算不满足：当前约 {cost['total_cost']/10000:.1f} 万")

        if not result["duration"]:
            feedback.append(f"工期过长：约 {duration} 月")

        if not result["far"]:
            feedback.append(f"容积率超限：{metrics['far_after']}")

        if not result["expansion"]:
            feedback.append(f"扩容比例不足：{metrics['expansion_ratio']:.2%} (<10%)")

        return False, "；".join(feedback)

    except Exception as e:
        logger.error(f"工程验证异常: {e}", exc_info=True)

        # 强制写回安全字段，防止上层崩溃
        scheme["estimated_total_cost"] = 0.0
        scheme["estimated_duration"] = 0.0
        scheme["far_after"] = 0.0
        scheme["expansion_ratio"] = 0.0

        return False, f"工程验证异常: {str(e)}"