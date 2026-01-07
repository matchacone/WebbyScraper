import os
import subprocess
import sys

import asyncio
import LLM_extraction
from crawl4ai import *

def ensure_browsers_installed():
    """Checks if Playwright browsers are present. If not, installs them."""
    print("Checking browser components...")
    try:
        subprocess.run(["playwright", "--version"], check=True, stdout=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("First time setup: Installing browsers (this takes a minute)...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("Browser setup complete!")

async def main():
    urls = [
        "https://www.zillow.com/profile/Matt-Laricy",
        "https://www.zillow.com/profile/SKGroup", 
        #Add more URLs to this list as needed
    ]

    browser_conf = BrowserConfig(headless=True, verbose=True)
    
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": False,
            "escape_asterisks": False
        }
    )
    
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        verbose=True,   
        markdown_generator=md_generator,
        page_timeout=80000,
        extraction_strategy=LLM_extraction.llm_strategy,
        excluded_tags=["style", "noscript"],
        exclude_external_links=False,
    )
    
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        print(f"Starting crawl for {len(urls)} URLs...")
        
        
        results = await crawler.arun_many(
            urls=urls,
            config=run_conf
        )

        
        for result in results:
            print(f"\n{'='*40}")
            print(f"URL: {result.url}")
            
            if result.success:
                print("--- Extracted Content ---")
                print(result.extracted_content)
                #print(result.markdown)
            else:
                print(f"Error: {result.error_message}")
            
            print(f"{'='*40}\n")

if __name__ == "__main__":
    ensure_browsers_installed()
    asyncio.run(main())