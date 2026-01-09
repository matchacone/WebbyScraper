import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

import LLM_extraction

async def main():
    
    scorer = KeywordRelevanceScorer(
        keywords=["Contact","contact","find","email","phone"],
        weight=0.7
    )
    
    strategy = BestFirstCrawlingStrategy(
        max_depth = 3,
        include_external=False,
        url_scorer=scorer,
        max_pages=10
    )
    
    config = CrawlerRunConfig(
        deep_crawl_strategy=strategy,
        extraction_strategy= LLM_extraction.llm_strategy,
        verbose=True,
    )

    all_scraped_data = []

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun("https://filipinohomes.com/agent-list.php", config=config)

        print(f"Crawled {len(results)} pages in total")
        
        for result in results[:3]:  # Show first 3 results
            print(f"URL: {result.url}")
            print(f"Depth: {result.metadata.get('depth', 0)}")

if __name__ == "__main__":
    asyncio.run(main())