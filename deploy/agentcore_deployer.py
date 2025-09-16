# deploy/agentcore_deployer.py
import subprocess
from pathlib import Path
import re

def agentcore_configure(tarball_path: Path, agent_name: str, execution_role_arn=None):
    tarball_str = str(tarball_path.resolve())  # absolute path
    cmd = f'agentcore configure -e "{tarball_str}" --name {agent_name}'
    if execution_role_arn:
        cmd += f' --execution-role {execution_role_arn}'
    print("Running:", cmd)
    subprocess.check_call(cmd, shell=True)  # shell=True avoids shlex path issues on Windows
    print("✅ Configure succeeded")

def agentcore_launch(local=False):
    cmd = "agentcore launch"
    if local:
        cmd += " --local"
    print("Running:", cmd)
    subprocess.check_call(cmd, shell=True)
    print("✅ Launch succeeded")

def deploy_from_tarball(tarball_path: str, execution_role_arn=None, local=False):
    tarball = Path(tarball_path)
    if not tarball.exists():
        raise FileNotFoundError(f"{tarball} not found")

    # Infer project name and version
    m = re.match(r"(.+)_v(\d+)\.tar\.gz", tarball.name)
    if not m:
        raise ValueError(f"Invalid tarball name format: {tarball.name}")
    project_name, version = m.groups()
    version = int(version)

    # Generate valid AgentCore name (letters/numbers/underscores, max 48 chars)
    agent_name = project_name.replace("-", "_")
    if not agent_name[0].isalpha():
        agent_name = "a" + agent_name
    agent_name = f"{agent_name}_v{version}"[:48]

    print(f"Deploying {project_name} v{version} via AgentCore as '{agent_name}'...")
    
    agentcore_configure(tarball, agent_name, execution_role_arn)
    agentcore_launch(local=local)

    deployment_info = {
        "project": project_name,
        "version": version,
        "agentcore_name": agent_name,
        "endpoint": f"agentcore://{agent_name}",
        "status": "deployed",
        "tarball_path": str(tarball.resolve())
    }
    print("✅ Deployment complete:", deployment_info)
    return deployment_info

if __name__ == "__main__":
    # pick the tarball from deployable folder
    deploy_from_tarball("langgraph_example_v1757963502.tar.gz")
