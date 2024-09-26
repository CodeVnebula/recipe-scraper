import time
import asyncio

from models import ConcreteRecipe
from database import MongoDB, Statistics
from config import MONGO_URI, DATABASE_NAME
from scraper import RecipeScraper

from config import COMEULI_CATEGORY_URL


async def mystatistics():
    db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)

    statistics = Statistics(db)

    avg_steps, avg_ingredients, most_active_author, most_servings_recipe = await asyncio.gather(
        statistics.average_steps_per_recipe(),
        statistics.average_ingredients_per_recipe(),
        statistics.most_active_author(),
        statistics.recipe_with_most_servings()
    )

    print()
    print("Average steps per recipe:", round(avg_steps, 2))
    print()
    print("Average ingredients per recipe:", round(avg_ingredients, 2))
    print()
    print(f"Most active author: '{most_active_author.get('author')}'", end=" ")
    print("with", most_active_author.get('recipe_count'), "recipes")
    print()
    print(f"Most servings recipe: '{most_servings_recipe.get('recipe_title')}'", end=" ")
    print("with", most_servings_recipe.get('servings'), "servings")
    print("Recipe URL:", most_servings_recipe.get('recipe_url'))
    print()


async def main():
    db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
    
    # await db.drop_collection()

    _scraper = RecipeScraper(
        category_url=COMEULI_CATEGORY_URL,
        page_limit=None,
        db=db
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

    await mystatistics()
    
if __name__ == '__main__':
    asyncio.run(main())
