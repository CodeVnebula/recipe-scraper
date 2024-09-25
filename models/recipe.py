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
