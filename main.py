from ui.load_ui import Application
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
import sys
import asyncio

from database import MongoDB, Statistics
from config import MONGO_URI, DATABASE_NAME


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
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = Application()
    await window.show()
    with loop:
        loop.run_forever()

if __name__ == '__main__':
    asyncio.run(main())
