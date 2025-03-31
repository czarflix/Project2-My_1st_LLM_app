import streamlit as st  # For building the web User Interface (UI)
import os  # To access environment variables (like API keys)
from dotenv import load_dotenv  # To load variables from our secure .env file

# Langchain Core Components
from langchain_core.prompts import ChatPromptTemplate  # To structure our prompts
from langchain_core.output_parsers import StrOutputParser  # To get plain text output from LLMs

# Langchain Integrations (Connecting to specific LLMs)
from langchain_openai import ChatOpenAI  # To talk to OpenAI's API
from langchain_groq import ChatGroq  # To talk to Groq's API
from langchain_ollama import ChatOllama

# Load environment variables FIRST
load_dotenv()

# Loading environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
os.getenv("LANGCHAIN_TRACING_V2")
os.getenv("LANGCHAIN_ENDPOINT")
os.getenv("LANGCHAIN_API_KEY")
os.getenv("LANGCHAIN_PROJECT")

# Setting the default Ollama model (for easy use later on)
DEFAULT_OLLAMA_MODEL = 'llama3.2'

# Setting up the Langchain
prompt_template_str = """
Human: You are a helpful AI assistant. Respond concisely to the following user query:
{user_prompt}

A:
"""
prompt_template = ChatPromptTemplate.from_template(prompt_template_str)

# Setting up the output parser to convert output into text
output_parser = StrOutputParser()

# Initialzing the LLM
llm_openai = None  # Starting my assuming the open ai llm isn't available
llm_groq = None  # Starting my assuming groq llm isn't available
llm_ollama = None  # Starting by assuming ollama llm isnt available
ollama_available = False  # Flag to track if Ollama is truly ready

# Connecting to LLMs

# Connecting to Open AI
if openai_api_key:
    try:
        llm_openai = ChatOpenAI(model="gpt-4o-mini")
    except Exception as e:
        st.error(f"Error connecting to OpenAI: {e}")
else:
    st.warning("OpenAI API key not found. OpenAI will not be available.")

# Connecting to Groq
if groq_api_key:
    try:
        llm_groq = ChatGroq(model="llama3-8b-8192", temperature=0.7)
    except Exception as e:
        st.error(f"Error connecting to Groq: {e}")
else:
    st.warning("Groq API key not found. Groq will not be available.")

# Initializing Ollama and performing a readiness check
ollama_available = False
try:
    llm_ollama_instance = ChatOllama(model=DEFAULT_OLLAMA_MODEL)

    try:
        llm_ollama_instance.invoke("Reply with just OK")
        llm_ollama = llm_ollama_instance
        ollama_available = True
    except Exception as e:
        st.error(f"Error connecting to Ollama: {e}")
except Exception as e:
    st.error(f"Error initializing Ollama: {e}")

# Building LCEL chains
# Only create chains for LLMs that were successfully initialized

chain_openai = None  # Start as None
if llm_openai:
    chain_openai = prompt_template | llm_openai | output_parser

chain_groq = None  # Start as None
if llm_groq:
    chain_groq = prompt_template | llm_groq | output_parser

chain_ollama = None  # Start as None
if llm_ollama and ollama_available:
    chain_ollama = prompt_template | llm_ollama | output_parser

# Streamlit UI
st.set_page_config(page_title="My first LLM app", layout="wide")
st.title("My first LLM app")
st.markdown("Comparing Responses from OpenAI, Groq, and Local Ollama")

# Sidebar for Configuration status
st.sidebar.markdown(f"""
- OpenAI (GPT-4o mini): {'✅ Ready' if llm_openai else '❌ Not Available (Check API Key)'}
- Groq (Llama3 8B): {'✅ Ready' if llm_groq else '❌ Not Available (Check API Key)'}
- Ollama ({DEFAULT_OLLAMA_MODEL} Local): {'✅ Ready' if ollama_available else '❌ Not Available (Check Ollama Status/Model)'}
""")
st.sidebar.markdown("---")
user_prompt = st.sidebar.text_input("Enter your prompt here:",
                                    placeholder="e.g., Explain the concept of Langchain in simple terms.")

# Button to trigger generation, disabled if no prompt is available
if st.button("Generate Responses", disabled=not user_prompt):
    st.markdown("---")
    st.subheader("LLM Responses")

    # Create columns for side-by-side display
    col1, col2, col3 = st.columns(3)

    # --- OpenAI column ---
    with col1:
        st.markdown("#### OpenAI (GPT-4o mini)")
        if chain_openai:  # Checking if open ai chain exists
            try:
                # Showing spinner while waiting for response
                with st.spinner("Querying OpenAI..."):
                    response_openai = chain_openai.invoke({"user_prompt": user_prompt})

                st.success("Response received!")
                st.markdown(response_openai)  # Fixed formatting
            except Exception as e:
                # If an API error occurrs
                st.error(f"OpenAI Error during generation: {e}")

        else:
            # Message if OpenAI was not initialized correctly
            st.warning("OpenAI chain is not available.")

    # --- Groq Column ---
    with col2:
        st.markdown("#### Groq (Llama3 8B)")
        if chain_groq:  # Check if the Groq chain is ready
            try:
                with st.spinner("Querying Groq... (Usually Fast!)"):
                    response_groq = chain_groq.invoke({"user_prompt": user_prompt})  # Fixed variable name
                st.success("Response received!")  # Consistent messaging
                st.markdown(response_groq)  # Fixed variable name
            except Exception as e:
                st.error(f"Groq Error during generation: {e}")
        else:
            st.warning("Groq chain is not available.")

    # --- Ollama Column ---
    with col3:
        st.markdown(f"#### Ollama ({DEFAULT_OLLAMA_MODEL} - Local)")
        if chain_ollama:  # Check if the Ollama chain is ready
            try:
                with st.spinner(f"Querying local {DEFAULT_OLLAMA_MODEL}..."):
                    response_ollama = chain_ollama.invoke({"user_prompt": user_prompt})  # Fixed variable name
                st.success("Response received!")  # Consistent messaging
                st.markdown(response_ollama)  # Fixed variable name
            except Exception as e:
                st.error(f"Ollama Error during generation: {e}")
        else:
            st.warning("Ollama chain is not available.")

# Add instructions on how to run at the bottom
st.markdown("---")
st.markdown("""
## How to run this app:
1. Make sure you have set up environment variables in a `.env` file:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `GROQ_API_KEY` - Your Groq API key
   - `LANGCHAIN_TRACING_V2`, `LANGCHAIN_ENDPOINT`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT` - Optional for LangSmith tracing
2. Install Ollama locally if you want to use local models
3. Run the app with `streamlit run app.py`
""")
