import os
from dotenv import load_dotenv
from typing import Any, Optional, Literal
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print("Loaded Config")
        self.config = load_config()

    def __getitem__(self, key):
            return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        
        """
        print("LLM Loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config.llm.groq.model_name
            llm = ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI...")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config.llm.openai.model_name
            llm = ChatOpenAI(model=model_name, openai_api_key=openai_api_key)

        return llm