from dotenv import load_dotenv
# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import erp_core.config as cfg
import os


load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# llm = ChatAnthropic(model=cfg.anthropic_model_name, temperature=1)
llm = ChatOpenAI(model=cfg.model_name, temperature=0)
