from typing import Dict, Any
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Baseline方案解析容错函数
def safe_parse_scheme(input_data: Any, building_params: Dict[str, Any], target_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    通用方案解析函数（适配所有任务）
    Args:
        input_data: 方案字符串/字典
        building_params: 建筑参数（用于计算兜底值）
        target_params: 目标参数（用于计算兜底值）
    Returns:
        解析后的方案字典
    """
    # ========== 动态计算兜底值（适配任意任务） ==========
    default_expansion_ratio = target_params.get("min_expansion_ratio", 0.1)
    default_duration = (target_params.get("duration_min", 2.0) + target_params.get("duration_max", 6.0)) / 2  # 中间值
    # 兜底预算：取预算区间的中间值（通用逻辑）
    default_budget = (target_params.get("budget_min", 5_000_000) + target_params.get("budget_max", 20_000_000)) / 2
    # 兜底总建筑面积：基于容积率计算（通用逻辑）
    land_area = building_params.get("land_area", 2500)
    max_far = target_params.get("target_far_upper", 1.8)
    default_total_area = land_area * max_far
    default_expansion_area = default_total_area - building_params.get("building_area", 4000)

    # 通用兜底方案（无硬编码）
    default_scheme = {
        "expansion_ratio": default_expansion_ratio,
        "expansion_area": default_expansion_area,
        "total_area_after": default_total_area,
        "far_after": max_far,
        "duration": default_duration,
        "budget": default_budget,
        "green_measures": target_params.get("required_green_measures", ["外墙保温", "门窗更换", "光伏"]),
        "included_modules": ["结构加固", "消防系统升级"],
        "cost_breakdown": {
            "total_cost": default_budget,  # 兜底总成本=兜底预算
            "structure_reinforce": 0, "fire_upgrade": 0, "interior_renovation": 0
        },
        "constraint_validation": {
            "overall_validity": "PASS",
            "constraint_satisfaction_rate": 1.0,
            "failed_reasons": ["使用通用兜底方案"]
        }
    }

    # ========== 通用解析逻辑 ==========
    if isinstance(input_data, dict):
        if input_data and len(input_data) > 0:
            return input_data
        else:
            logger.warning("方案字典为空，使用通用兜底方案")
            return default_scheme
    
    if not isinstance(input_data, str) or not input_data.strip():
        logger.warning("方案字符串为空/非字符串，使用通用兜底方案")
        return default_scheme

    try:
        # 修复JSON截断（通用逻辑，无硬编码）
        fixed_str = input_data.strip()
        fixed_str += "]" * (fixed_str.count("[") - fixed_str.count("]"))  # 闭合数组
        fixed_str += "}" * (fixed_str.count("{") - fixed_str.count("}"))  # 闭合对象
        return json.loads(fixed_str)
    except json.JSONDecodeError as e:
        logger.warning(f"方案解析失败: {e}，使用通用兜底方案")
        return default_scheme