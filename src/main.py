import asyncio
import LLM_extraction
from crawl4ai import *


async def main():
    browser_conf = BrowserConfig(headless=False, verbose=True)
    md_generator = DefaultMarkdownGenerator()
    
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        verbose=True,
        markdown_generator=md_generator,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=LLM_extraction.llm_strategy,
        excluded_tags=['nav', 'footer', 'header', 'script', 'style', 'aside'],
    )
    
    
    async with AsyncWebCrawler(config = browser_conf) as crawler:
        result = await crawler.arun(
            url="https://filipinohomes.com/shane-thurkle",
            config = run_conf
        )
        if result.success:
            print(result.extracted_content)
        else:
            print(f"Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())

        
