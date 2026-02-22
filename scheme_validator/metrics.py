# 面积与容积率计算（基础物理世界）
def calc_area_metrics(building_area, land_area, expansion_area):
    total_area = building_area + expansion_area
    far = round(total_area / land_area, 2)
    expansion_ratio = expansion_area / building_area if building_area > 0 else 0
    return {
        "total_area_after": int(total_area),
        "far_after": far,
        "expansion_ratio": round(expansion_ratio, 3)
    }

# 成本模型（唯一成本真理）
def calc_cost(building_area, expansion_area, elevator_add, cost_factor):
    structure = building_area * 550 * cost_factor * 1.15
    fire = building_area * 220 * cost_factor
    interior = building_area * 700 * cost_factor
    expansion = expansion_area * 1800 * cost_factor
    mep = building_area * 500 * cost_factor
    energy = building_area * 400 * cost_factor
    barrier = building_area * 80 * cost_factor
    elevator = elevator_add * 600000 * cost_factor

    direct = structure + fire + interior + expansion + mep + energy + barrier + elevator
    management = direct * 0.12
    tax = (direct + management) * 0.09
    total = direct + management + tax

    return {
        "direct_cost": int(direct),
        "management_cost": int(management),
        "tax": int(tax),
        "total_cost": int(total)
    }

# 工期模型（唯一时间真理）
def calc_duration(building_area, expansion_area):
    base = building_area / 1200
    expansion = expansion_area / 600
    total = base + expansion + 1.0 + 0.5 + 1.0
    return round(total, 2)

# 约束判断（Validator以后只调用这个）
def check_constraints(metrics, cost, duration, target):
    results = {}

    results["far"] = metrics["far_after"] <= target["far_max"]
    results["budget"] = target["budget_min"] <= cost["total_cost"] <= target["budget_max"]
    results["duration"] = duration <= target["duration_max"]
    results["expansion"] = metrics["expansion_ratio"] >= 0.1

    results["pass"] = all(results.values())
    results["score"] = sum(results.values()) / len(results)

    return results
