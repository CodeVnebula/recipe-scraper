from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DATABASE_NAME = "recipe_db"

KULINARIA_URL = "https://www.kulinaria.ge"
COMEULI_CATEGORY_URL = KULINARIA_URL + "/receptebi/cat/comeuli/"

CATEGORIES = {
    'სალათები': '/receptebi/cat/salaTebi/',
    'ცომეული': '/receptebi/cat/comeuli/',
    'ნამცხვრები და ტორტები': '/receptebi/cat/namcxvrebi-da-tortebi/',
    'ხორცეული': '/receptebi/cat/xorceuli/',
    'წვნიანები': '/receptebi/cat/wvnianebi/',
    'ქართული სამზარეულო': '/receptebi/cat/karTuli-samzareulo/',
    'თევზი და ზღვის პროდუქტები': '/receptebi/cat/Tevzi-da-zRvis-produktebi/',
    'დესერტები და ტკბილეულობა': '/receptebi/cat/desertebi-da-tkbileuloba/',
    'სამარხვო/ვეგეტარიანული': '/receptebi/cat/samarxvovegetarianuli/',
    'მსოფლიო სამზარეულო': '/receptebi/cat/msoplio-samzareulo/',
    'სადღესასწაულო': '/receptebi/cat/sadResaswaulo/',
    'პასტა და ბურღულეული': '/receptebi/cat/pasta-da-burRuleuli/',
    'სასმელები': '/receptebi/cat/sasmelebi/',
    'კონსერვი და სოუსები': '/receptebi/cat/konservi-da-sousebi/',
    'აპეტაიზერები და გარნირები': '/receptebi/cat/apetaizerebi-da-garnirebi/',
    'ბავშვებისთვის': '/receptebi/cat/bavSvebisTvis/',
    'სხვა': '/receptebi/cat/sxva/',
}