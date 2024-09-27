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
        ui_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.ui")
        uic.loadUi(ui_file, self) 
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.category_combobox = self.findChild(QComboBox, "category_combobox")
        self.start_scrape_button = self.findChild(QPushButton, "start_scrape_button")
        self.progressBar = self.findChild(QProgressBar, "progressBar")
        self.recipe_amount = self.findChild(QLabel, "recipe_amount")
        self.stats_button = self.findChild(QPushButton, "stats_button")
        self.main_window_button = self.findChild(QPushButton, "main_window_button")
        
        self.table_page = self.findChild(QWidget, "table_page")
        self.recipe_details_page = self.findChild(QWidget, "recipe_details_page")
        
        """Recipe details widgets"""
        self.default_details_page = self.findChild(QWidget, "default_details_page")
        self.category_page = self.findChild(QWidget, "category_page")
        self.lists_page = self.findChild(QWidget, "lists_page")
        self.listWidget = self.findChild(QListWidget, "listWidget")
        self.recipe_image_label = self.findChild(QLabel, "recipe_image_label")
        self.category_title = self.findChild(QLabel, "category_title")
        self.url_label = self.findChild(QLabel, "url_label")
        self.recipe_title = self.findChild(QLabel, "recipe_title")
        self.servings = self.findChild(QLabel, "servings")
        self.recipe_description = self.findChild(QTextBrowser, "recipe_description")
        self.recipe_id = self.findChild(QLabel, "recipe_id")
        self.main_categor_button = self.findChild(QPushButton, "main_categor_button")
        self.sub_category_button = self.findChild(QPushButton, "sub_category_button")
        self.ingredients_button = self.findChild(QPushButton, "ingredients_button")
        self.steps_button = self.findChild(QPushButton, "steps_button")

        """Stats page widgets"""
        self.tableWidget = self.findChild(QTableWidget, "tableWidget")
        self.stats_stackedWidget = self.findChild(QStackedWidget, "stats_stackedWidget")
        self.most_recipes_author_button = self.findChild(QPushButton, "most_recipes_author_button")
        self.avg_steps_button = self.findChild(QPushButton, "avg_steps_button")
        self.avg_ingredients_button = self.findChild(QPushButton, "avg_ingredients_button")
        self.most_servings_button = self.findChild(QPushButton, "most_servings_button")
        self.author_with_most_recipes_page = self.findChild(QWidget, "author_with_most_recipes_page")
        self.avg_page = self.findChild(QWidget, "avg_page")
        self.most_servings_recipe_page = self.findChild(QWidget, "most_servings_recipe_page")
        self.author_name_label = self.findChild(QLabel, "author_name_label")
        self.avg_label = self.findChild(QLabel, "avg_label")
        self.recipe_name_stats_label = self.findChild(QLabel, "recipe_name_stats_label")
        self.recipe_url_stats_label = self.findChild(QLabel, "recipe_url_stats_label")
        self.default_stats_button = self.findChild(QPushButton, "default_stats_button")
        
        self.progressBar.setValue(0)
        self.stackedWidget.setCurrentWidget(self.table_page)
        self.category_combobox.addItems(CATEGORIES)
        
        self.start_scrape_button.clicked.connect(self.start_scrape)
        self.main_window_button.clicked.connect(self.show_table_page)
        self.stats_button.clicked.connect(self.show_stats_page)
    
    
    def show_stats_page(self):
        db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
        self.statistics = Statistics(db)
        self.stackedWidget.setCurrentWidget(self.stats)
        self.stats_stackedWidget.setCurrentWidget(self.default_stats_page)
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
        self.stats_stackedWidget.setCurrentWidget(self.most_recipes_author_page)
        
    @asyncSlot()
    async def show_author_with_most_recipes_page(self):
        self.stats_stackedWidget.setCurrentWidget(self.author_with_most_recipes_page)
        author_name = await self.statistics.most_active_author()
        self.author_name_label.setText(author_name.get('author', 'No data yet'))  
        
    def show_table_page(self):
        self.stackedWidget.setCurrentWidget(self.table_page)
        
    @asyncSlot()
    async def start_scrape(self):
        db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
        _scraper = RecipeScraper(COMEULI_CATEGORY_URL, None, db)

        _scraper.myfunction = self.add_row_to_table
        _scraper.progressbar_function = self.progressBar.setValue
        _scraper.recipe_count_function = self.recipe_amount.setText

        self.progressBar.setValue(0)
        await _scraper.scrape_recipes()
        all_recipes = await db.get_all_recipes()
        db.client.close()

        for recipe in all_recipes:
            self.add_row_to_table(recipe.to_dict())

        self.progressBar.setValue(100)
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
