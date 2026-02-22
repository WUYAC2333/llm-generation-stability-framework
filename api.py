from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import run_single_task

app = FastAPI(title="Building Scheme Experiment API")

class TaskRequest(BaseModel):
    task_filename: str


@app.post("/run-task")
def run_task(req: TaskRequest):
    try:
        result = run_single_task(req.task_filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))