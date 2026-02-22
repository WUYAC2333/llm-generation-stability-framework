# 项目 7：无绿色要求 + 机电改造优先级最高（首轮易忽略核心模块）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-007",
    "building_area": 3600,
    "floors": 6,
    "floor_height": 3.2,
    "structure_type": "框架结构",
    "land_area": 2300,
    "current_far": 1.55,
    "built_year": 2005,                       # 建筑较新
    "location": "杭州市临平区临平新城板块",
    "current_usage": "办公",
    "structural_damage": {
        "description": "无明显损伤",
        "level_estimate": "无",
        "confidence": 0.95,
        "last_inspection": 2025
    },
    "fire_rating_current": "一级",
    "electrical_load_current": 90,
    "elevator_config": 2,
    "green_building_req": False,              # 无绿色要求
    "cost_adjust_factor": 1.08,
    "base_rent": 425
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.22,
    "min_expansion_ratio": 0.12,
    "target_office_density": 8,
    "target_fire_rating": "一级",
    "target_electrical_load": 180,            # 机电需求翻倍
    "target_far_upper": 1.9,
    "elevator_upgrade_req": 2,
    "green_building_req": False,
    "budget_max": 13_500_000,
    "budget_min": 6_200_000,
    "duration_max": 7,
    "duration_min": 4
}