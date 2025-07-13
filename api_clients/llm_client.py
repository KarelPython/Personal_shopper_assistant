import os
from dotenv import load_dotenv
from utils.logger import logger
from openai import OpenAI

load_dotenv()

class LLMClient:
    def __init__(self, api_key_env_var="OPENAI_API_KEY"):
        self.api_key = os.getenv(api_key_env_var)
        if not self.api_key:
            logger.error(f"API key not found for {api_key_env_var}")
            raise ValueError(f"API key environment variable {api_key_env_var} not set.")
        self.client = OpenAI(api_key=self.api_key)
        

    def get_completion(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        try:
            response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
              
        except Exception as e:
            logger.error(f"Error calling LLM API: {e}")
            return "Omlouváme se, došlo k chybě při zpracování vašeho požadavku."