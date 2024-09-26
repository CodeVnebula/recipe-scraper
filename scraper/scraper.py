import aiohttp
import asyncio

from bs4 import Tag
from scraper.parser import MainPageParser, RecipeParser


class RecipeScraper:
    def __init__(self, category_url: str, page_limit: int | None = None):
        self.page_limit = page_limit
        self.category = category_url
        self._page_number = 1
        self._all_recipes = []
        self._tasks = []
        self.__lock = asyncio.Lock()

    async def print(self, *args, **kwargs) -> None:
        async with self.__lock:
            print(*args, **kwargs)

    @staticmethod
    async def _fetch_html(url: str) -> str:
        """Fetch HTML content from the given URL."""
        async with aiohttp.request('GET', url) as response:
            return await response.text()

    async def _scrape_post(self, post: Tag) -> dict | None:
        """Scrape individual post for recipe data."""
        post_data = MainPageParser.scrape_post(post)

        if post_data.get('recipe_url'):
            await self.print('Scraping post', post_data.get('recipe_url'))
            detailed_data = await self._fetch_recipe_details(post_data.get('recipe_url'), return_all_data=False)
            post_data.update(detailed_data)

        return post_data

    async def _fetch_recipe_details(self, recipe_url: str | bytes, return_all_data: bool = True) -> dict:
        """Fetch recipe details from the recipe URL."""
        try:
            html = await self._fetch_html(recipe_url)
        except aiohttp.client_exceptions:
            return {}

        soup = RecipeParser(html)

        return soup.parse(return_all_data=return_all_data)

    async def scrape_recipes(self) -> list:
        """Scrape recipes from multiple pages."""
        soup = None

        while True:
            # Construct the URL for the current page
            if soup and soup.next_url:
                current_page_url = soup.next_url
            else:
                current_page_url = f"{self.category}/?page={self._page_number}"

            await self.print('Scraping page', current_page_url)

            try:
                main_html = await self._fetch_html(current_page_url)
            except aiohttp.client_exceptions:
                await self.print('Failed to scrape page', current_page_url)
                continue

            soup = MainPageParser(main_html)

            posts = soup.get_posts()

            # Initiate scraping of posts without waiting for them to finish
            for post in posts:
                task = asyncio.create_task(self._scrape_post(post))
                self._tasks.append(task)

            if not soup.has_next:
                break

            if self.page_limit is not None and self._page_number >= self.page_limit:
                await self.print('Page limit reached')
                break

            self._page_number += 1  # Move to the next page

        # Wait for all tasks to complete and gather results
        recipes_data = await asyncio.gather(*self._tasks)
        self._all_recipes.extend(recipes_data)

        return self._all_recipes
