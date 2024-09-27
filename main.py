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


async def main():
    db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
    await db.drop_collection()
    db.client.close()
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = Application()
    window.show()
    with loop:
        loop.run_forever()

if __name__ == '__main__':
    asyncio.run(main())