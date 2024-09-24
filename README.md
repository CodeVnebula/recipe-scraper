# Recipe Scraping Project

This project involves scraping recipes from [kulinaria.ge](https://kulinaria.ge) and storing them in a MongoDB database. The application extracts recipe details such as title, URL, categories, ingredients, and preparation steps. It also calculates statistics regarding the recipes stored in the database.

## Features

- Scrape recipe data from a specified category on kulinaria.ge.
- Store recipe details in MongoDB.
- Calculate statistics such as:
  - Average number of ingredients per recipe.
  - Average number of preparation steps per recipe.
  - Recipe with the most servings.
  - Most active author with the highest number of recipes.
- Utilizes `asyncio` for efficient asynchronous operations, allowing for improved performance during web scraping and database interactions.

## Directory Structure

```bash
recipe_scraper/
│
├── database/
│   ├── __init__.py
│   ├── mongo.py           # MongoDB connection and CRUD operations
│   └── statistics.py      # Statistics calculations for recipes
│
├── models/
│   ├── __init__.py
│   └── recipe.py          # Recipe schema and definition
│
├── scraper/
│   ├── __init__.py
|   ├── parser.py          # Html parser
│   └── scraper.py         # Recipe scraper
│
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Helper functions for scraping and processing data
│
├── main.py                # Main script to run the scraper
├── .env                   # Environment variables for MongoDB connection
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/recipe_scraper.git
   cd recipe_scraper
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your MongoDB connection string:
   ```
   MONGODB_URI=mongodb://localhost:27017
   ```

## Usage

1. Run the main script to start scraping recipes:
   ```bash
   python main.py
   ```

2. The application will scrape recipes from the specified category on kulinaria.ge and store them in MongoDB. 

3. After scraping, you can calculate statistics by invoking the respective methods defined in the `RecipeStatistics` class.

## Contribution

This project is a collaborative effort between me and [CodeVnebula](https://github.com/CodeVnebula).


## Acknowledgments

- [kulinaria.ge](https://kulinaria.ge) for providing the recipe data.
- [MongoDB](https://www.mongodb.com) for database management.
- [Python](https://www.python.org) for the programming language.
- [asyncio](https://docs.python.org/3/library/asyncio.html) for enabling asynchronous programming in Python.
- [Beautiful Soup 4 (bs4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for web scraping and parsing HTML.
