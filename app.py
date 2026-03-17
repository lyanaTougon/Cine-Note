from flask import Flask, render_template
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)


# Connexion MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['movies_db']
movies_collection = db['movies']

@app.route('/')
def home():
    movies = list(movies_collection.find())
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)

# MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ma_base']
collection = db['items']

# Films pour carrousel
films_carrousel = [
    {"title": "Film 1", "image": "https://picsum.photos/800/400?random=1"},
    {"title": "Film 2", "image": "https://picsum.photos/800/400?random=2"},
    {"title": "Film 3", "image": "https://picsum.photos/800/400?random=3"},
    {"title": "Film 4", "image": "https://picsum.photos/800/400?random=4"},
]

# Films récents et à venir
films_recents = [
    {"title": "Film Récent 1", "image": "https://picsum.photos/200/300?random=5"},
    {"title": "Film Récent 2", "image": "https://picsum.photos/200/300?random=6"},
    {"title": "Film Récent 3", "image": "https://picsum.photos/200/300?random=7"},
]

films_avenir = [
    {"title": "Film A Venir 1", "image": "https://picsum.photos/200/300?random=8"},
    {"title": "Film A Venir 2", "image": "https://picsum.photos/200/300?random=9"},
    {"title": "Film A Venir 3", "image": "https://picsum.photos/200/300?random=10"},
]

# Films à découvrir
films_a_decouvrir = [
    {"title": "Film Découvrir 1", "image": "https://picsum.photos/150/220?random=11"},
    {"title": "Film Découvrir 2", "image": "https://picsum.photos/150/220?random=12"},
    {"title": "Film Découvrir 3", "image": "https://picsum.photos/150/220?random=13"},
    {"title": "Film Découvrir 4", "image": "https://picsum.photos/150/220?random=14"},
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
    app.run(debug=True)

