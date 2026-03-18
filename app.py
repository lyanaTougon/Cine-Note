from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
app.secret_key = "ton_secret_key"

# -------------------- BASE DE DONNÉES --------------------
client = MongoClient('mongodb://localhost:27017/')
db = client['cine_note']
films_collection = db['films']
users_collection = db['users']
comments_collection = db['comments']

# -------------------- FILMS INIT --------------------
films_carrousel = [
    {"title": "Avatar 3", "url": "/films/avatar3", "image": "avatar3.jpeg",
     "description": "Jake Sully et Neytiri affrontent une nouvelle menace sur Pandora dans un monde encore plus spectaculaire.",
     "color1": "#000428", "color2": "#1A0033", "note": 9},
  {
  "title": "Wicked 1",
  "url": "/films/wicked-1",
  "image": "wicked1.jpg",
  "description": "Une aventure magique dans un monde enchanteur.",
  "color1": "#FF69B4",  
  "color2": "#008000", 
  "note": 9.0,
},
    {"title": "Ballerina", "url": "/films/ballerina", "image": "ballerina.webp",
     "description": "Une tueuse redoutable formée dans l’ombre cherche à se venger dans un monde impitoyable.",
     "color1": "#9370DB", "color2": "#1A0033", "note": 8.2}
]

films_recents = [
    {"title": "Zootopie 2", "url": "/films/zootopie2", "image": "zootopie2_couv.jpg", "note": 8.8},
]

films_avenir = [
    {"title": "Parasite", "url": "/films/parasite", "image": "parasite_couv.webp", "note": 8.7},
]

films_a_decouvrir = [
    {"title": "Chainsawman", "url": "/films/chainsawman", "image": "chainsawman_couv.jpg", "genres": ["Action","Drame"], "note": 8.0},
    {"title": "Spider-Verse", "url": "/films/spiderverse", "image": "spiderverse_couv.jpg", "genres": ["Action","Aventure"], "note": 8.3},
    {"title": "Tenet", "url": "/films/tenet", "image": "tenet_couv.webp", "genres": ["Action","Drame"], "note": 7.9},
    {"title": "Parasite", "url": "/films/parasite", "image": "parasite_couv.webp", "genres": ["Action","Drame"], "note": 8.7}
]

# -------------------- ADMIN FIXE --------------------
hashed_admin = hashlib.sha256("1234".encode()).hexdigest()
users_collection.update_one(
    {"email": "admin1@exemple.com"},
    {"$set": {"password": hashed_admin, "role": "admin"}},
    upsert=True
)

# -------------------- ROUTES --------------------
@app.route('/', methods=['GET','POST'])
def index():
    query = request.form.get('search','') if request.method=='POST' else ''
    results = list(films_collection.find({"title":{"$regex": query, "$options":"i"}})) if query else []
    return render_template('index.html',
                           query=query, results=results,
                           films_carrousel=films_carrousel,
                           films_recents=films_recents,
                           films_avenir=films_avenir,
                           films_a_decouvrir=films_a_decouvrir)

@app.route('/films')
def films_page():
    all_films = films_carrousel + films_recents + films_avenir + films_a_decouvrir
    return render_template('films.html', films=all_films)

@app.route('/se_connecter', methods=['GET','POST'])
def se_connecter():
    error = None
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()
        user = users_collection.find_one({"email": email, "password": hashed})
        if user:
            session['user'] = email
            session['role'] = user.get("role","user")
            return redirect(url_for('index'))
        else:
            error = "Email ou mot de passe incorrect"
    return render_template('se_connecter.html', error=error)

@app.route('/creer_compte', methods=['GET','POST'])
def creer_compte():
    error = None
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        if users_collection.find_one({"email": email}):
            error = "Cet email existe déjà"
        else:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            users_collection.insert_one({"email": email, "password": hashed, "role":"user", "favoris":[]})
            session['user'] = email
            session['role'] = "user"
            return redirect(url_for('index'))
    return render_template('creer_compte.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/favoris')
def favoris():
    if 'user' not in session:
        return redirect(url_for('se_connecter'))
    user = users_collection.find_one({"email": session['user']})
    favoris = user.get("favoris", [])
    return render_template('favoris.html', favoris=favoris)

@app.route('/note')
def note():
    top5 = sorted(films_carrousel + films_recents + films_avenir + films_a_decouvrir, key=lambda x:x.get("note",0), reverse=True)[:5]
    comments = list(comments_collection.find())
    return render_template('note.html', top5=top5, comments=comments)

@app.route('/admin')
def admin_page():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    all_users = list(users_collection.find())
    all_films = films_carrousel + films_recents + films_avenir + films_a_decouvrir
    return render_template('admin.html', users=all_users, films=all_films)

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)