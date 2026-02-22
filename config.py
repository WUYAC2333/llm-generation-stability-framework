import os
import dashscope
from dashscope import Generation

EXPERIMENT_ROUNDS = 5

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
RESULTS_PATH = os.path.join(PROJECT_ROOT, "experiment")

def init_dashscope():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY not found in environment variables")
    dashscope.api_key = api_key
    Generation.api_key = api_key