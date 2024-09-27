from PyQt5.QtWidgets import (
    QMainWindow, 
    QApplication,
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
import sys
import os
from config import CATEGORIES
from scraper import RecipeScraper
from models.recipe import ConcreteRecipe
from database.mongo import MongoDB
from qasync import asyncSlot


class Application(QMainWindow):
    def __init__(self, _scraper: RecipeScraper, db: MongoDB):
        self._scraper = _scraper
        self.db = db
        
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
        self.default_stats_page = self.findChild(QWidget, "default_stats_page")
        self.author_with_most_recipes_page = self.findChild(QWidget, "author_with_most_recipes_page")
        self.avg_pages = self.findChild(QWidget, "avg_pages")
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
        self.stackedWidget.setCurrentWidget(self.stats)
    
    def show_table_page(self):
        self.stackedWidget.setCurrentWidget(self.table_page)
    
    @asyncSlot()
    async def start_scrape(self):
        recipes_data = await self._scraper.scrape_recipes()
        recipes = []
        total_recipes = len(recipes_data)
        
        current_progress = 0

        for index, recipe_data in enumerate(recipes_data):
            recipe = ConcreteRecipe.from_dict(recipe_data)
            recipes.append(recipe)

            current_progress = (index + 1) / total_recipes * 100
            self.progressBar.setValue(int(current_progress))
            
            self.add_row_to_table(recipe_data)
            await self.db.save_recipe(recipe)
        
        self.progressBar.setValue(100)
        self.recipe_amount.setText(f"{len(recipes)}")
        
    def add_row_to_table(self, recipe_data: dict):
        # Check if recipe_data contains necessary fields before adding
        if not all(key in recipe_data for key in ('title', 'author', 'servings', 'recipe_url')):
            print("Missing fields in recipe data")
            return  # Exit the function if data is incomplete

        # Add recipe data to the current row in the table
        row = self.tableWidget.rowCount()  # Get the current number of rows
        self.tableWidget.insertRow(row)     # Insert a new row at the end

        # Set the items in the new row based on recipe data
        self.tableWidget.setItem(row, 0, QTableWidgetItem(recipe_data.get('title', '')))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(recipe_data.get('author', '')))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(recipe_data.get('servings', '')))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(recipe_data.get('recipe_url', '')))
        
        
        
    


