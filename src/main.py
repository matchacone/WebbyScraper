import asyncio
import LLM_extraction
from crawl4ai import *


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
    asyncio.run(main())

        
