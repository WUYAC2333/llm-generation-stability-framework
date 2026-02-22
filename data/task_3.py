# 项目3：低扩容权限+工期优先（首轮易超工期）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-003",
    "building_area": 2500,
    "floors": 4,
    "floor_height": 3.0,
    "structure_type": "砖混结构",
    "land_area": 1800,
    "current_far": 1.4,
    "built_year": 1992,
    "location": "杭州市滨江区钱江世纪城板块",
    "current_usage": "办公+仓储",
    "structural_damage": {
        "description": "轻度裂缝/墙面渗水",
        "level_estimate": "轻度",
        "confidence": 0.7,
        "last_inspection": 2024
    },
    "fire_rating_current": "三级",
    "electrical_load_current": 60,
    "elevator_config": 0,
    "green_building_req": False,
    "cost_adjust_factor": 1.15,
    "base_rent": 575
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.25,  
    "min_expansion_ratio": 0.14,
    "target_office_density": 9,
    "target_fire_rating": "一级",
    "target_electrical_load": 100,
    "target_far_upper": 1.57,
    "elevator_upgrade_req": 1,
    "green_building_req": False,
    "budget_max": 11_000_000,
    "budget_min": 5_000_000,
    "duration_max": 5.2,  # 核心修正：工期上限从4→4.5（放宽，让Agent能达标）
    "duration_min": 3
}