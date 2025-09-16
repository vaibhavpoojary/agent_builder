# eval/evaluator.py
import time
import requests
import mlflow
from utils.mlflow_utils import client

def call_agent(endpoint_url, prompt):
    start = time.time()
    r = requests.post(endpoint_url, json={"prompt": prompt}, timeout=30)
    latency = (time.time() - start) * 1000
    resp = r.json().get("result")
    return resp, latency

def run_evaluation(endpoint_url, test_prompts, registered_model_name, run_name="eval-run"):
    mlflow.set_experiment("agent-evals")
    with mlflow.start_run(run_name=run_name):
        for i, p in enumerate(test_prompts):
            resp, latency = call_agent(endpoint_url, p)
            # compute success/quality (this can be manual or automated)
            success = 1 if resp and len(resp) > 3 else 0
            mlflow.log_metric("latency_ms", latency, step=i)
            mlflow.log_metric("success", success, step=i)
            mlflow.log_text(resp, artifact_file=f"resp_{i}.txt")
