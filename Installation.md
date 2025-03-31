
---

# **Project 2: Installation and Setup**  

Follow these steps to set up the environment for **Project 2**. This guide assumes you have completed **Project 0** and have a working Python environment (**Conda** or **venv**) with `pip` available.  

---

## **1. Activate Your Virtual Environment**  

Ensure the virtual environment you created in **Project 0** is activated.  

### **Using Conda:**  
```bash
conda activate your_env_name
```
### **Using venv:**  
#### **Linux/macOS:**  
```bash
source your_env_name/bin/activate
```
#### **Windows:**  
```bash
.\your_env_name\Scripts\activate
```

---

## **2. Install Required Python Libraries**  

Install **Langchain** and the required integrations for **OpenAI, Groq, Ollama, and Streamlit**, along with `python-dotenv` for managing API keys.  

```bash
pip install langchain langchain-openai langchain-groq langchain-ollama streamlit python-dotenv
```
```bash
pip install urllib3==1.26.16 # Some deprecation issues so we need to install urllib
```
### **Library Overview:**  
- **`langchain`** – The core Langchain library.  
- **`langchain-openai`** – Integration for OpenAI models.  
- **`langchain-groq`** – Integration for Groq models.  
- **`langchain-community`** – Contains integrations for community-supported tools like Ollama.  
- **`streamlit`** – To build the web application interface (as used in previous projects).  
- **`python-dotenv`** – Loads API keys securely from a `.env` file.  

---

## **3. Set Up API Keys**  

You will need API keys for **OpenAI** and **Groq**.  

### **OpenAI:**  
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys).  
2. Sign up or log in.  
3. Create a **new secret key**. **Copy it immediately** as it won’t be visible again.  

### **Groq:**  
1. Go to [Groq API Keys](https://console.groq.com/keys).  
2. Sign up or log in.  
3. Create a **new API key** and **copy it immediately**.  

### **Store Your API Keys Securely:**  

Create a `.env` file in the **root directory** of your project and add the following:  

```ini
# .env file
OPENAI_API_KEY="your_openai_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
```

💡 **Important:** If using Git, **add `.env` to `.gitignore`** to prevent accidental leaks.  

---

## **4. Install and Set Up Ollama (for Local LLM)**  

### **Install Ollama:**  
1. Visit [Ollama](https://ollama.com/).  
2. Download and install **the appropriate version** for your OS (**macOS, Linux, Windows**).  
3. The installer **automatically sets up** Ollama as a background service.  

### **Pull a Local Model:**  

Once Ollama is installed, open a terminal and **download a model** (e.g., **llama3**, ~4.7GB).  

```bash
ollama pull llama3
```

Wait for the **download to complete**.  

### **Verify Ollama is Running:**  

Run the following command to test if **Ollama** is active:  

```bash
ollama run llama3 "Why is the sky blue?"
```

If you receive a response, **Ollama is set up correctly**.  

---

## **5. (Optional) Set Up Langsmith**  

If you want to trace Langchain calls for debugging:  

1. Visit [Langsmith](https://smith.langchain.com/) and sign up.  
2. Create an **API key**.  
3. Add the following to your `.env` file:  

```ini
# .env file (if using Langsmith)
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
LANGCHAIN_PROJECT="My First LLM App"  # Change as needed
```

---

✅ **You are now ready to proceed with Project 2!** 🚀