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
        "title": "Scream 7",
        "url": "/films/scream7",
        "image": "scream7.webp",
        "description": "Un film captivant plein de rebondissements.",
        "color1": "#000000",  # noir
        "color2": "#FF8C00"   # orange
        
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
    {"title": "Film Récent 1", "url": "/films/recent1", "image": "recent1.jpg"},
    {"title": "Film Récent 2", "url": "/films/recent2", "image": "recent2.jpg"},
    {"title": "Film Récent 3", "url": "/films/recent3", "image": "recent3.jpg"},
]

# Films à venir
films_avenir = [
    {"title": "Film A Venir 1", "url": "/films/avenir1", "image": "avenir1.jpg"},
    {"title": "Film A Venir 2", "url": "/films/avenir2", "image": "avenir2.jpg"},
    {"title": "Film A Venir 3", "url": "/films/avenir3", "image": "avenir3.jpg"},
]

# Films à découvrir
films_a_decouvrir = [
    {"title": "Film Découvrir 1", "url": "/films/decouvrir1", "image": "decouvrir1.jpg"},
    {"title": "Film Découvrir 2", "url": "/films/decouvrir2", "image": "decouvrir2.jpg"},
    {"title": "Film Découvrir 3", "url": "/films/decouvrir3", "image": "decouvrir3.jpg"},
    {"title": "Film Découvrir 4", "url": "/films/decouvrir4", "image": "decouvrir4.jpg"},
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
