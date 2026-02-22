def normalize_scheme_fields(scheme: dict) -> dict:
    """
    将LLM输出格式转换为工程模型可计算格式
    """

    normalized = dict(scheme)

    # ---- 1. 成本拆解扁平化 ----
    cost = scheme.get("cost_breakdown", {})

    normalized["structure_reinforce_cost"] = cost.get("structure_reinforce", 0)
    normalized["fire_upgrade_cost"] = cost.get("fire_upgrade", 0)
    normalized["interior_cost"] = cost.get("interior_renovation", 0)
    normalized["expansion_cost"] = cost.get("expansion", 0)
    normalized["mep_cost"] = cost.get("mechanical_electrical", 0)
    normalized["energy_cost"] = cost.get("energy_saving", 0)
    normalized["barrier_free_cost"] = cost.get("barrier_free", 0)
    normalized["elevator_cost"] = cost.get("elevator", 0)
    normalized["management_cost"] = cost.get("design_management", 0)
    normalized["tax_cost"] = cost.get("tax_and_fees", 0)

    # ---- 2. 派生参数 ----
    if "expansion_ratio" not in normalized:
        base_area = scheme.get("total_area_after", 0) - scheme.get("expansion_area", 0)
        if base_area > 0:
            normalized["expansion_ratio"] = scheme.get("expansion_area", 0) / base_area
        else:
            normalized["expansion_ratio"] = 0

    return normalized