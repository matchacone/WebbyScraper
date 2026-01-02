import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import LLMConfig

load_dotenv()

class Contacts(BaseModel):
    website: str = Field(..., description='Current website URL visited')
    name: str = Field(..., description='Name of the contact')
    title: str = Field(..., description='Title/Job Position of the contact')
    last_name: str = Field(..., description='Last name of the contact')
    first_name: str = Field(..., description='First name of the contact')
    email: str = Field(..., description='Email of the contact')
    phone: str = Field(..., description='Phone/Telephone number')

llm_cfg = LLMConfig(
    provider='ollama/llama3.2',
    api_token="no-token"
)

llm_strategy = LLMExtractionStrategy(
    llm_config=llm_cfg,
    schema=Contacts.model_json_schema(),
    extraction_type="schema",
    extra_args={"temperature": 0},
    instruction="""Extract contact details for the MAIN person/agent on this page.
    - If a field is not explicitly visible, return 'N/A'.
    - DO NOT invent information.
    - DO NOT extract contacts from the footer, 'similar listings', or navigation menu."""
)