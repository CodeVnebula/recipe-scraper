from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DATABASE_NAME = "recipe_db"

KULINARIA_URL = "https://www.kulinaria.ge"

# KULINARIA_RECIPE_URL = KULINARIA_URL / "receptebi/"
# '/' Throws an error because it's a string
# KULINARIA_RECIPE_URL = KULINARIA_URL + "/receptebi/..." 
KULINARIA_RECIPE_CATEGORY_URL = KULINARIA_URL / "receptebi/cat/comeuli/"
