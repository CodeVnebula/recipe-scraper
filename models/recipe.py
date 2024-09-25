from abc import ABC, abstractmethod

class Recipe(ABC):
    @abstractmethod
    def __init__(self, 
                 title: str, 
                 recipe_url: str, 
                 main_category: dict, 
                 sub_category: dict, 
                 image_url: str, 
                 description: str, 
                 author: str, 
                 servings: int, 
                 ingredients: list, 
                 steps: list):
        """
        Args:
            title (str): The title of the recipe.
            recipe_url (str): The URL of the recipe page.
            main_category (dict): The main category of the recipe (title and URL).
            sub_category (dict): The subcategory of the recipe (title and URL).
            image_url (str): URL of the main image of the recipe.
            description (str): Short description of the recipe.
            author (str): The name of the author.
            servings (int): The number of servings.
            ingredients (list): A list of ingredients.
            steps (list): A list of preparation steps (each with a number and description).
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Convert the Recipe object into a dictionary for MongoDB storage.
        
        Returns:
            dict: The recipe represented as a dictionary.
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, recipe_dict: dict):
        """
        Create a Recipe object from a dictionary.
        
        Args:
            recipe_dict (dict): The dictionary representation of the recipe.
            
        Returns:
            Recipe: The Recipe object.
        """
        pass
    

class ConcreteRecipe(Recipe):
    def __init__(self, 
                 title: str, 
                 recipe_url: str, 
                 main_category: dict, 
                 sub_category: dict, 
                 image_url: str, 
                 description: str, 
                 author: str, 
                 servings: int, 
                 ingredients: list, 
                 steps: list):
        self.title = title
        self.recipe_url = recipe_url
        self.main_category = main_category
        self.sub_category = sub_category
        self.image_url = image_url
        self.description = description
        self.author = author
        self.servings = servings
        self.ingredients = ingredients
        self.steps = steps

    @classmethod
    def to_dict(self) -> dict:
        """Converts the Recipe object to a dictionary for MongoDB storage."""
        return {
            "title": self.title,
            "recipe_url": self.recipe_url,
            "main_category": self.main_category,
            "sub_category": self.sub_category,
            "image_url": self.image_url,
            "description": self.description,
            "author": self.author,
            "servings": self.servings,
            "ingredients": self.ingredients,
            "steps": self.steps
        }

    @classmethod
    def from_dict(cls, recipe_dict: dict):
        """Creates a Recipe object from a MongoDB dictionary."""
        return cls(
            title=recipe_dict.get("title"),
            recipe_url=recipe_dict.get("recipe_url"),
            main_category=recipe_dict.get("main_category"),
            sub_category=recipe_dict.get("sub_category"),
            image_url=recipe_dict.get("image_url"),
            description=recipe_dict.get("description"),
            author=recipe_dict.get("author"),
            servings=recipe_dict.get("servings"),
            ingredients=recipe_dict.get("ingredients"),
            steps=recipe_dict.get("steps")
        )