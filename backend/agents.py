import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from backend.prompt import system_prompt
from backend.tools import get_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# llama-3.1-8b-instant
# llama-3.3-70b-versatile
# meta-llama/llama-guard-4-12b
# openai/gpt-oss-120b


model = ChatGroq(model="qwen/qwen3-32b")

# model =ChatGoogleGenerativeAI(model = "gemini-2.5-flash",
#  api_key=os.getenv("GEMINI_API_KEY"))

def get_chat_agent():
   
    tools = get_tools(model)
    graph = create_react_agent(model, tools, prompt=system_prompt)    
    return graph
