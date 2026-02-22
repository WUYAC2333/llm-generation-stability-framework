# 项目 2：高结构损伤 + 绿色三星要求（首轮易超预算）
building_params = {
    "building_id": "HZ-OLD-OFFICE-2026-002",
    "building_area": 3700,                     # 略微减少面积，降低初始成本
    "floors": 6,
    "floor_height": 3.2,
    "structure_type": "框架-剪力墙结构",
    "land_area": 2500,
    "current_far": 1.6,
    "built_year": 1988,
    "location": "杭州市西湖区文三路板块",
    "current_usage": "传统办公",
    "structural_damage": {
        "description": "中度裂缝/梁柱腐蚀/楼板开裂",
        "level_estimate": "中度",
        "confidence": 0.85,
        "last_inspection": 2023
    },
    "fire_rating_current": "二级",
    "electrical_load_current": 45,
    "elevator_config": 1,
    "green_building_req": True,
    "cost_adjust_factor": 1.1,                 # 略微降低溢价
    "base_rent": 450
}

target_params = {
    "expansion_allowed": True,
    "max_expansion_ratio": 0.20,               # 最大扩容比例
    "min_expansion_ratio": 0.10,
    "target_office_density": 7,
    "target_fire_rating": "一级",
    "target_electrical_load": 150,
    "target_far_upper": 1.80,                  # 容积率上限，FAR 上限
    "elevator_upgrade_req": 3,
    "green_building_req": True,
    "budget_max": 17_500_000,                  # 提高上限，给 Agent 调整空间
    "budget_min": 4_000_000,
    "duration_max": 7,
    "duration_min": 4.5
}