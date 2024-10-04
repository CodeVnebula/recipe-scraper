from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DATABASE_NAME = "recipe_db"

KULINARIA_URL = "https://www.kulinaria.ge"
COMEULI_CATEGORY_URL = KULINARIA_URL + "/receptebi/cat/comeuli/"

CATEGORIES = [
    'სალათები',
    'ცომეული',
    'ნამცხვრები და ტორტები',
    'ხორცეული',
    'წვნიანები',
    'ქართული სამზარეულო',
    'თევზი და ზღვის პროდუქტები',
    'დესერტები და ტკბილეულობა',
    'სამარხვო/ვეგეტარიანული',
    'მსოფლიო სამზარეულო',
    'სადღესასწაულო',
    'პასტა და ბურღულეული',
    'სასმელები',
    'კონსერვი და სოუსები',
    'აპეტაიზერები და გარნირები',
    'ბავშვებისთვის',
    'სხვა',
]