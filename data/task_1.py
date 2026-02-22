# 基本建筑条件（增强：引入不确定性与检测置信度）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-001",
    "building_area": 3000,                    # ㎡
    "floors": 5,
    "floor_height": 3.2,                      # m
    "structure_type": "框架结构",
    "land_area": 2000,                        # ㎡
    "current_far": 1.5,
    "built_year": 1995,
    "location": "杭州市拱墅区申花板块",
    "current_usage": "传统办公",
    "structural_damage": {
        "description": "轻度裂缝/梁柱碳化",
        "level_estimate": "轻度",             # LLM需据此判断，但可能不准
        "confidence": 0.75,                   # 检测报告可信度
        "last_inspection": 2024
    },
    "fire_rating_current": "二级",
    "electrical_load_current": 50,            # kW
    "elevator_config": 1,                     # 台
    "green_building_req": True,
    "cost_adjust_factor": 1.1,
    "base_rent": 520
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.18,
    "min_expansion_ratio": 0.11,
    "target_office_density": 8,               # ㎡/人
    "target_fire_rating": "一级",
    "target_electrical_load": 120,            # kW
    "target_green_rating": "二星",            # 必须通过组合措施达标
    "target_far_upper": 1.80,
    "elevator_upgrade_req": 2,
    "green_building_req": True,
    "budget_max": 13_900_000,
    "budget_min": 6_000_000,
    "duration_max": 7.0,        # 月
    "duration_min": 4.0,        # 月
}