from scheme_parser import parse_baseline_output
import json
import re

# 解析LLM输出的3个方案，返回方案列表（兼容单方案场景）
def parse_agent_output(text, building_params=None, target_params=None):
    # ---------- 1. 空值处理 ----------
    if text is None:
        return []
    
    # 去除文本首尾空白字符（避免空格导致的判断错误）
    stripped_text = text.strip()
    # 判断文本首尾字符
    first_char = stripped_text[0]
    last_char = stripped_text[-1]
    # 情况1：以{开头、}结尾 → 首尾加[]
    if first_char == '{' and last_char == '}':
        formatted_text = f"[{stripped_text}]"
    
    # 情况2：以[开头、]结尾 → 不修改
    elif first_char == '[' and last_char == ']':
        formatted_text = stripped_text
    
    # 情况3：其他格式 → 报错
    else:
        print(
            f"文本格式错误！仅支持{{}}或[]包裹的文本，当前文本首尾字符为：{first_char}/{last_char}\n"
            f"原始文本：{text}"
        ) 
    structured_data = json.loads(formatted_text)

    # ---------- 2. 如果输入已是列表/字典，直接适配 ----------
    if isinstance(structured_data, list):
        schemes = []
        for item in structured_data:
            if isinstance(item, dict):
                parsed = parse_baseline_output(json.dumps(item), building_params, target_params)
                if parsed:
                    schemes.append(parsed)
        return schemes
    elif isinstance(structured_data, dict):
        parsed = parse_baseline_output(json.dumps(structured_data), building_params, target_params)
        return [parsed] if parsed else []
    else:
        # 提取文本内容（兼容带content属性的对象）
        if hasattr(structured_data, "content"):
            structured_data = structured_data.content
        if not isinstance(structured_data, str):
            return []

        # ---------- 3. 核心修改：优先匹配双重大括号 {{}} 包裹的方案 ----------
        # 正则匹配 {{ 开始、}} 结束的所有文本块（非贪婪匹配）
        # 正则解释：\{\{ 匹配开头{{，(.*?) 非贪婪匹配中间内容，\}\} 匹配结尾}}
        pattern = r'\{\{(.*?)\}\}'
        # re.DOTALL 让 . 匹配换行符，兼容JSON内的换行
        scheme_matches = re.findall(pattern, structured_data, re.DOTALL)
        
        # 兜底：若双括号匹配不到，降级为原有单括号匹配逻辑
        if not scheme_matches:
            pattern_fallback = r'\{[^{}]*\}'
            scheme_matches = re.findall(pattern_fallback, structured_data, re.DOTALL)
            # 若仍无结果，尝试提取整个JSON
            if not scheme_matches:
                start = structured_data.find("{")
                end = structured_data.rfind("}")
                if start != -1 and end != -1:
                    scheme_matches = [structured_data[start:end+1]]

        # ---------- 4. 逐个解析提取到的方案文本 ----------
        schemes = []
        for idx, scheme_text in enumerate(scheme_matches):
            # 去除文本两端的空白字符（换行、空格、制表符）
            scheme_text = scheme_text.strip()
            if not scheme_text:
                continue
            
            try:
                # 调用子函数解析单个方案
                scheme = parse_baseline_output(scheme_text, building_params, target_params)
                if scheme:
                    schemes.append(scheme)
                else:
                    print(f"❌ 第 {idx+1} 个方案解析失败（无效方案）")
            except Exception as e:
                continue

        # 保证至少返回列表（即使无有效方案）
        return schemes