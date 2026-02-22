# 项目 10：多约束冲突 + 优化优先级动态（首轮易决策错误）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-010",
    "building_area": 3800,
    "floors": 6,
    "floor_height": 3.2,
    "structure_type": "框架结构",
    "land_area": 2400,
    "current_far": 1.6,
    "built_year": 1999,
    "location": "杭州市拱墅区运河新城板块",
    "current_usage": "办公+文创",
    "structural_damage": {
        "description": "轻度裂缝/文创改造后荷载增加",
        "level_estimate": "轻度",
        "confidence": 0.82,
        "last_inspection": 2024
    },
    "fire_rating_current": "二级",
    "electrical_load_current": 70,
    "elevator_config": 1,
    "green_building_req": True,
    "cost_adjust_factor": 1.18,
    "base_rent": 470
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.19,
    "min_expansion_ratio": 0.12,
    "target_office_density": 7,
    "target_fire_rating": "一级",
    "target_electrical_load": 140,
    "target_far_upper": 1.80,
    "elevator_upgrade_req": 3,
    "green_building_req": True,
    "budget_max": 17_500_000,
    "budget_min": 6_800_000,
    "duration_max": 7,
    "duration_min": 4
}