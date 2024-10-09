from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DATABASE_NAME = "recipe_db"

KULINARIA_URL = "https://www.kulinaria.ge"

RECIPES_URL = KULINARIA_URL + '/receptebi/'

COMEULI_CATEGORY_URL = KULINARIA_URL + "/receptebi/cat/comeuli/"

CATEGORIES = [
    'ცომეული',
]
