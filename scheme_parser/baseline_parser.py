import json
import re
from engineering import compute_costs, compute_green_score, compute_annual_income, compute_npv

def parse_baseline_output(text, building_params, target_params):

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None

    json_text = text[start:end+1]
    json_text = re.sub(r",\s*}", "}", json_text)
    json_text = re.sub(r",\s*]", "]", json_text)

    data = json.loads(json_text)

    # 计算模型
    data = compute_costs(data, building_params, target_params)
    data["green_score"] = compute_green_score(data, building_params)
    data["annual_income"] = compute_annual_income(data, building_params)
    data["npv"] = compute_npv(data)

# 核对工期
    new_elevator_count = target_params["elevator_upgrade_req"]-building_params["elevator_config"]
    data["duration_calculation"]["elevator_duration"] = 0.5*new_elevator_count
    data["duration_calculation"]["buffer_duration"] = round(0.1 * (data["duration_calculation"]["base_duration"]+data["duration_calculation"]["expansion_duration"]+data["duration_calculation"]["green_duration"]+data["duration_calculation"]["elevator_duration"]), 2)
    total_duration = data["duration_calculation"]["base_duration"]+data["duration_calculation"]["expansion_duration"]+data["duration_calculation"]["green_duration"]+data["duration_calculation"]["elevator_duration"]+data["duration_calculation"]["buffer_duration"]
    data["duration"] = round(total_duration, 2)
    data["duration_calculation"]["estimated_total_duration"] = round(total_duration, 2)

    # expansion_ratio 保证存在
    if "expansion_ratio" not in data:
        data["expansion_ratio"] = data.get("expansion_ratio", 0.0)

    # ===== 成本完整性检查 =====
    if len(data.get("cost_breakdown", {})) < 6:
        return None
    
    return data