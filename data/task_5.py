# 项目5：混合用途 + 高 FAR 约束（首轮易超 FAR）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-005",
    "building_area": 3200,
    "floors": 5,
    "floor_height": 3.5,
    "structure_type": "框架结构",
    "land_area": 2100,
    "current_far": 1.65,
    "built_year": 1998,
    "location": "杭州市上城区钱江新城板块",
    "current_usage": "办公+商业",
    "structural_damage": {
        "description": "轻度裂缝/管道老化",
        "level_estimate": "轻度",
        "confidence": 0.78,
        "last_inspection": 2024
    },
    "fire_rating_current": "二级",
    "electrical_load_current": 70,
    "elevator_config": 2,
    "green_building_req": True,
    "cost_adjust_factor": 1.25,
    "base_rent": 625
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.18,
    "min_expansion_ratio": 0.10,
    "target_office_density": 8,
    "target_fire_rating": "一级",
    "target_electrical_load": 130,
    "target_far_upper": 1.75,
    "elevator_upgrade_req": 3,
    "green_building_req": True,
    "budget_max": 15_000_000,
    "budget_min": 6_500_000,
    "duration_max": 7.5,
    "duration_min": 4.5,
}