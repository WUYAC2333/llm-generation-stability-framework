# 项目 4：低预算 + 高电梯需求（首轮易超成本）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-004",
    "building_area": 3500,
    "floors": 7,                              # 楼层更多
    "floor_height": 3.3,
    "structure_type": "框架结构",
    "land_area": 2200,
    "current_far": 1.7,
    "built_year": 2000,                       # 建筑较新
    "location": "杭州市余杭区未来科技城板块",
    "current_usage": "科创办公",
    "structural_damage": {
        "description": "无明显损伤/仅墙面开裂",
        "level_estimate": "轻微",
        "confidence": 0.9,
        "last_inspection": 2025
    },
    "fire_rating_current": "一级",            # 消防已达标
    "electrical_load_current": 80,
    "elevator_config": 1,
    "green_building_req": True,
    "cost_adjust_factor": 1.05,                # 溢价更低
    "base_rent": 420
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.21,
    "min_expansion_ratio": 0.10,
    "target_office_density": 6,               # 密度极低（空间要求高）
    "target_fire_rating": "一级",
    "target_electrical_load": 200,            # 电力需求翻倍
    "target_far_upper": 1.9,
    "elevator_upgrade_req": 4,                # 电梯数量大幅增加
    "green_building_req": True,
    "budget_max": 16_000_000,                  # 预算极低
    "budget_min": 5_500_000,
    "duration_max": 8.2,
    "duration_min": 4
}