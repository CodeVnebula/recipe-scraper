import asyncio

from PyQt5.QtWidgets import (
    QMainWindow, 
    QWidget,
    QStackedWidget,
    QComboBox,
    QPushButton,
    QLabel,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QListWidget
)
from PyQt5 import uic
import os
from config import CATEGORIES
from scraper import RecipeScraper
from database.mongo import MongoDB
from database.statistics import Statistics
from qasync import asyncSlot

from config import MONGO_URI, DATABASE_NAME, COMEULI_CATEGORY_URL


class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()

        self.db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
        self.statistics = Statistics(self.db)

        ui_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.ui")
        uic.loadUi(ui_file, self) 
        self.stackedWidget: QStackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.category_combobox: QComboBox = self.findChild(QComboBox, "category_combobox")
        self.start_scrape_button: QPushButton = self.findChild(QPushButton, "start_scrape_button")
        self.progressBar: QProgressBar = self.findChild(QProgressBar, "progressBar")
        self.recipe_amount: QLabel = self.findChild(QLabel, "recipe_amount")
        self.stats_button: QPushButton = self.findChild(QPushButton, "stats_button")
        self.main_window_button: QPushButton = self.findChild(QPushButton, "main_window_button")

        self.details_button: QPushButton = self.findChild(QPushButton, "extra_info_button")
        self.details_label: QLabel = self.findChild(QLabel, "selected_recipe_label")
        self.selected_item_id: int | None = None
        
        self.table_page: QWidget = self.findChild(QWidget, "table_page")
        self.recipe_details_page: QWidget = self.findChild(QWidget, "recipe_details_page")
        
        """Recipe details widgets"""
        self.default_details_page: QWidget = self.findChild(QWidget, "default_details_page")
        self.category_page: QWidget = self.findChild(QWidget, "category_page")
        self.lists_page: QWidget = self.findChild(QWidget, "lists_page")
        self.listWidget: QListWidget = self.findChild(QListWidget, "listWidget")
        self.recipe_image_label: QLabel = self.findChild(QLabel, "recipe_image_label")
        self.category_title: QLabel = self.findChild(QLabel, "category_title")
        self.url_label: QLabel = self.findChild(QLabel, "url_label")
        self.recipe_title: QLabel = self.findChild(QLabel, "recipe_title")
        self.servings: QLabel = self.findChild(QLabel, "servings")
        self.recipe_description: QTextBrowser = self.findChild(QTextBrowser, "recipe_description")
        self.recipe_id: QLabel = self.findChild(QLabel, "recipe_id")
        self.main_categor_button: QPushButton = self.findChild(QPushButton, "main_categor_button")
        self.sub_category_button: QPushButton = self.findChild(QPushButton, "sub_category_button")
        self.ingredients_button: QPushButton = self.findChild(QPushButton, "ingredients_button")
        self.steps_button: QPushButton = self.findChild(QPushButton, "steps_button")

        """Stats page widgets"""
        self.tableWidget: QTableWidget = self.findChild(QTableWidget, "tableWidget")
        self.stats_stackedWidget: QStackedWidget = self.findChild(QStackedWidget, "stats_stackedWidget")
        self.most_recipes_author_button: QPushButton = self.findChild(QPushButton, "most_recipes_author_button")
        self.avg_steps_button: QPushButton = self.findChild(QPushButton, "avg_steps_button")
        self.avg_ingredients_button: QPushButton = self.findChild(QPushButton, "avg_ingredients_button")
        self.most_servings_button: QPushButton = self.findChild(QPushButton, "most_servings_button")
        self.default_stats_page: QWidget = self.findChild(QWidget, "default_stats_page")
        self.author_with_most_recipes_page: QWidget = self.findChild(QWidget, "author_with_most_recipes_page")
        self.avg_pages: QWidget = self.findChild(QWidget, "avg_pages")
        self.most_servings_recipe_page: QWidget = self.findChild(QWidget, "most_servings_recipe_page")
        self.author_name_label: QLabel = self.findChild(QLabel, "author_name_label")
        self.avg_label: QLabel = self.findChild(QLabel, "avg_label")
        self.recipe_name_stats_label: QLabel = self.findChild(QLabel, "recipe_name_stats_label")
        self.recipe_url_stats_label: QLabel = self.findChild(QLabel, "recipe_url_stats_label")
        self.default_stats_button: QPushButton = self.findChild(QPushButton, "default_stats_button")

        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        
        self.progressBar.setValue(0)
        self.stackedWidget.setCurrentWidget(self.table_page)
        self.category_combobox.addItems(CATEGORIES)
        
        self.start_scrape_button.clicked.connect(self.start_scrape)
        self.main_window_button.clicked.connect(self.show_table_page)
        self.stats_button.clicked.connect(self.show_stats_page)
        self.details_button.clicked.connect(self.show_details_page)

        self.tableWidget.setColumnHidden(4, True)

    def on_item_clicked(self, item):
        row = item.row()

        _id = self.tableWidget.item(row, 4).text()
        title = self.tableWidget.item(row, 0).text()

        self.selected_item_id = int(_id) if _id.isdigit() else None
        self.details_label.setText(title)

    def show_stats_page(self):
        self.details_button.hide()
        self.details_label.hide()
        self.stackedWidget.setCurrentWidget(self.stats)
        self.stats_stackedWidget.setCurrentWidget(self.most_servings_recipe_page)
        self.default_stats_button.clicked.connect(self.show_default_stats_page)
        self.most_recipes_author_button.clicked.connect(self.show_author_with_most_recipes_page)
        self.avg_steps_button.clicked.connect(self.show_avg_steps_page)
        self.avg_ingredients_button.clicked.connect(self.show_avg_ingredients_page)
        self.most_servings_button.clicked.connect(self.show_most_servings_page)

    
    @asyncSlot()
    async def show_avg_steps_page(self):
        self.stats_stackedWidget.setCurrentWidget(self.avg_page)
        avg_steps = await self.statistics.average_steps_per_recipe()
        self.avg_label.setText(f"{avg_steps:.2f}")
        
    @asyncSlot()
    async def show_avg_ingredients_page(self):
        self.stats_stackedWidget.setCurrentWidget(self.avg_page)
        avg_ingredients = await self.statistics.average_ingredients_per_recipe()
        self.avg_label.setText(f"{avg_ingredients:.2f}")
    
    @asyncSlot()
    async def show_most_servings_page(self):
        self.stats_stackedWidget.setCurrentWidget(self.most_servings_recipe_page)
        most_servings_recipe = await self.statistics.recipe_with_most_servings()
        self.recipe_name_stats_label.setText(most_servings_recipe.get('recipe_title', 'No data yet'))
        self.recipe_url_stats_label.setText(most_servings_recipe.get('recipe_url', 'No data yet'))
        
    def show_default_stats_page(self):
        self.recipe_name_stats_label.setText('')
        self.recipe_url_stats_label.setText('')
        self.stats_stackedWidget.setCurrentWidget(self.most_servings_recipe_page)

    @asyncSlot()
    async def show_author_with_most_recipes_page(self):
        self.stats_stackedWidget.setCurrentWidget(self.author_with_most_recipes_page)
        author_name = await self.statistics.most_active_author()
        self.author_name_label.setText(author_name.get('author', 'No data yet'))  
        
    def show_table_page(self):
        self.stackedWidget.setCurrentWidget(self.table_page)
        self.details_button.show()
        self.details_label.setText('')
        self.details_label.show()

    def show_details_page(self):
        self.stackedWidget.setCurrentWidget(self.recipe_details_page)
        self.details_button.hide()
        self.details_label.hide()
    
    @asyncSlot()
    async def start_scrape(self, scrape_data: bool = True):
        db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
        _scraper = RecipeScraper(COMEULI_CATEGORY_URL, None, db)

        _scraper.myfunction = self.add_row_to_table
        _scraper.progressbar_function = self.progressBar.setValue
        _scraper.recipe_count_function = self.recipe_amount.setText

        self.progressBar.setValue(0)
        # await _scraper.scrape_recipes()
        all_recipes = await db.get_all_recipes()
        db.client.close()

        for recipe in all_recipes:
            self.add_row_to_table(recipe.to_dict())

        self.progressBar.setValue(100)
        self.recipe_amount.setText(f"{len(all_recipes)}")

    @asyncSlot()
    async def load_data_from_database(self):
        db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
        all_recipes = await db.get_all_recipes()
        db.client.close()

        for recipe in all_recipes:
            self.add_row_to_table(recipe.to_dict())

        self.recipe_amount.setText(f"{len(all_recipes)}")

    def add_row_to_table(self, recipe_data: dict):
        if not all(key in recipe_data for key in ('title', 'author', 'servings', 'recipe_url')):
            print("Missing fields in recipe data")
            return

        servings = recipe_data.get('servings', '')
        servings = 0 if servings is None else str(servings)

        row = self.tableWidget.rowCount() 
        self.tableWidget.insertRow(row)    

        self.tableWidget.setItem(row, 0, QTableWidgetItem(recipe_data.get('title', '')))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(recipe_data.get('author', '')))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(servings))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(recipe_data.get('recipe_url', '')))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(str(recipe_data.get('_id', ''))))

    def closeEvent(self, event):
        self.db.client.close()
        event.accept()

    async def show(self):
        await self.load_data_from_database()
        super().show()
