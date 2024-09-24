from abc import ABC, abstractmethod

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
