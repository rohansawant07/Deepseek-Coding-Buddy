import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Custom CSS styling with purple accent
st.markdown("""
<style>
    /* Base styles */
    html, body, [class*="css"]  {
        color: #E0E0E0;
        background-color: #121212;
    }

    /* Main container */
    .main {
        background-color: #121212;
        padding: 2rem;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #1E1E1E;
        border-right: 1px solid #333333;
    }

    /* Input fields */
    .stTextInput textarea {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }

    /* Select box */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #2D2D2D !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
    }

    /* Dropdown menu */
    div[role="listbox"] div {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
    }

    /* Chat messages */
    .stChatMessage {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* User messages */
    div[data-testid="stChatMessageUser"] {
        background-color: #2D2D2D;
        border: 1px solid #404040;
    }

    /* AI messages */
    div[data-testid="stChatMessageAssistant"] {
        background-color: #1E1E1E;
        border: 1px solid #333333;
    }

    /* Code blocks */
    code {
        color: #78C9FF !important;
        background-color: #2D2D2D !important;
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid #404040;
        font-family: 'Fira Code', monospace;
    }

    pre code {
        display: block;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        border-radius: 8px !important;
    }

    /* Buttons and hover states */
    .stButton button {
        background-color: #2D2D2D !important;
        color: #78C9FF !important;
        border: 1px solid #404040 !important;
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        background-color: #78C9FF !important;
        color: #121212 !important;
        border-color: #78C9FF !important;
    }

    /* Divider styling */
    hr {
        border-color: #404040 !important;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 CodeGenius Pro")
st.caption("✨ AI-Powered Coding Wizard with Multi-Model Intelligence")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Engine Settings")
    selected_model = st.selectbox(
        "Model Version",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],
        index=0,
        help="Choose model size based on complexity needs"
    )
    
    st.divider()
    st.markdown("### Core Capabilities")
    st.markdown("""
    - 🧩 Advanced Code Synthesis
    - 🔍 Context-Aware Debugging
    - 📚 Smart Documentation
    - ⚡ Performance Optimization
    - 🛠️ Code Refactoring
    """)
    st.divider()
    st.markdown("**Powered by**  \n"
                "[Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")
    st.markdown("*v1.2.0 | CodeGenius Pro*")

# Initiate the chat engine
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.35,
    top_p=0.9,
    num_ctx=4096
)

# Enhanced system prompt
system_prompt = SystemMessagePromptTemplate.from_template(
    """You are CodeGenius Pro - an elite AI coding assistant. Provide:
1. Optimal solutions with strategic debugging hooks
2. Clean, production-ready code
3. Performance considerations
4. Alternative approaches when applicable
Always prioritize security and best practices. Use markdown for code formatting."""
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{
        "role": "ai", 
        "content": "Hello! I'm CodeGenius Pro 🚀\n\nHow can I assist with your coding challenge today?"
    }]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and processing
user_query = st.chat_input("Describe your coding task or paste error...")

def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    with st.spinner("🔍 Analyzing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    st.rerun()