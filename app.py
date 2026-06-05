import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json
import re

# --- CONFIGURATION & UI SETUP ---
st.set_page_config(page_title="AI Prompt Optimizer", page_icon="🪄", layout="wide")

st.title("🪄 AI Prompt Optimizer & Coach")
st.caption("Transform weak prompts into highly optimized, frameworks-driven instructions locally.")

# Sidebar Settings
st.sidebar.header("Model Settings")
model_name = st.sidebar.selectbox("Select Ollama Model", ["qwen2.5vl"], index=0)
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.3, 0.1)

# Initialize the Local LLM
@st.cache_resource
def get_llm(model, temp):
    return ChatOllama(model=model, temperature=temp)

llm = get_llm(model_name, temperature)

# --- SYSTEM PROMPT DEFINITIONS ---
# This meta-prompt instructs the LLM to act as an expert prompt engineer and output JSON.
OPTIMIZER_SYSTEM_PROMPT = """
You are an expert Prompt Engineer. Your task is to analyze the user's raw, weak input prompt and rewrite it into exactly 5 different high-quality, engineered variations following these strict frameworks:

1. Role-Based (Assigns a highly specific persona and context)
2. Chain-of-Thought (Forces step-by-step reasoning before answering)
3. Few-Shot (Provides mock examples of preferred input/output mapping)
4. Strict Constraints (Defines clear boundaries, negative constraints, and output formats)
5. Creative/Exploratory (Encourages open-ended, multi-perspective brainstorming)

For EACH variation, you must also provide a brief, 1-sentence "Coach's Note" explaining WHY this variation works and what prompt engineering technique it teaches.

You MUST respond ONLY with a valid JSON object matching this exact structure, with no markdown formatting, no code blocks, and no text before or after the JSON:
{{
    "variations": [
        {{"type": "Role-Based", "prompt": "rewritten prompt here", "note": "coach note here"}},
        {{"type": "Chain-of-Thought", "prompt": "rewritten prompt here", "note": "coach note here"}},
        {{"type": "Few-Shot", "prompt": "rewritten prompt here", "note": "coach note here"}},
        {{"type": "Strict Constraints", "prompt": "rewritten prompt here", "note": "coach note here"}},
        {{"type": "Creative/Exploratory", "prompt": "rewritten prompt here", "note": "coach note here"}}
    ]
}}
"""

# --- HELPER FUNCTIONS ---
def clean_json_string(text):
    """Cleans potential LLM formatting artifacts (like markdown code blocks)."""
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    return text.strip()

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Input Your Raw Prompt")
    raw_prompt = st.text_area(
        "What do you want to ask the AI?",
        placeholder="e.g., Write a marketing email for shoes.",
        height=150
    )
    
    test_context = st.text_input(
        "Optional: Add sample variables / testing context", 
        placeholder="e.g., The shoes are eco-friendly running sneakers priced at $99."
    )
    
    optimize_btn = st.button("🪄 Optimize & Generate Variations", use_container_width=True, type="primary")

with col2:
    st.subheader("🧠 Interactive Prompt Coach")
    
    if optimize_btn and raw_prompt:
        with st.spinner("Engineering prompt variations..."):
            try:
                # Orchestrate Meta-Prompting via LangChain
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", OPTIMIZER_SYSTEM_PROMPT),
                    ("human", "Optimize this raw prompt: '{input_prompt}'")
                ])
                
                chain = prompt_template | llm
                response = chain.invoke({"input_prompt": raw_prompt})
                
                # Parse JSON responses safely
                cleaned_content = clean_json_string(response.content)
                data = json.loads(cleaned_content)
                
                st.session_state["prompt_variations"] = data.get("variations", [])
                st.success("Generated 5 optimized variations successfully!")
                
            except Exception as e:
                st.error("Failed to parse the model's output as JSON. Please try again.")
                st.code(response.content if 'response' in locals() else str(e))

    # If variations exist in state, display them interactively
    if "prompt_variations" in st.session_state:
        for idx, var in enumerate(st.session_state["prompt_variations"]):
            with st.expander(f"✨ Option {idx+1}: {var['type']}"):
                
                # Show the engineered prompt
                st.markdown("**Engineered Prompt:**")
                st.info(var["prompt"])
                
                # Show the educational coaching note
                st.markdown("💡 **Coach's Takeaway:**")
                st.caption(var["note"])
                
                # Test execution framework
                if st.button(r"▶️ Run This Version", key=f"run_{idx}"):
                    full_execution_input = var["prompt"]
                    if test_context:
                        full_execution_input += f"\n\nContext/Data to apply this to:\n{test_context}"
                    
                    st.markdown("---")
                    st.markdown("**🏃‍♂️ Live Output Generation:**")
                    
                    with st.spinner("Generating output from this variation..."):
                        # Directly invoke the LLM with the newly engineered prompt template
                        output_response = llm.invoke(full_execution_input)
                        st.write(output_response.content)
    else:
        st.info("Paste a weak prompt on the left to see prompt engineering frameworks in action.")