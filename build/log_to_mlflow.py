import mlflow

mlflow.set_tracking_uri("http://34.250.151.22:5000")
mlflow.set_experiment("incident_agents")

with mlflow.start_run(run_name="incident_agent_package"):
    mlflow.log_param("project", "incident_agent")
    mlflow.log_param("version", 0.3)
    mlflow.log_artifact(
        local_path="C:\\Users\\vaibhava\\agenticai\\agentbuilder\\agent-platform\\deployable\\langgraph_example_v1757961993.tar.gz",
        artifact_path="packages"
    )
