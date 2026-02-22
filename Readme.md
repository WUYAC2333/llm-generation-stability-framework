# 项目 3｜面向复杂多约束任务的 LLM 生成稳定性评估与优化框架 —— 以杭州老旧办公楼改造为实验场景

> (本作品集包含三个基于 FastAPI 服务化封装的 AIGC 系统，分别聚焦生成、检索增强与评估任务，均支持 Swagger 交互测试。)

## 1. 项目定位

本项目关注的核心问题不是 Agent 本身，而是：

> **在复杂多约束工程任务中，如何提升 LLM 生成结果的稳定性、可控性与收益表现，并通过量化实验验证其有效性。**

实验场景设定为：**杭州老旧办公楼改造决策问题**（预算、容积率、消防、绿建等级、工期等多约束耦合）。

本项目目标：

- 构建真实工程约束环境
- 分析 LLM 在多约束场景下的失败模式
- 设计可控生成框架
- 用结构化实验验证 Agent 相比 Baseline 的提升

---

## 2. 问题定义

建筑改造问题具有典型特征：

- 多目标（成本 / 收益 / 绿建评分）
- 强硬约束（容积率 / 消防等级 / 工期合理性）
- 成本与收益非线性耦合
- 现实政策约束嵌入

典型难点：

- LLM 易出现“目标驱动幻觉”
- 成本优化不现实
- 数值自洽问题
- 多轮生成波动大

本项目将其抽象为：

> **复杂多约束连续优化生成任务**

---

## 3. 系统架构

### 3.1 Baseline（Single-shot）

单次 LLM 生成完整方案 → 规则校验 → 统计结果

问题：

- 成本虚构
- 极端数值
- 波动性高
- 成功率不稳定

---

### 3.2 Agent 框架（Generate-and-Select）

核心思想：

> 生成候选集 → 规则校验 → 确定性定价 → 多目标选择

结构演化：

**V1：LLM 全权生成**

LLM → 金额 → Python求和

问题：

- 成本优化不现实
- 数值幻觉

**V2：强化 Prompt 约束**

成本结构更完整
优化幅度收敛

仍存在：

- 数值自洽问题
- 预算驱动波动

**V3：确定性定价层（Deterministic Pricing Layer）**

架构升级：

```
LLM → 输出工程量
Cost Engine → 确定性计算成本
Validator → 区间校验
```

优势：

- 剥离金额生成权
- 降低幻觉风险
- 提高可控性

---

## 4. 核心工程建模

### 4.1 非线性成本模型

- 绿色溢价和扩容溢价均采用分段非线性计算逻辑
- 绿色溢价按绿色评分划分为≤60、60-80、＞80 三个区间，扩容溢价按扩容比例划分为≤12%、12%-17%、＞17% 三个区间
- 最终年度收益由基准租金、有效面积及两类溢价共同决定

---

### 4.2 工期关键路径模型

考虑：

- 主体改造效率
- 扩建周期
- 绿建审批（+1个月）
- 电梯安装（+0.5个月/部）
- 规划缓冲期（不可压缩）

---

### 4.3 工程级规则校验

包括：

- 容积率合规
- 预算合理性
- 工期合理区间

---

### 4.4 多目标优化

构建：

- NPV 收益模型
- 边际递减扩容收益
- 绿建收益递减
- 成本-收益-绿建三目标冲突

本质上：

> 一个简化版多目标投资决策系统

---

## 5. 实验设计

### 5.1 实验规模

- 10 组复杂任务参数
- 每组 5 轮生成
- 每轮：
  - 1 Baseline
  - 3 Agent 策略

总样本：

`10 × 5 × 4 = 200 个生成结果`

---

### 5.2 评价指标

- 单样本可行率
- 轮级成功率
- 平均 NPV
- 收益变异系数（CV）
- 相对提升率

---

## 6. 实验结果

### 6.1 可行性

| 指标         | Baseline | Agent |
| ------------ | -------- | ----- |
| 单样本可行率 | 66%      | 53%   |
| 轮级成功率   | 66%      | 100%  |

虽然 Agent 单样本可行率略低，但由于采用多策略并行生成机制：

> 每轮必有一个可行解

显著降低复杂任务下的失败风险。

---

### 6.2 收益水平（NPV）

- Baseline 平均 NPV：3,526,076
- Agent 平均 NPV：4,643,466

提升：

> +31.7%

---

### 6.3 稳定性（变异系数 CV）

- Baseline：0.53
- Agent 成本优先：0.54
- Agent 平衡策略：0.24
- Agent 绿建优先：0.25

说明：

> agent 在平衡型与绿色优先策略下显著降低了收益波动，在维持较高收益水平的同时增强了输出稳定性。

---

### 6.4 策略差异性

- 成本优先：+39.8%
- 平衡型：+29.9%
- 绿建优先：-5.5%

> 该结果符合预期：不同优化目标对应不同收益结构，系统能够真实反映目标冲突与多目标权衡关系，而非简单趋同于单一高收益方向。

---

## 7. 核心结论

在复杂多约束生成任务中，引入：

- 多策略并行生成
- 确定性定价层
- 自动规则校验
- 多轮统计评估

可实现：

- 轮级成功率 100%
- 收益提升 31.7%
- 稳定性显著增强
- 多目标权衡可解释

证明：

> Agent 框架在复杂工程生成场景下具备更高工程可靠性与优化能力。

---

## 8. 工程能力体现

本项目体现的能力：

- LLM 工程化控制
- 生成失败模式分析
- 规则引擎设计
- 确定性数值建模
- 多轮实验统计评估
- 复杂系统模块解耦
- FastAPI 工程封装

---

## 9. 运行方式（API）

本项目已封装为 FastAPI 服务。

### 9.1 启动

1. 激活 Conda 环境 （请替换为你的实际环境名）

`conda activate python39`

2. 安装依赖

`pip install -r requirements.txt`

3. 设置 DASHSCOPE_API_KEY（如需要）

Windows：
`set DASHSCOPE_API_KEY=你的key`

Mac/Linux：
`export DASHSCOPE_API_KEY=你的key`

4. 启动 API 服务

`uvicorn api:app --reload`

5. 打开接口文档

浏览器访问：

`http://127.0.0.1:8000/docs`

即可通过 Swagger 页面调用接口。

---

### 9.2 调用接口

Swagger 页面调用接口正确使用步骤：

- 点击 POST /run-task
- 点击右侧 Try it out
- 在 JSON 里输入：
  `{ "task_filename": "task_1.py" }`
- 点击 Execute

返回 200 即代表实验运行成功。

生成方案示例：

```
{
"expansion_ratio": 0.15,
"expansion_area": 450,
"total_area_after": 3450,
"far_after": 1.73,
"budget": 8496000,
"duration": 5.25,
"included_modules": [
"结构加固",
"消防系统升级",
"办公空间扩容",
"机电系统改造",
"节能改造",
"无障碍设施改造"
],
"fire_rating_final": "一级",
"green_measures": [
"外墙保温",
"门窗更换",
"光伏"
],
"elevator_after": 2,
"cost_breakdown": {
"structure_reinforce": 2047500,
"fire_upgrade": 726000,
"interior_renovation": 2310000,
"expansion": 891000,
"mechanical_electrical": 1815000,
"energy_saving": 1320000,
"barrier_free": 264000,
"elevator": 1320000,
"design_management": 1283220,
"tax_and_fees": 1077904,
"total_cost": 13054624
},
"duration_calculation": {
"base_duration": 2.5,
"expansion_duration": 0.8,
"green_duration": 1.0,
"elevator_duration": 0.5,
"buffer_duration": 1.0,
"estimated_total_duration": 5.8,
"scheme_duration": 5.25,
"rationality": "合理"
},
"constraint_validation": {
"expansion_constraint": "PASS",
"far_constraint": "PASS (1.73 ≤ 1.8)",
"structure_safety": "PASS",
"budget_constraint": "PASS",
"budget_rationality": "PASS",
"duration_rationality": "PASS",
"module_completeness": "PASS",
"fire_rating": "PASS",
"green_requirement": "PASS",
"overall_validity": "PASS",
"constraint_satisfaction_rate": 1.0
},
"engineering_rationale": "本方案针对杭州拱墅区申花板块的一栋1995年建成的框架结构办公楼进行改造。考虑到建筑存在轻度结构裂缝，且需扩容至原面积的15%，我们首先进行了必要的结构加固工作，确保了建筑的安全性。同时，为满足绿色二星标准，采取了外墙保温、门窗更换及安装光伏板等措施，有效提升了建筑能效。在成本方面，由于申花板块的成本系数为1.1，并且对于90年代建筑扩容时需要额外增加15%的结构加固费用，因此总预算控制在了8496000元内。工期方面，通过合理安排各项工程进度，包括基础改造、扩建、绿色认证以及电梯安装等环节，最终确定整个项目可以在5.25个月内完成，符合既定要求。"
}
```
