import os
import json
import asyncio
from typing import List
from pydantic import create_model, Field
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import LLMConfig

def create_dynamic_schema(field_names: List[str]):
    """
    Dynamically creates a Pydantic model based on a list of field names.
    Example: ['email', 'phone'] -> Class with email and phone fields.
    """
    fields = {}
    for name in field_names:
        clean_name = name.strip().lower().replace(" ", "_")
        if not clean_name: continue
        
        # specific prompt help for common fields, generic for others
        desc = f"Extract the {clean_name}"
        fields[clean_name] = (str, Field(..., description=desc))
    
    # If user provided no valid fields, default to a generic 'summary'
    if not fields:
        fields['summary'] = (str, Field(..., description="Summary of the page content"))

    return create_model('DynamicScrapeModel', **fields)

async def run_scrape(urls: List[str], fields: List[str], model_id: str, api_key: str):
    """
    The main function called by the Flet App.
    """
    print(f"--- Starting Scrape ---")
    print(f"Targeting: {len(urls)} URLs")
    print(f"Extracting: {fields}")

    # 1. Setup API Key for this session
    if not api_key:
        return {"error": "API Key is missing."} 
    
    if "/" in model_id:
        provider_str = model_id
        provider_prefix = model_id.split("/")[0] # e.g., "deepseek" or "anthropic"
    else:
        # Default fallback: assume OpenAI if no slash is present
        provider_str = f"openai/{model_id}"
        provider_prefix = "openai"

    DynamicSchema = create_dynamic_schema(fields)
    
    llm_cfg = LLMConfig(provider=provider_str, api_token=api_key)

    llm_strategy = LLMExtractionStrategy(
        llm_config=llm_cfg,
        schema=DynamicSchema.model_json_schema(),
        extraction_type="schema",
        chunk_token_threshold=100000, 
        apply_chunking=False,
        instruction="Extract the requested fields. Return 'N/A' if not found."
    )

    # 3. Configure "Foolproof" Browser
    browser_conf = BrowserConfig(
        headless=True, 
        verbose=True,
    )

    scroll_script = """
        async function scrollDown() {
            let totalHeight = 0;
            let distance = 300;
            while (totalHeight < document.body.scrollHeight) {
                window.scrollBy(0, distance);
                totalHeight += distance;
                await new Promise(r => setTimeout(r, 100)); 
            }
        }
        await scrollDown();
    """

    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        verbose=True,
        page_timeout=60000,
        wait_until="domcontentloaded",
        delay_before_return_html=3.0,
        remove_overlay_elements=True,
        js_code=scroll_script,
        extraction_strategy=llm_strategy,
        excluded_tags=["style", "noscript", "script", "nav", "footer"],
        exclude_external_links=False,
        magic = True
    )

    # 4. Run Crawler
    results_data = []
    
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        # arun_many handles both single and multiple URLs efficiently
        results = await crawler.arun_many(urls=urls, config=run_conf)

        for res in results:
            if res.success:
                try:
                    # Clean markdown wrappers if present
                    clean_json = res.extracted_content.replace("```json", "").replace("```", "").strip()
                    data = json.loads(clean_json)
                    
                    # Normalize list vs single object
                    if isinstance(data, list):
                        results_data.extend(data)
                    else:
                        results_data.append(data)
                except Exception as e:
                    print(f"Error parsing JSON for {res.url}: {e}")
            else:
                 print(f"Failed to scrape {res.url}: {res.error_message}")
    
    return results_data