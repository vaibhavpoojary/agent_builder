# agent_builder
agent_builder_for_aws_native_cloud under development
<img width="2230" height="841" alt="image" src="https://github.com/user-attachments/assets/6da61250-b4ae-498d-9d94-6c551dd550b8" />
# 📖 Simple Chatbot — AgentCore + Anthropic Claude 3.5

A minimal chatbot agent that uses **Amazon Bedrock AgentCore Runtime** with **Anthropic Claude 3.5 Sonnet** as the model backend.  

This project is designed to run on **Windows x64 without Docker Desktop** — all container builds happen in the cloud via the `agentcore` CLI.

---

## 🚀 Features
- Chatbot powered by **Anthropic Claude 3.5 Sonnet**  
- Deployable to **Bedrock AgentCore Runtime**  
- No Docker Desktop required (uses cloud builds)  
- Works from **Windows x64** with AWS CLI + AgentCore CLI  

---

## 📂 Project Structure

```
simple-chatbot/
├── my_agent.py               # Main agent code
├── requirements.txt          # Python dependencies
├── .bedrock_agentcore.yaml   # AgentCore config (auto-generated)
└── README.md                 # Project documentation
```

---

## ⚙️ Prerequisites

1. **AWS Account** with:
   - Amazon Bedrock enabled  
   - Access to **Anthropic Claude 3.5 Sonnet** (request in Bedrock console → Model access)  
   - IAM execution role with permissions:
     - `AmazonBedrockFullAccess`
     - `BedrockAgentCoreFullAccess`

2. **Local tools** on Windows:
   - Python 3.10+  
   - pip  
   - AWS CLI (`aws configure`)  
   - AgentCore Starter Toolkit:  
     ```powershell
     pip install --upgrade pip
     pip install bedrock-agentcore-starter-toolkit
     ```

---

## 📝 Configuration

Update `.bedrock_agentcore.yaml` with your **AWS Account ID** and **Execution Role ARN**:

```yaml
executionRole: arn:aws:iam::<ACCOUNT_ID>:role/YourAgentExecutionRole
region: us-east-1
```

---

## ▶️ Local Test (Python only)

1. Run the agent locally:
   ```powershell
   set BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
   set AWS_REGION=us-east-1
   python my_agent.py
   ```

2. In another terminal, test with curl:
   ```powershell
   curl -X POST http://localhost:8080/invocations `
        -H "Content-Type: application/json" `
        -d "{\"prompt\":\"Tell me a joke.\"}"
   ```

---

## 🚢 Deploy to AgentCore Runtime

1. **Configure project** (generates Dockerfile + config):
   ```powershell
   agentcore configure `
     --entrypoint my_agent.py `
     --name simple-chatbot `
     --requirements-file requirements.txt `
     --execution-role arn:aws:iam::<ACCOUNT_ID>:role/YourAgentExecutionRole `
     --region us-east-1
   ```

2. **Deploy to AgentCore Runtime**:
   ```powershell
   agentcore launch
   ```

   - Code + dependencies are packaged  
   - AWS builds the container (Linux ARM64)  
   - Image is pushed to **ECR**  
   - Runtime is created in **Bedrock AgentCore**  

3. CLI will output the **runtime ARN** and **endpoint**.

---

## 💬 Invoke the Deployed Chatbot

1. Using the CLI:
   ```powershell
   agentcore invoke "{"prompt":"Hello Claude!"}"
   ```

2. From the AWS Console:
   - Go to **Amazon Bedrock → Agent Runtimes**  
   - Select **simple-chatbot** runtime  
   - Click **Invoke runtime**  
   - Enter payload:  
     ```json
     {
       "prompt": "Tell me about AgentCore."
     }
     ```
   - See model response in JSON output

---

## 🛠 How It Works (Option 1)

- You run **Python code locally** (x64, no Docker needed)  
- `agentcore configure` → generates config files  
- `agentcore launch` → uploads project to AWS  
- AWS builds container as **Linux ARM64** in the cloud  
- AWS deploys the runtime to **Bedrock AgentCore**  
- You test via CLI or AWS Console  

✅ No Docker Desktop or ARM64 machine required.

---

## 🔐 IAM Execution Role Policy Example

Attach this policy to your `YourAgentExecutionRole`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:CreateAgent",
        "bedrock:CreateAgentVersion",
        "bedrock:DeleteAgent",
        "bedrock:GetAgent",
        "bedrock:ListAgents",
        "bedrock:InvokeAgent"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:*",
        "iam:PassRole",
        "logs:*",
        "s3:*"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## ⚠️ Notes & Tips
- Ensure you have **Claude 3.5 Sonnet access** in Bedrock console  
- Use correct **region** where model is available (default: `us-east-1`)  
- Set `BEDROCK_MODEL_ID` via env var if model ID changes in future  
- Costs: You are billed for **Bedrock model usage (tokens)** and **ECR storage**  

---

## ✅ Next Steps
- Add conversation memory  
- Connect to API Gateway / Lambda for web apps  
- Use Guardrails in Bedrock for safe responses  
 
