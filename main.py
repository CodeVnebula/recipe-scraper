import json
from models.recipe import ConcreteRecipe
from database.mongo import MongoDB
from config import MONGO_URI, DATABASE_NAME
import asyncio

async def main():
    db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)

    with open('recipes.json', 'r', encoding='utf-8') as file:
        recipes_data = json.load(file)

    recipes = []
    for recipe_data in recipes_data:
        recipe = ConcreteRecipe(
            title=recipe_data["title"],
            recipe_url=recipe_data["recipe_url"],
            main_category=recipe_data["main_category"],
            sub_category=recipe_data["sub_category"],
            image_url=recipe_data["image_url"],
            description=recipe_data["description"],
            author=recipe_data["author"],
            servings=recipe_data["servings"],
            ingredients=recipe_data["ingredients"],
            steps=recipe_data["steps"]
        )
        recipes.append(recipe)

    await db.save_recipes(recipes)
    
    # recipe = await db.get_recipe("<>")
    # if recipe:
    #     print(recipe.to_dict())

    print("Success")
if __name__ == '__main__':
    asyncio.run(main())
