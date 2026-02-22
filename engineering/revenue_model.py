def compute_annual_income(data, building_params):

    total_area = building_params["building_area"]
    base_rent = building_params["base_rent"]

    green_score = data["green_score"]
    expansion_ratio  = data["expansion_ratio"]
    expansion_area = expansion_ratio*total_area

    # 绿色溢价：前60分：每10分涨6%，60-80：每10分涨2.5%，80以上：每10分涨1.5%
    if green_score <= 60:
        green_premium = 1 + 0.006 * green_score
    elif green_score <= 80:
        green_premium = 1 + 0.006*60 + 0.0025*(green_score-60)
    else:
        green_premium = 1 + 0.006*60 + 0.0025*20 + 0.0015*(green_score-80)

    # 扩容直接增加面积收益(扩容溢价)，但具有边际递减效应
    effective_area = total_area + expansion_area
    if expansion_ratio <= 0.12:
        # 0~12%区间：线性增长，边际收益最高
        expansion_premium = 1 + 0.8 * expansion_ratio
    elif 0.12 < expansion_ratio <= 0.17:
        # 12%~17%区间：先算10%的基础溢价，再算超出10%部分的低边际收益
        expansion_premium = 1 + 0.8 * 0.12 + 0.4 * (expansion_ratio - 0.12)
    else:
        # 17%以上区间：先算前17%的溢价，再算超出17%部分的最低边际收益
        expansion_premium = 1 + 0.8 * 0.12 + 0.4 * 0.05 + 0.1 * (expansion_ratio - 0.17)
    annual_income = base_rent * effective_area * green_premium*expansion_premium

    return round(annual_income, 2)


def compute_npv(data, years=10, discount_rate=0.08):

    income = data["annual_income"]
    cost = data["budget"]

    npv_income = sum(
        income / ((1+discount_rate)**t)
        for t in range(1, years+1)
    )

    return round(npv_income - cost, 2)