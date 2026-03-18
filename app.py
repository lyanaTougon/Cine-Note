from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ma_base']
collection = db['items']

# Films pour carrousel (images locales dans static/images/)
films_carrousel = [
    {
    "title": "Avatar 3",
    "url": "/films/avatar3",
    "image": "avatar3.jpeg",
    "description": "Jake Sully et Neytiri affrontent une nouvelle menace sur Pandora dans un monde encore plus spectaculaire.",
    "color1": "#000428",  # bleu nuit profond
    "color2": "#1A0033"   # violet très foncé
},
    {
        "title": "Suzume",
        "url": "/films/suzume",
        "image": "suzume.jpg",
        "description": "Une jeune fille aventureuse part sauver des secrets mystiques.",
        "color1": "#87CEFA",  # bleu clair
        "color2": "#1E90FF"   # bleu foncé
    },
{
    "title": "Ballerina",
    "url": "/films/ballerina",
    "image": "ballerina.webp",
    "description": "Une tueuse redoutable formée dans l’ombre cherche à se venger dans un monde impitoyable.",
        "color1": "#9370DB",  # violet clair
        "color2": "#1A0033"   # violet foncé
},


]

# Films récents
films_recents = [
    {"title": "Zootopie 2", "url": "/films/zootopie2", "image": "zootopie2_couv.jpg"},

]

# Films à venir
films_avenir = [
    {"title": "Film A Venir 1", "url": "/films/avenir1", "image": "avenir1.jpg"},
    {"title": "Film A Venir 2", "url": "/films/avenir2", "image": "avenir2.jpg"},
]

films_a_decouvrir = [
    {
        "title": "Chainsawman",
        "url": "/films/chainsawman",
        "image": "chainsawman_couv.jpg",
        "genres": ["Action", "Drame"]
    },
        {
        "title": "Parasite",
        "url": "/films/parasite",
        "image": "parasite_couv.webp",
        "genres": ["Drame", "Thriller"]
    },
            {
        "title": "Spider-Verse",
        "url": "/films/spiderverse",
        "image": "spiderverse_couv.jpg",
        "genres": ["Action", "Aventure"]
    },
                {
        "title": "Tenet",
        "url": "/films/tenet",
        "image": "tenet_couv.webp",
        "genres": ["Action", "Drame"]
    },
   
]

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ""
    results = []
    if request.method == 'POST':
        query = request.form.get('search')
        results = list(collection.find({"name": {"$regex": query, "$options": "i"}}))
    return render_template('index.html', query=query, results=results,
                           films_carrousel=films_carrousel,
                           films_recents=films_recents,
                           films_avenir=films_avenir,
                           films_a_decouvrir=films_a_decouvrir)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
