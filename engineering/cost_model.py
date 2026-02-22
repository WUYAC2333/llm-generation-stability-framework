def compute_costs(data, building_params, target_params):

    # 定义单价
    UNIT_PRICE = {
            "structure_reinforce": 550,
            "fire_upgrade": 220,
            "interior_renovation": 700,
            "expansion": 1800,
            "mechanical_electrical": 500,
            "barrier_free": 80,
            "elevator": 600000
    }

    cost_adjust_factor = building_params["cost_adjust_factor"]

    if data["quantity_breakdown"]:
        q = data["quantity_breakdown"]

        # 计算绿建成本
        unit_price = {
            "外墙保温": 80,
            "门窗更换": 220,
            "光伏": 180,
            "雨水回收": 35,
            "智能照明": 45,
            "地源热泵": 320,
            "高效灯具": 20
        }
        breakdown = {}
        energy_cost = 0
        for measure in data["green_measures"]:
            if measure in unit_price:
                cost = unit_price[measure] * q["energy_saving_area"]
                breakdown[measure] = cost
                energy_cost += cost

        # 直接成本计算
        structure_cost = q["structure_reinforce_area"] * UNIT_PRICE["structure_reinforce"]
        fire_cost = q["fire_upgrade_area"] * UNIT_PRICE["fire_upgrade"]
        interior_cost = q["interior_renovation_area"] * UNIT_PRICE["interior_renovation"]
        expansion_cost = q["expansion_area"] * UNIT_PRICE["expansion"]
        mech_cost = q["mechanical_electrical_area"] * UNIT_PRICE["mechanical_electrical"]
        barrier_cost = q["barrier_free_area"] * UNIT_PRICE["barrier_free"]
        elevator_cost = (target_params["elevator_upgrade_req"]-building_params["elevator_config"]) * UNIT_PRICE["elevator"]
        data["quantity_breakdown"]["new_elevator_count"] = target_params["elevator_upgrade_req"]-building_params["elevator_config"]

        # 90年代扩容加固溢价
        if data["expansion_ratio"] > 0:
            structure_cost *= 1.15

        # 板块溢价
        direct_cost = (
            structure_cost + fire_cost + interior_cost + expansion_cost +
            mech_cost + energy_cost + barrier_cost + elevator_cost
        ) * cost_adjust_factor

        # 管理费 & 税费
        design_management = direct_cost * 0.12
        tax_and_fees = (direct_cost + design_management) * 0.09

        total_cost = direct_cost + design_management + tax_and_fees

        data["budget"] = round(total_cost, 2)
        data["cost_breakdown"] = {
            "structure_reinforce": int(structure_cost * cost_adjust_factor),
            "fire_upgrade": int(fire_cost * cost_adjust_factor),
            "interior_renovation": int(interior_cost * cost_adjust_factor),
            "expansion": int(expansion_cost * cost_adjust_factor),
            "mechanical_electrical": int(mech_cost * cost_adjust_factor),
            "energy_saving": int(energy_cost * cost_adjust_factor),
            "barrier_free": int(barrier_cost * cost_adjust_factor),
            "elevator": int(elevator_cost * cost_adjust_factor),
            "design_management": int(design_management),
            "tax_and_fees": int(tax_and_fees),
            "total_cost": int(total_cost)
        }
    else:
        print("LLM返回结果中找不到quantity_breakdown字段：", data)

    return data