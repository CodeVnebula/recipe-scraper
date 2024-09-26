from abc import ABC, abstractmethod
from database import MongoDB
from bson.son import SON


class RecipeStatistics(ABC):
    """Abstract base class for recipe statistics operations."""

    @abstractmethod
    async def average_ingredients_per_recipe(self) -> float:
        """Calculate and return the average number of ingredients per recipe."""
        pass

    @abstractmethod
    async def average_steps_per_recipe(self) -> float:
        """Calculate and return the average number of preparation steps per recipe."""
        pass

    @abstractmethod
    async def recipe_with_most_servings(self) -> dict:
        """Find the recipe with the most servings and return its name and URL."""
        pass

    @abstractmethod
    async def most_active_author(self) -> dict:
        """Find the author with the most recipes and return the author's name and count."""
        pass


class Statistics(RecipeStatistics):
    """Statistics class for the recipe statistics operations."""
    def __init__(self, db: MongoDB) -> None:
        self.__db = db
        self.__collection = db.collection

    async def average_ingredients_per_recipe(self) -> float:
        """Calculate the average number of ingredients per recipe."""
        pipeline = [
            {
                "$project": {
                    "ingredients_count": {"$size": {"$ifNull": ["$ingredients", []]}}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_ingredients_per_recipe": {"$avg": "$ingredients_count"}
                }
            }
        ]

        result = await self.__collection.aggregate(pipeline).to_list(None)
        return result[0]['average_ingredients_per_recipe'] if result else 0

    async def average_steps_per_recipe(self) -> float:
        """Calculate the average number of steps per recipe."""
        pipeline = [
            {
                "$project": {
                    "steps_count": {"$size": {"$ifNull": ["$steps", []]}}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_steps_per_recipe": {"$avg": "$steps_count"}
                }
            }
        ]

        result = await self.__collection.aggregate(pipeline).to_list(None)
        return result[0]['average_steps_per_recipe'] if result else 0

    async def recipe_with_most_servings(self) -> dict:
        """Find the recipe with the most servings."""
        pipeline = [
            {
                "$group": {
                    "_id": "$_id",
                    "recipe_title": {"$first": "$title"},
                    "recipe_url": {"$first": "$recipe_url"},
                    "servings": {"$max": "$servings"}
                }
            },
            {
                "$sort": SON([("servings", -1)])  # Sort by recipe_count in descending order
            },
            {
                "$limit": 1  # Limit to the top author
            }
        ]

        result = await self.__collection.aggregate(pipeline).to_list(None)
        return result[0] if result else {}

    async def most_active_author(self) -> dict:
        """Find the most active author."""
        pipeline = [
            {
                "$group": {
                    "_id": "$author",
                    "recipe_count": {"$sum": 1},
                }
            },
            {
                "$sort": SON([("recipe_count", -1)])
            },
            {
                "$limit": 1
            },
            {
                "$project": {
                    "author": "$_id",
                    "recipe_count": "$recipe_count",
                    "_id": 0
                }
            }
        ]

        result = await self.__collection.aggregate(pipeline).to_list(None)
        return result[0] if result else {}
