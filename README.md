🪄 AI Prompt Optimizer & Coach
An interactive, local, and privacy-focused Streamlit application that transforms weak, low-effort prompts into highly optimized instructions using structured prompt engineering frameworks.

Powered by a remote GPU server running Ollama (qwen2.5vl or llama3), LangChain v0.3, and ChromaDB, this tool provides 5 distinct engineered variations of any prompt and dynamically runs them to show how semantic architecture alters LLM behavior.

🚀 Features
5-Framework Optimization Engine: Rewrites prompts instantly using specialized paradigms:

Role-Based: Establishes target context and professional personas.

Chain-of-Thought (CoT): Enforces step-by-step logical reasoning loops.

Few-Shot: Implements target structural example blocks.

Strict Constraints: Defines execution boundaries and negative constraints.

Creative/Exploratory: Broadens multi-perspective ideation.

Interactive Prompt Coach: Explains why changes were made via specialized educational takeaways ("Coach's Takeaways").

Live Sandbox Testing: Hit Run This Version to directly execute any engineered variation against your remote GPU and inspect outputs side-by-side.

Bulletproof JSON Parser: Uses advanced regex bracket extraction and native backend formatting to ensure local models always return parseable data structures.

📐 Architecture Flow
Plaintext
  ┌────────────────────────┐         HTTP (JSON format)         ┌─────────────────────────┐
  │      Streamlit UI      │ ─────────────────────────────────> │    Remote GPU Server    │
  │   (Local Workspace)    │ <───────────────────────────────── │    (Ollama Backend)     │
  └────────────────────────┘        Structured Outputs          └─────────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ LangChain Pipeline   │ ──> (Regex Cleaning & State Triage)
   └──────────────────────┘
🛠️ Installation & Setup
1. Prerequisites
Ensure you have Python 3.10+ installed and access to a remote GPU instance running an accessible Ollama endpoint.

2. Remote Server Configuration
Your remote Ollama instance must be configured to bind to external connections. By default, it blocks public access.

On your remote Linux GPU machine:

Bash
# Edit the Ollama systemd service configuration
sudo systemctl edit ollama.service
Add the following block to explicitly instruct Ollama to bind to all available network interfaces:

Plaintext
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Save the file, reload systemd, and restart the service:

Bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
3. Local Installation & Environment Provisioning
To avoid package dependency conflicts with other OpenAI integrations, it is highly recommended to isolate this tool inside a Python virtual environment.

Bash
# Clone or navigate to your project space
cd prompt_engineering

# Create and activate a isolated virtual environment
python -m venv venv
source venv/bin/activate      # On Windows Use: venv\Scripts\activate

# Install the explicit, cross-compatible ecosystem version set
pip install streamlit
pip install "langchain-core>=0.3.68,<1.0.0"
pip install "langchain-ollama>=0.2.0,<1.0.0"
🏃‍♂️ Running the Application
Open app.py and ensure the REMOTE_URL constant accurately points to your active GPU server environment:

Python
REMOTE_URL = "http://10.22.39.192:11434"
Make sure the specified target model (e.g., qwen2.5vl or llama3) is pulled down onto your remote server repository:

Bash
ollama pull qwen2.5vl
Initialize the application from your terminal workspace:

Bash
streamlit run app.py
📖 How It Works Internally
Meta-Prompting: The application wraps your raw prompt in an underlying master prompt template. This instructs the model to act as a principal prompt engineer.

Deterministic Response Generation: It binds parameters via llm.bind(format="json") forcing the Ollama backend sampler to process strings solely structured as a JSON schema array.

Failsafe Execution UI: The outputs are extracted via regex, cached inside Streamlit's st.session_state to survive refreshing triggers, and structured cleanly into responsive user interaction tabs.

📄 License
This project is proprietary and intended for internal audit compliance, testing, and training review frameworks.
