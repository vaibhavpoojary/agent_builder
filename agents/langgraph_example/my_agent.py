# agents/langgraph_example/my_agent.py
from bedrock_agentcore import BedrockAgentCoreApp
# Import your LangGraph code (this file should expose `run_agent(prompt)`)
# Replace with your real langgraph imports
from my_agent import run_agent  

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload: dict):
    """
    AgentCore will call this. Payload expected to contain 'prompt'.
    Keep this simple: parse, call agent logic and return JSON-able dict.
    """
    prompt = payload.get("prompt") or payload.get("input") or "Hello"
    response = run_agent(prompt)        # your LangGraph call
    # Ensure return types are serializable
    return {"result": str(response)}

if __name__ == "__main__":
    # For local dev loop
    app.run()
