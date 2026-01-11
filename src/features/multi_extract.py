import os
import subprocess
import sys

import json
import asyncio
import LLM_extraction
from crawl4ai import *
from convert_csv import create_csv





def ensure_browsers_installed():
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
    
    all_scraped_data = []
    
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        print(f"Starting crawl for {len(urls)} URLs...")
        
        
        results = await crawler.arun_many(
            urls=urls,
            config=run_conf
        )

        
        for result in results:
            if result.success:
                clean_text = result.extracted_content
                data = json.loads(clean_text)
                
                if isinstance(data, list):
                    all_scraped_data.extend(data) # Add multiple items
                else:
                    all_scraped_data.append(data) # Add single item
            
            else:
                print(f"Error: {result.error_message}")
            
    create_csv(all_scraped_data, "final_real_estate_data.csv")        
    

if __name__ == "__main__":
    ensure_browsers_installed()
    asyncio.run(main())