from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDB:
    """Base class for MongoDB operations."""

    def __init__(self, uri: str, db_name: str):
        """Initialize MongoDB client and database."""
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['recipes']

    async def save_recipes(self, recipes: list):
        """Save recipes asynchronously to the MongoDB database."""
        recipes_dicts = [recipe.to_dict() for recipe in recipes]
        await self.collection.insert_many(recipes_dicts)

    async def get_recipe(self, recipe_id: str):
        """Retrieve a recipe by its ID."""
        recipe_dict = await self.collection.find_one({"id": ObjectId(recipe_id)})
        if recipe_dict:
            return recipe_dict
        return None
