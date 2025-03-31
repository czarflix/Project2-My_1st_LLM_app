

# Streamlit LLM Comparison App - Code Explanation

## Section 1: Imports
```python
import streamlit as st
import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
```
This section imports all required libraries:
- `streamlit`: Creates the web interface elements
- `os`: Provides access to environment variables
- `load_dotenv`: Loads environment variables from a .env file
- `ChatPromptTemplate`: Creates formatted prompt templates for LLMs
- `StrOutputParser`: Converts LLM outputs to plain strings
- LangChain integrations for OpenAI, Groq, and Ollama to interact with these specific LLM providers

## Section 2: Environment Setup
```python
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
os.getenv("LANGCHAIN_TRACING_V2")
os.getenv("LANGCHAIN_ENDPOINT")
os.getenv("LANGCHAIN_API_KEY")
os.getenv("LANGCHAIN_PROJECT")

DEFAULT_OLLAMA_MODEL = 'llama3.2'
```
Here the code:
- Loads all variables from the .env file using `load_dotenv()`
- Extracts API keys for OpenAI and Groq into variables for later use
- Loads LangChain tracing configuration variables (though they're not assigned to variables)
- Defines a constant `DEFAULT_OLLAMA_MODEL` set to 'llama3.2' for use with the local Ollama instance

## Section 3: Prompt Template Setup
```python
prompt_template_str = """
Human: You are a helpful AI assistant. Respond concisely to the following user query:
{user_prompt}

A:
"""
prompt_template = ChatPromptTemplate.from_template(prompt_template_str)

output_parser = StrOutputParser()
```
This section:
- Creates a multi-line string template for prompts that:
  - Includes a role prefix ("Human:")
  - Provides brief instructions to the AI
  - Contains a placeholder `{user_prompt}` that will be replaced with actual user input
  - Includes a response prefix ("A:")
- Converts this string into a `ChatPromptTemplate` object for LangChain
- Initializes a `StrOutputParser` to convert structured LLM responses into plain text

## Section 4: LLM Initialization
```python
llm_openai = None
llm_groq = None
llm_ollama = None
ollama_available = False

if openai_api_key:
    try:
        llm_openai = ChatOpenAI(model="gpt-4o-mini")
    except Exception as e:
        st.error(f"Error connecting to OpenAI: {e}")
else:
    st.warning("OpenAI API key not found. OpenAI will not be available.")

if groq_api_key:
    try:
        llm_groq = ChatGroq(model="llama3-8b-8192", temperature=0.7)
    except Exception as e:
        st.error(f"Error connecting to Groq: {e}")
else:
    st.warning("Groq API key not found. Groq will not be available.")

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
```
This code initializes connections to three different LLM providers with error handling:

1. **OpenAI Initialization**:
   - Sets `llm_openai` to `None` initially
   - Checks if `openai_api_key` exists
   - If key exists, attempts to create a `ChatOpenAI` instance with "gpt-4o-mini" model
   - Catches and displays any initialization errors
   - Shows warning if API key is missing

2. **Groq Initialization**:
   - Sets `llm_groq` to `None` initially
   - Checks if `groq_api_key` exists
   - If key exists, creates a `ChatGroq` instance with "llama3-8b-8192" model and temperature 0.7
   - Catches and displays any initialization errors
   - Shows warning if API key is missing

3. **Ollama Initialization**:
   - Sets `llm_ollama` to `None` and `ollama_available` to `False` initially
   - Uses a two-level try-except pattern:
     - Outer try: Creates the `ChatOllama` instance
     - Inner try: Tests connection by sending a simple test prompt
     - If test succeeds, assigns instance to `llm_ollama` and sets `ollama_available` to `True`
     - Catches and displays connection vs. initialization errors separately

## Section 5: LangChain Expression Language (LCEL) Chain Setup
```python
chain_openai = None
if llm_openai:
    chain_openai = prompt_template | llm_openai | output_parser

chain_groq = None
if llm_groq:
    chain_groq = prompt_template | llm_groq | output_parser

chain_ollama = None
if llm_ollama and ollama_available:
    chain_ollama = prompt_template | llm_ollama | output_parser
```
This section creates processing chains using LangChain's pipe operator syntax:

- Initializes all chains to `None`
- For each LLM, checks if it was successfully initialized
- If available, creates a chain using the pipe operator (`|`):
  - `prompt_template`: Formats the user input using the template defined earlier
  - `llm_*`: Sends the formatted prompt to the respective LLM
  - `output_parser`: Converts the LLM response to a plain string
- For Ollama, adds an additional check on the `ollama_available` flag

## Section 6: Streamlit UI Setup
```python
st.set_page_config(page_title="My first LLM app", layout="wide")
st.title("My first LLM app")
st.markdown("Comparing Responses from OpenAI, Groq, and Local Ollama")

st.sidebar.markdown(f"""
- OpenAI (GPT-4o mini): {'✅ Ready' if llm_openai else '❌ Not Available (Check API Key)'}
- Groq (Llama3 8B): {'✅ Ready' if llm_groq else '❌ Not Available (Check API Key)'}
- Ollama ({DEFAULT_OLLAMA_MODEL} Local): {'✅ Ready' if ollama_available else '❌ Not Available (Check Ollama Status/Model)'}
""")
st.sidebar.markdown("---")
user_prompt = st.sidebar.text_input("Enter your prompt here:",
                                    height=150,
                                    placeholder="e.g., Explain the concept of Langchain in simple terms.")
```
This code configures the Streamlit user interface:

- `st.set_page_config()`: Sets the page title and uses a wide layout
- `st.title()` and `st.markdown()`: Adds the app title and description

In the sidebar:
- Uses f-string with conditional expressions to show each LLM's status:
  - `{'✅ Ready' if llm_openai else '❌ Not Available (Check API Key)'}`
- Adds a separator line
- Creates a text input box with:
  - 150 pixel height
  - A placeholder example prompt
  - Stores user input in the `user_prompt` variable

## Section 7: Response Generation Logic
```python
if st.button("Generate Responses", disabled=not user_prompt):
    st.markdown("---")
    st.subheader("LLM Responses")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### OpenAI (GPT-4o mini)")
        if chain_openai:
            try:
                with st.spinner("Querying OpenAI..."):
                    response_openai = chain_openai.invoke({"user_prompt": user_prompt})

                st.success("Response received!")
                st.markdown(response_openai)
            except Exception as e:
                st.error(f"OpenAI Error during generation: {e}")
        else:
            st.warning("OpenAI chain is not available.")

    with col2:
        st.markdown("#### Groq (Llama3 8B)")
        if chain_groq:
            try:
                with st.spinner("Querying Groq... (Usually Fast!)"):
                    response_groq = chain_groq.invoke({"user_prompt": user_prompt})
                st.success("Response received!")
                st.markdown(response_groq)
            except Exception as e:
                st.error(f"Groq Error during generation: {e}")
        else:
            st.warning("Groq chain is not available.")

    with col3:
        st.markdown(f"#### Ollama ({DEFAULT_OLLAMA_MODEL} - Local)")
        if chain_ollama:
            try:
                with st.spinner(f"Querying local {DEFAULT_OLLAMA_MODEL}..."):
                    response_ollama = chain_ollama.invoke({"user_prompt": user_prompt})
                st.success("Response received!")
                st.markdown(response_ollama)
            except Exception as e:
                st.error(f"Ollama Error during generation: {e}")
        else:
            st.warning("Ollama chain is not available.")
```
This section manages the response generation process:

- `st.button()`: Creates a "Generate Responses" button that's disabled when no prompt is entered
- When clicked, the code:
  - Adds a separator and subheader
  - Creates three equal columns with `st.columns(3)`
  
For each LLM (OpenAI, Groq, Ollama) in its respective column:
1. Displays a header with the model name
2. Checks if the corresponding chain exists
3. If available:
   - Wraps the API call in a try-except block to catch errors
   - Shows a spinner during processing with `st.spinner()`
   - Invokes the chain with the user prompt in a dictionary: `{"user_prompt": user_prompt}`
   - Shows success message and displays the response with `st.markdown()`
   - Catches and displays any errors that occur during generation
4. If not available, shows a warning message

## Section 8: Footer
```python
st.markdown("---")
st.markdown("""
""")
```
This final section:
- Adds a horizontal separator with `st.markdown("---")`
- Includes an empty markdown container that could be used for additional information in the future (currently empty)

