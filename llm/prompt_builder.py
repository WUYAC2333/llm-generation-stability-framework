from typing import Dict, Any

def build_baseline_prompt(building_params: Dict[str, Any],
                          target_params: Dict[str, Any]) -> str:

    area = building_params["building_area"]
    land_area = building_params["land_area"]
    struct_type = building_params["structure_type"]
    max_expansion_ratio = target_params["max_expansion_ratio"]
    max_budget = target_params["budget_max"]
    min_budget = target_params["budget_min"]
    max_duration = target_params["duration_max"]
    target_fire = target_params["target_fire_rating"]
    elevator_target = target_params["elevator_upgrade_req"]
    built_year = building_params["built_year"]
    location = building_params["location"]
    cost_adjust_factor = building_params["cost_adjust_factor"]
    base_rent = building_params["base_rent"]

    min_expansion_ratio = 0.1  # 10%下限
    min_expansion_area = int(area * min_expansion_ratio)  # 最小扩容面积
    max_expansion_area = int(area * max_expansion_ratio)  # 最大扩容面积
    max_far = target_params.get("target_far_upper", 1.8)  # 容积率上限
    max_total_area = int(max_far * land_area)  # 最大总建筑面积（容积率约束）
    max_allowed_expansion = max_total_area - area  # 容积率限制下的最大扩容面积
    final_max_expansion = min(max_expansion_area, max_allowed_expansion)  # 双重约束：扩容比例+容积率

    prompt = f"""
    你是资深建筑改造工程师，熟悉杭州2025年改造市场价（申花板块溢价10%）。请生成符合以下条件的老旧办公楼改造方案，严格按JSON输出（无额外文本）：
【绿色建筑说明】
1. 绿色建筑为连续评分模型（0~100分），每增加1项绿建措施增加的分数及成本如下：
- 外墙保温：7分，80 元/㎡,    # 薄抹灰保温，办公楼常用
- 门窗更换：6分，220 元/㎡,    # 断桥铝+中空玻璃
- 光伏：9分，180 元/㎡,    # 屋顶光伏摊到建筑面积
- 雨水回收：8分，35 元/㎡,    # 含管网+小水箱
- 智能照明：7分，45 元/㎡,    # 感应+智能面板
- 地源热泵：10分，320 元/㎡,    # 打井+机房摊面积（高价值项）
- 高效灯具：5分，20 元/㎡     # 替换LED基础款
- 节能面积得分 = 节能面积比例 × 50分（节能面积比例 = 节能改造面积÷建筑面积）
2. 绿色建筑得分=绿建措施得分+节能面积得分，总分≤100，必须≥40分
3. 绿建措施最少应包含[外墙保温, 门窗更换]。

【核心工程条件（高复杂度）】
- 建筑背景：杭州{location} {struct_type}办公楼，{built_year}年建成，面积{area}㎡，用地{land_area}㎡，1995年建筑存在轻度结构裂缝（置信度75%）
- 区位成本：申花板块成本系数{cost_adjust_factor}，所有直接成本需乘以该系数
- 硬性约束：
  1. 扩容≤{max_expansion_ratio}且≥0.1（必须扩容10%以上）
  2. 容积率≤{target_params['target_far_upper']}
  3. 预算{min_budget}~{max_budget}元（申花板块溢价后）
  4. 工期4~{max_duration}个月（大面积项目>2500㎡基础效率1200㎡/月，不可压缩）
  5. 消防升级至{target_fire}（依据《杭州市既有建筑消防技术导则（2023）》第5.2条）
  6. 电梯≥{elevator_target}台，无障碍改造符合《杭州市无障碍环境建设条例》第12条
  7. 90年代建筑扩容>0%必须做结构加固，且成本上浮15%
  8. 改造后该建筑的基础租金为{base_rent}元 /㎡/ 12个月
  9. 年收益= {base_rent}*（建筑扩容前面积*（1+expansion_ratio））*绿色建筑溢价，应尽量使年收益更高
  10. expansion_ratio对租金有正向影响，但存在边际递减效应：当expansion_ratio超过0.12后，单位面积新增带来的租金提升幅度略微降低；当expansion_ratio超过0.17后，单位面积新增带来的租金提升幅度明显降低，应合理权衡扩容规模与投资回报。
  11. 绿色建筑评分对租金溢价具有边际递减特征：低分段（60分以下）提升对市场吸引力影响显著，高分段（80分以上）提升对租金影响较小，应避免为追求极高绿建分数而产生过高成本。
  12. 机电改造面积应随扩容面积增长，mechanical_electrical_area ≥ total_area_after * 75%

  【核心约束规则】
1. 结构安全：{built_year}年建成建筑，扩容>0%必须做结构加固，且成本上浮15%（申花板块额外×{cost_adjust_factor}）；
2. 工期效率：>2500㎡项目基础效率1200㎡/月，不可压缩，总工期≤{target_params['duration_max']}个月；
3. 扩容规则（强制）：
   • 扩容比例：严格≥{min_expansion_ratio*100}%且≤{max_expansion_ratio*100}%（即≥{min_expansion_area}㎡且≤{final_max_expansion}㎡）；
   • 90年代框架结构扩容>10%时工期+0.5个月；
   • 最终总建筑面积≤{max_total_area}㎡（容积率≤{max_far}），超出则方案无效；
4. 容积率规则（强制）：
   • 扩容后容积率=总建筑面积/用地面积 ≤ {max_far}；
   • 总建筑面积=原有面积({area}㎡)+扩容面积 ≤ {max_total_area}㎡；
5. 合规依据：消防符合《杭州市既有建筑消防技术导则（2023）》第5.2条，无障碍符合《杭州市无障碍环境建设条例》第12条。

【输出要求（强制遵守，否则方案无效）】
1. 必须输出 duration_calculation（体现并行施工/工期压缩逻辑）；
2. engineering_rationale 需清晰说明多目标优化逻辑+合规性
3. 约束满足率必须达到100%，所有校验项均为PASS；
4. 核心字段强制要求：
   • expansion_ratio：严格≥{min_expansion_ratio}且≤{max_expansion_ratio}；
   • far_after：严格≤{max_far}（保留2位小数）；
   • expansion_area：≥{min_expansion_area}㎡且≤{final_max_expansion}㎡；
   • total_area_after：≤{max_total_area}㎡；
5. 输出为标准JSON格式，无截断、无中文标点、字段值为数字类型（非字符串）；

【工期计算规则】
- 基础工期=建筑面积/1200
- 扩建工期=扩建面积/600
- 绿建工期 = 绿建措施时间+节能面积相关时间，每增加 1 个绿建措施  +0.3 个月，节能面积相关时间 = 节能面积比例*1.5
- 每增加1台电梯，改造工期增加0.5个月
- 缓冲工期=0.1*（基础+扩建+绿色+电梯）个月
- 总工期=基础+扩建+绿色+电梯+缓冲，且≥4个月、≤{max_duration}个月

【输出要求（完整结构化）】
{{
  "expansion_ratio": 0.~{max_expansion_ratio}的浮点数（≥0.1），应该尽量尝试不同可能，不允许取0.1、0.2和0.15这三个极限值和中间值
  "expansion_area": 扩建面积（整数）,
  "total_area_after": 扩容后总面积（整数）,
  "far_after": 容积率（保留2位小数）,
  "duration": 工期（浮点数，月）,
  "fire_rating_final": "{target_fire}",
  "green_measures": 包含上文定义的若干绿建措施的列表，
  "elevator_after": {elevator_target},
  "quantity_breakdown": {{
    "structure_reinforce_area": 结构加固面积（整数）,
    "fire_upgrade_area": 消防升级面积（整数）,
    "interior_renovation_area": 室内改造面积（整数）,
    "expansion_area": 扩建面积（整数）,
    "mechanical_electrical_area": 机电改造面积（整数）,
    "energy_saving_area": 节能改造面积（整数）,
    "barrier_free_area": 无障碍改造面积（整数）,
    "new_elevator_count": 电梯新增数量（整数）
  }},
  "duration_calculation": {{
    "base_duration": 基础改造工期,
    "expansion_duration": 扩建工期,
    "green_duration": 绿建工期 = 绿建措施时间+节能面积相关时间,
    "elevator_duration": 0.5*新增电梯数量,
    "buffer_duration": 0.1*（基础+扩建+绿色+电梯）个月,
    "estimated_total_duration": 估算总工期
  }},
  "engineering_rationale": "300字专业说明，包含结构安全、绿色建筑策略、成本溢价、工期效率等逻辑"
}}

【关键提醒】
1. 所有数值必须严格按杭州2025市场价+申花板块溢价计算，禁止随意填写

【格式强制要求】
1. 严格使用双引号包裹所有JSON属性名和字符串值，禁止用单引号；
2. 每个键值对后必须加逗号（最后一个键值对除外）；
3. 数值（预算、工期、面积等）直接写数字，不要加引号；
4. 仅输出JSON，无任何前置文本（如"方案如下："）和后置文本。用于该接口赔偿mm

【成本说明】
- 各项工程单价将由系统按杭州2025市场价统一计算
- LLM只需给出工程量和数量
- 禁止输出任何金额
    """
    return prompt

def build_agent_prompt(building_params: Dict[str, Any],
                          target_params: Dict[str, Any]) -> str:
    prompt = build_baseline_prompt(building_params, target_params)
    prompt += f"""
    【工程量决策自由度说明】
1. 优化优先级必须通过调整工程量比例体现
2. 工程量优化范围：
消防升级：≥80%面积
结构加固：≥90%面积
机电改造：≥75%面积
节能改造：60%~100%面积

【多方案搜索要求】
1. 本轮生成3个差异化方案，对应3种不同决策偏好：
方案A（成本优先）：
- 以低成本为首要目标
- 绿建措施数量控制在最低满足分数要求
- 工期允许略长但不超限

方案B（平衡型）：
- 平衡成本、绿建与收益
- 绿建措施适中

方案C（绿色优先）：
- 追求更高绿建要求
- 节能面积应相对更高
- 增加绿建措施种类
- 接受成本增加
- 工期可适度延长

2. 不同偏好必须通过工程量比例变化体现（至少2个指标差异≥10%）：
3. 不自动修正为最低边界解
4. 所有方案必须独立满足约束
"""
    
    return prompt