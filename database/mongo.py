from motor.motor_asyncio import AsyncIOMotorClient
from models.recipe import ConcreteRecipe


class MongoDB:
    """Base class for MongoDB operations using Motor for async MongoDB access."""

    def __init__(self, uri: str, db_name: str):
        """Initialize MongoDB client and database asynchronously."""
        self.client = AsyncIOMotorClient(uri)  
        self.db = self.client[db_name]
        self.collection = self.db['recipes']

    async def save_recipes(self, recipes: list):
        """Save multiple recipes asynchronously to the MongoDB database."""
        recipes_dicts = []
        for recipe in recipes:
            recipe_dict = recipe.to_dict()
            if recipe_dict['_id'] is None:
                del recipe_dict['_id']
            recipes_dicts.append(recipe_dict)
        await self.collection.insert_many(recipes_dicts) 

    async def get_recipe(self, recipe_id: int):
        """Retrieve a recipe asynchronously by its ID."""
        recipe_dict = await self.collection.find_one({"_id": recipe_id})
        if recipe_dict:
            return ConcreteRecipe.from_dict(recipe_dict)
        return None, f"Recipe with ID: {recipe_id} not found"

    async def save_recipe(self, concrete_recipe: ConcreteRecipe):
        """Save a single recipe asynchronously to the MongoDB database."""
        concrete_recipe_dict = concrete_recipe.to_dict()
        _id = await self.collection.insert_one(concrete_recipe_dict) 
        return _id

    async def get_all_recipes(self):
        """Retrieve all recipes asynchronously."""
        cursor = self.collection.find()  
        recipes = await cursor.to_list(length=None) 
        return [ConcreteRecipe.from_dict(recipe) for recipe in recipes] 

    async def recipe_exists(self, recipe_id: int):
        """Check if a recipe exists in the database by its ID."""
        recipe = await self.collection.find_one({"_id": recipe_id}, {"_id": 1})
        return recipe is not None
    
    async def drop_collection(self):
        """Drop all documents from the collection."""
        await self.collection.drop()
    