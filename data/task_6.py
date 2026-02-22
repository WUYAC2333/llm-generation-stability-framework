# 项目 6：低检测置信度 + 多目标冲突（首轮易决策错误）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-006",
    "building_area": 2800,
    "floors": 4,
    "floor_height": 3.2,
    "structure_type": "砖混结构",
    "land_area": 2100,
    "current_far": 1.3,
    "built_year": 1990,
    "location": "杭州市萧山区钱江世纪城板块",
    "current_usage": "传统办公",
    "structural_damage": {
        "description": "疑似中度损伤/数据不足",
        "level_estimate": "中度",
        "confidence": 0.4,                    # 检测置信度极低（数据不准）
        "last_inspection": 2022
    },
    "fire_rating_current": "二级",
    "electrical_load_current": 55,
    "elevator_config": 1,
    "green_building_req": True,
    "cost_adjust_factor": 1.1,
    "base_rent": 460
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.25,
    "min_expansion_ratio": 0.13,
    "target_office_density": 8,
    "target_fire_rating": "一级",
    "target_electrical_load": 110,
    "target_far_upper": 1.8,
    "elevator_upgrade_req": 2,
    "green_building_req": True,
    "budget_max": 12_000_000,
    "budget_min": 5_800_000,
    "duration_max": 5.5,
    "duration_min": 3.5
}