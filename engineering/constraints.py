def compile_target_constraints(target_params, building_params):
    """
    把规划目标翻译为工程可计算约束
    """

    compiled = {}

    # ---- FAR ----
    compiled["far_max"] = target_params.get(
        "target_far_upper",
        building_params.get("current_far", 2.0)
    )

    # ---- 预算 ----
    compiled["budget_min"] = target_params.get("budget_min", 0)
    compiled["budget_max"] = target_params.get("budget_max", 1e12)

    # ---- 工期 ----
    compiled["duration_max"] = target_params.get("duration_max", 12)

    # ---- 成本系数（城市差异）----
    compiled["cost_factor"] = building_params.get("cost_adjust_factor", 1.0)

    return compiled