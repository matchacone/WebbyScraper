import os
import subprocess
import sys

import json
import asyncio
import LLM_extraction
from crawl4ai import *
from convert_csv import json_to_csv


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
    
    scroll_script = """
        async function scrollDown() {
            let totalHeight = 0;
            let distance = 300; // Scroll 300px at a time
            
            while (totalHeight < document.body.scrollHeight) {
                window.scrollBy(0, distance);
                totalHeight += distance;
                // Wait 100ms between scrolls to let the page catch up
                await new Promise(r => setTimeout(r, 100)); 
            }
        }
        await scrollDown();
    """
    
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        verbose=True,   
        markdown_generator=md_generator,
        magic = True,
        
        #word_count_threshold=10,
        page_timeout=60000,
        wait_until="domcontentloaded",
        delay_before_return_html=5.0,
        
        # 2. CONTENT FIXES
        remove_overlay_elements=True, 
        js_code=scroll_script,
        
        extraction_strategy=LLM_extraction.llm_strategy,
        excluded_tags=["style", "noscript", "script", "nav", "footer"],
        exclude_external_links=False,
    )
    
    
    async with AsyncWebCrawler(config = browser_conf) as crawler:
        for attempt in range(3):
            try:
                result = await crawler.arun(
                    url="https://www.zillow.com/profile/Matt-Laricy",
                    config=run_conf
                )
                
                if result.success:
                    raw_json = result.extracted_content
                    json_to_csv(raw_json)
                    
                    break
                else:
                    print(f"Attempt {attempt+1} failed: {result.error_message}")
            
            except Exception as e:
                print(f"Crawl crashed on attempt {attempt+1}: {e}")

            # cooldown
            await asyncio.sleep(5)

if __name__ == "__main__":
    ensure_browsers_installed()
    asyncio.run(main())

        
