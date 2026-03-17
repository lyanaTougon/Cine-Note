from flask import Flask, render_template
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