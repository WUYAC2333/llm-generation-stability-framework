# 项目9：工期极严+无结构损伤（首轮易超工期）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-009",
    "building_area": 2200,
    "floors": 3,
    "floor_height": 3.0,
    "structure_type": "框架结构",
    "land_area": 1500,
    "current_far": 1.45,
    "built_year": 2010,
    "location": "杭州市钱塘区下沙板块",
    "current_usage": "办公",
    "structural_damage": {
        "description": "无损伤/全新维护",
        "level_estimate": "无",
        "confidence": 0.98,
        "last_inspection": 2025
    },
    "fire_rating_current": "一级",
    "electrical_load_current": 85,
    "elevator_config": 2,
    "green_building_req": True,
    "cost_adjust_factor": 1.05,
    "base_rent": 440
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.30,
    "min_expansion_ratio": 0.10,
    "target_office_density": 8,
    "target_fire_rating": "一级",
    "target_electrical_load": 120,
    "target_far_upper": 1.8,
    "elevator_upgrade_req": 2,
    "green_building_req": True,
    "budget_max": 7_800_000,
    "budget_min": 4_500_000,
    "duration_max": 5.3,  
    "duration_min": 2.5,
    "duration_reasonable_lower": 2.8  # 新增：工期合理下限，避免"工期不合理"报错
}