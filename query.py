from abc import ABC, abstractmethod
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

class QueryService(ABC):
    @abstractmethod
    def ask(self, system_prompt: str, prompt: str) -> str:
        pass

class GeminiService(QueryService):
    def ask(self, system_prompt: str, prompt: str) -> str:
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

            response = client.models.generate_content(
                model='gemini-2.5-pro-exp-03-25',
                contents=types.Part.from_text(text=f'{prompt}'),
                config=types.GenerateContentConfig(
                    system_instruction=f"{system_prompt}",
                    temperature=0,
                    top_p=0.95,
                    top_k=20,
                    candidate_count=1,
                    seed=5,
                    #max_output_tokens=100,
                    stop_sequences=['STOP!'],
                    presence_penalty=0.0,
                    frequency_penalty=0.0,
                    #response_mime_type="application/json",
                ),
            )

            return response.text

        except Exception as e:
            return f"Error: {str(e)}"
