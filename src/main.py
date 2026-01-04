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
        # A simple check (this is a bit hacky but works for simple apps)
        # We try to run a playwright command. If it fails, we install.
        subprocess.run(["playwright", "--version"], check=True, stdout=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("First time setup: Installing browsers (this takes a minute)...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("Browser setup complete!")


async def main():
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
        
        #word_count_threshold=10,
        page_timeout=80000,
        extraction_strategy=LLM_extraction.llm_strategy,
        
        excluded_tags= ["style", "noscript"],
        exclude_external_links=False,
    )
    
    
    async with AsyncWebCrawler(config = browser_conf) as crawler:
        result = await crawler.arun(
            url="https://www.zillow.com/profile/Matt-Laricy",
            config = run_conf
        )
        if result.success:
            print(result.markdown)
            print(result.extracted_content)
        else:
            print(f"Error: {result.error_message}")

if __name__ == "__main__":
    ensure_browsers_installed()
    asyncio.run(main())

        
