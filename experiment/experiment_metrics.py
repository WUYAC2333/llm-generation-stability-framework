def extract_metrics(scheme: dict, is_valid: bool, gen_time: float):

    cost_val = scheme.get("budget", 0.0) or 0.0
    duration_val = scheme.get("duration", 0.0) or 0.0

    return {
        "is_valid": is_valid,
        "budget": cost_val,
        "duration": duration_val,
        "expansion_ratio": scheme.get("expansion_ratio", 0),
        "green_measures_count": len(scheme.get("green_measures", [])),
        "total_cost": cost_val,
        "generation_time": gen_time
    }