def compute_green_score(data, building_params):

    total_area = building_params["building_area"]
    q = data["quantity_breakdown"]

    ratio = q["energy_saving_area"] / total_area

    measure_scores = {
        "外墙保温": 7,
        "门窗更换": 6,
        "光伏": 9,
        "雨水回收": 8,
        "智能照明": 7,
        "地源热泵": 10,
        "高效灯具": 5
    }

    measure_score = sum(
        measure_scores.get(m, 0)
        for m in data["green_measures"]
    )

    return min(round(measure_score + ratio * 50, 2), 100)