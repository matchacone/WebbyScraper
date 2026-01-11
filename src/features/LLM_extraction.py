import os
import sys

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import LLMConfig

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_api_key():
    """Get API key from env or ask user."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        # If running as an app, we might need a popup, but for now use CLI
        print("\n[!] Gemini API Key not found.")
        key = input("Please paste your Google Gemini API Key: ").strip()
        # Set it for this session so other parts of the app can find it
        os.environ["GEMINI_API_KEY"] = key
    return key

class Contacts(BaseModel):
    URL: str = Field(..., description="URL of the page")
    name: str = Field(..., description="Full name of the person (e.g., 'Shane Thurkle').")
    address: str = Field(..., description="Address of the person.")
    title: str = Field(..., description="Job Title. MAX 5 words. Return 'N/A' if the text looks like a message or sentence.")
    first_name: str = Field(..., description="First name inferred from 'name'.")
    last_name: str = Field(..., description="Last name inferred from 'name'.")
    email: str = Field(..., description="Personal email of the contact")
    phone: str = Field(..., description="Mobile/Cell number preferred. Format: +63... or 09...")

llm_cfg = LLMConfig(
    provider='gemini/gemini-2.5-flash',
    #provider='ollama/llama3.1'
    api_token=get_api_key()
)

llm_strategy = LLMExtractionStrategy(
    llm_config=llm_cfg,
    schema=Contacts.model_json_schema(),
    extraction_type="schema",
    
    chunk_token_threshold=30000,
    overlap_rate=0.15,
    apply_chunking=False,
    
    input_format="markdown",
    instruction = """
    Extract the specific data fields requested by the user from the webpage content.
        - If a field is missing, return "N/A".
        - Be precise and concise.
        - Do not hallucinate data not present on the page.
    """
)