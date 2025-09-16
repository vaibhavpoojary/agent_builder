# utils/mlflow_utils.py
import os
import mlflow
from mlflow.client import MlflowClient

MLFLOW_URI = os.environ.get("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(MLFLOW_URI)
client = MlflowClient(tracking_uri=MLFLOW_URI)

def log_artifact_and_register(experiment_name, run_name, local_artifact_path, registered_model_name, artifact_path_in_run="artifact"):
    # Ensure experiment exists
    try:
        experiment = client.get_experiment_by_name(experiment_name)
    except Exception:
        raise
    if experiment is None:
        experiment_id = client.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id

    with mlflow.start_run(experiment_id=experiment_id, run_name=run_name) as run:
        run_id = run.info.run_id
        # log artifact(s)
        mlflow.log_artifact(local_artifact_path, artifact_path=artifact_path_in_run)
        # build the URI to the logged artifact
        artifact_uri = mlflow.get_artifact_uri(artifact_path_in_run)
        # Register the model (create registered model if needed)
        try:
            client.create_registered_model(registered_model_name)
        except Exception:
            pass  # already exists
        # create a new model version pointing to this run's artifact
        model_src = f"{artifact_uri}/{Path(local_artifact_path).name}"
        mv = client.create_model_version(
            name=registered_model_name,
            source=model_src,
            run_id=run_id
        )
        return {"run_id": run_id, "model_version": mv.version, "model_source": model_src}
