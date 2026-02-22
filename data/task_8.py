# 项目 8：高预算 + 绿色优先级最高（首轮易选高成本绿色措施）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-008",
    "building_area": 4200,                    # 面积最大
    "floors": 8,
    "floor_height": 3.2,
    "structure_type": "框架-剪力墙结构",
    "land_area": 2800,
    "current_far": 1.5,
    "built_year": 1996,
    "location": "杭州市西湖区西溪板块",
    "current_usage": "高端办公",
    "structural_damage": {
        "description": "轻度裂缝/屋面漏水",
        "level_estimate": "轻度",
        "confidence": 0.8,
        "last_inspection": 2024
    },
    "fire_rating_current": "二级",
    "electrical_load_current": 75,
    "elevator_config": 2,
    "green_building_req": True,
    "cost_adjust_factor": 1.3,                 # 西溪板块溢价最高
    "base_rent": 690
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.26,
    "min_expansion_ratio": 0.15,
    "target_office_density": 5,               # 密度极低（高端办公）
    "target_fire_rating": "一级",
    "target_electrical_load": 160,
    "target_far_upper": 1.8,
    "elevator_upgrade_req": 4,
    "green_building_req": True,
    "budget_max": 20_300_000,                 # 预算充足
    "budget_min": 10_000_000,
    "duration_max": 8.1,
    "duration_min": 5.0
}