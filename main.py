from ui.load_ui import Application
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
import sys
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
    
    return avg_steps, avg_ingredients, most_active_author, most_servings_recipe


async def setup_app():
    db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
    await db.drop_collection()  # Clear existing data if necessary
    _scraper = RecipeScraper(
        category_url=COMEULI_CATEGORY_URL,
        page_limit=None,
        db=db
    )

    return _scraper, db

async def main():
    # Initialize QApplication and event loop
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Set up the application and scrape data
    _scraper, db = await setup_app()
    
    window = Application(_scraper, db)
    window.show()

    # Start the application loop
    with loop:
        app.exec_()  # Just call exec_() without await

if __name__ == "__main__":
    asyncio.run(main())
