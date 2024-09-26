import json
import time
import asyncio

from models.recipe import ConcreteRecipe
from database import MongoDB
from config import MONGO_URI, DATABASE_NAME
from scraper import RecipeScraper

from config import COMEULI_CATEGORY_URL


async def main():
    db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
    
    # await db.drop_collection()

    _scraper = RecipeScraper(
        category_url=COMEULI_CATEGORY_URL,
        page_limit=None
    )

    start = time.perf_counter()
    recipes_data = await _scraper.scrape_recipes()
    end_time = time.perf_counter() - start
   
    recipes = []
    for recipe_data in recipes_data:
        recipe = ConcreteRecipe.from_dict(recipe_data)
        
        await db.save_recipe(recipe)
        print(f"Recipe saved id: {recipe.id}")
        recipes.append(recipe)

    print()
    print(len(recipes_data), "recipes scraped")
    print(f"Found {_scraper.exists_in_db} existing recipes in database")
    print(f'Scraping took {end_time:.2f} seconds')
    print("Success")
    
if __name__ == '__main__':
    asyncio.run(main())
