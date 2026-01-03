import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import LLMConfig

load_dotenv()

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
    api_token=os.getenv("GEMINI_API_KEY")
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