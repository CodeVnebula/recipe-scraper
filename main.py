import asyncio
import time
import json

from scraper import RecipeScraper
from config import COMEULI_CATEGORY_URL


async def main():
    _scraper = RecipeScraper(
        category_url=COMEULI_CATEGORY_URL,
        page_limit=None
    )

    start = time.perf_counter()
    result = await _scraper.scrape_recipes()
    print(len(result), "recipes scraped")
    print(f'Scraping took {time.perf_counter() - start} seconds')

    with open('recipes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    asyncio.run(main())
