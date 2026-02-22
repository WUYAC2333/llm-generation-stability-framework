# main.py
import os
import logging
import time
import ast
from datetime import datetime
from typing import Dict, Tuple, Any

from experiment import run_experiment, evaluate_exported_schemes, exported_schemes
from config import DATA_PATH, RESULTS_PATH, EXPERIMENT_ROUNDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_task_params(file_path) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    tree = ast.parse(file_content)
    building_params = None
    target_params = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == "building_params":
                        building_params = eval(
                            compile(ast.Expression(node.value), "<string>", "eval")
                        )
                    elif target.id == "target_params":
                        target_params = eval(
                            compile(ast.Expression(node.value), "<string>", "eval")
                        )

    if building_params is None or target_params is None:
        raise ValueError("未找到 building_params 或 target_params")

    return building_params, target_params


def run_single_task(task_filename: str):
    """
    供 FastAPI 调用的核心函数
    """
    file_path = os.path.join(DATA_PATH, task_filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{task_filename} 不存在")

    building_params, target_params = load_task_params(file_path)
    logger.info(f"成功读取任务 {task_filename} 参数")

    all_round_results = []

    for round_num in range(1, EXPERIMENT_ROUNDS + 1):
        logger.info(f"===== 开始第 {round_num}/{EXPERIMENT_ROUNDS} 轮实验 =====")
        baseline_result, agent_results = run_experiment(
            building_params, target_params
        )
        logger.info(f"任务 {task_filename} 实验第 {round_num}/{EXPERIMENT_ROUNDS} 轮运行完成")

        all_round_results.append({
            "round": round_num,
            "baseline": baseline_result,
            "agent": agent_results
        })

    return {
        "task": task_filename,
        "results": all_round_results
    }


def main():
    char_dict = {
        "1": "A",
        "2": "B",
        "3": "C",
        "4": "D",
        "5": "E"
    }
    current_time = datetime.now()
    simple_format = current_time.strftime("%Y%m%d%H%M%S")
    # 轮流运行任务（只运行任务1当作示例）
    files = os.listdir(DATA_PATH)
    flag = True
    for f in files:
        if flag: 
            logger.info(f"\n===== 开始运行任务 ({f}) =====")
            logger.info(f"\n仅运行任务1当作示例")
            flag = False
            results_dict = run_single_task(f)
            # 记录实验结果
            file_name_without_ext = f.rsplit('.', maxsplit=1)[0]
            all_round_results = results_dict["results"]
            record_str = ""
            for round_results in all_round_results:
                round_num = round_results["round"]
                char = char_dict[f"{str(round_num)}"]
                baseline_var_name = f"{file_name_without_ext}_baseline_scheme_{char}"
                agent_var_name_1 = f"{file_name_without_ext}_agent_scheme_{char}1"
                agent_var_name_2 = f"{file_name_without_ext}_agent_scheme_{char}2"
                agent_var_name_3 = f"{file_name_without_ext}_agent_scheme_{char}3"
                baseline_scheme = round_results["baseline"]
                agent_scheme_1 = round_results["agent"][0]
                agent_scheme_2 = round_results["agent"][1]
                agent_scheme_3 = round_results["agent"][2]
                record_str += f"{baseline_var_name} = {baseline_scheme}\n"
                record_str += f"{agent_var_name_1} = {agent_scheme_1}\n"
                record_str += f"{agent_var_name_2} = {agent_scheme_2}\n"
                record_str += f"{agent_var_name_3} = {agent_scheme_3}\n\n"
            with open(os.path.join(RESULTS_PATH, f"results_{simple_format}.py"), "a", encoding="utf-8") as file:
                file.write(record_str)

    code_to_write = '''
import re

# 全部方案字典
exported_schemes = {}
# 定义变量名匹配规则：匹配res_1_1的正则规则
AGENT_PATTERN = re.compile(r'^task_\d{1,2}_(baseline|agent)_scheme_(A|B|C|D|E)\d*$')
for var_name in dir():
    if not var_name.startswith('__') and AGENT_PATTERN.match(var_name):
        exported_schemes[var_name] = locals()[var_name]
'''
    with open(os.path.join(RESULTS_PATH, f"results_{simple_format}.py"), "a", encoding="utf-8") as file:
        file.write(code_to_write)
    
        # 调用 evaluate_exported_schemes
    print("由于实验运行时间较长，以已完成实验数据为例进行指标计算：")
    evaluation= evaluate_exported_schemes(exported_schemes)
    logger.info(evaluation)
    return

if __name__ == "__main__":
    main()