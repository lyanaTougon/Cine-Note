from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
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
    {"id": "avatar3", "title": "Avatar 3", "url": "/films/avatar3", "image": "avatar3.jpeg",
     "description": "Jake Sully et Neytiri affrontent une nouvelle menace sur Pandora dans un monde encore plus spectaculaire.",
     "color1": "#000428", "color2": "#1A0033", "note": 9},
     
    {"id": "wicked-1", "title": "Wicked 1", "url": "/films/wicked-1", "image": "wicked1.jpg",
     "description": "Une aventure magique dans un monde enchanteur.",
     "color1": "#FF69B4", "color2": "#008000", "note": 9.0},
    {"id": "ballerina", "title": "Ballerina", "url": "/films/ballerina", "image": "ballerina.webp",
     "description": "Une tueuse redoutable formée dans l’ombre cherche à se venger dans un monde impitoyable.",
     "color1": "#9370DB", "color2": "#1A0033", "note": 8.2}
]

films_recents = [
    {"id": "zootopie2", "title": "Zootopie 2", "url": "/films/zootopie2", "image": "zootopie2_couv.jpg", "note": 8.8},
]

films_avenir = [
    {"id": "parasite", "title": "Parasite", "url": "/films/parasite", "image": "parasite_couv.webp", "note": 8.7},
]

films_a_decouvrir = [
    {"id": "chainsawman", "title": "Chainsawman", "url": "/films/chainsawman", "image": "chainsawman_couv.jpg",
     "genres": ["Action","Drame"], "note": 8.0},
     {
  "id": "robot_sauvage",
  "title": "Robot Sauvage",
  "url": "/films/robot-sauvage",
  "image": "robotsauvage_couv.jpg",
  "genres": ["Action", "Aventure"],
  "note": 8.3
},
    
    {"id": "tenet", "title": "Tenet", "url": "/films/tenet", "image": "tenet_couv.webp",
     "genres": ["Action","Drame"], "note": 7.9},
    {"id": "parasite2", "title": "Parasite", "url": "/films/parasite", "image": "parasite_couv.webp",
     "genres": ["Action","Drame"], "note": 8.7}
]
# -------------------- FILMS UNIQUE --------------------
films_details = [

    {
    "id": "spiderverse",
    "title": "Spider-Verse",
    "image couv": "spiderverse_couv.jpg",
    "image": "spiderverse.jpg",
    "genres": ["Action", "Aventure"],
    "description": "Miles Morales traverse différentes dimensions...",
    "synopsis": "Miles Morales traverse différentes dimensions et rencontre de multiples versions de Spider-Man, tout en affrontant une nouvelle menace qui pourrait bouleverser tous les univers.",
    "date": "2023",
    "duree": "2h 20m",
    "trailer": "https://youtu.be/cqGjhVJWtEg?si=nsgkGx8yo6X4BBQf"
},
    {
        "id": "chainsawman",
        "title": "Chainsawman",
        "image": "chainsawman.webp",
        "image couv": "chainsawman_couv.jpg",
        "genres": ["Action", "Drame"],
        "description": "Un jeune homme transformé en chasseur de démons.",
        "synopsis": "Dans un monde où les démons rôdent, un jeune homme doit combattre pour survivre.",
        "date": "2025",
        "duree": "2h10",
        "trailer": "https://youtu.be/d1n552v1ng0?si=7-K8r-QQeegbpWS4"
    },
    {
        "id": "wicked1",
        "title": "Wicked 1",
        "image": "wicked1.jpg",
        "image couv": "wicked1_couv.jpg",
        "genres": ["Fantastique"],
        "description": "Une aventure magique.",
        "synopsis": "L’histoire des sorcières d’Oz avant Dorothy.",
        "date": "2024",
        "duree": "2h30",
        "trailer": "https://youtu.be/6COmYeLsz4c?si=t4I5_-BD5fbsxb6r"
        
    },
    {
  "id": "avatar3",
  "title": "Avatar 3",
  "image": "avatar3.jpeg",
  "image couv": "avatar3_couv.jpg",
  "genres": ["SF", "Aventure"],
  "description": "Sur Pandora, Jake Sully et sa famille affrontent de nouvelles menaces et découvrent une tribu hostile.",
  "synopsis": "Dans ce troisième volet de la franchise, Jake Sully, Neytiri et leur famille doivent faire face à l’alliance agressive d’une tribu Na’vi des Cendres tout en protégeant Pandora contre les forces humaines qui menacent leur monde.",
  "date": "2025",
  "duree": "3h 17m",
  "trailer": "https://youtu.be/ouVuXBtxk9M?si=H2I7SZUEWFISb4WD"
},
{
  "id": "robot_sauvage",
  "title": "Robot sauvage",
  "image": "robotsauvage.avif",
  "image couv": "robotsauvage_couv.jpg",
  "genres": ["Animation", "Aventure"],
  "description": "Un robot échoué sur une île déserte apprend à survivre et se lie d’amitié avec la faune locale.",
  "synopsis": "Après un naufrage, Roz, un robot utilitaire, se retrouve seule sur une île inhabitée. Elle doit apprendre à s’adapter à son nouvel environnement hostile et finit par se lier d’amitié avec les animaux, notamment en adoptant un oison orphelin qu’elle nomme Joli‑Bec.",
  "date": "2024",
  "duree": "1h 42m",
  "trailer": "https://youtu.be/Gn8QkmTtaTU?si=WF3zqEDpbK1yvJED"
},
{
  "id": "tenet",
  "title": "Tenet",
  "image": "tenet.jpg",
  "image couv": "tenet_couv.webp",
  "genres": ["Action", "SF"],
  "description": "Un agent doit empêcher une guerre mondiale liée à une technologie qui inverse le temps.",
  "synopsis": "Un protagoniste sans nom est recruté par une organisation mystérieuse appelée Tenet pour lutter contre une menace qui dépasse le cadre du temps traditionnel en utilisant la « inversion temporelle » afin d’arrêter une catastrophe mondiale imminente.",
  "date": "2020",
  "duree": "2h 30m",
  "trailer": "https://youtu.be/NQ5p6WYYK-s?si=7MZf6AQVmquJVOnK"
},
    {
        "id": "ballerina",
        "title": "Ballerina",
        "image": "ballerina.webp",
        "image couv": "ballerina_couv.jpg",
        "genres": ["Action", "Thriller"],
        "description": "Une tueuse cherche vengeance.",
        "synopsis": "Une assassine traque ceux qui ont détruit sa vie.",
        "date": "2025",
        "duree": "1h50",
        "trailer": "hhttps://youtu.be/0FSwsrFpkbw?si=3Bmx4M3rqwfTo_y9"
    },
{
  "id": "parasite",
  "title": "Parasite",
  "image": "parasite.jpeg",
    "image couv": "parasite_couv.webp",
  "genres": ["Thriller", "Comédie noire"],
  "description": "Une famille pauvre s’infiltre dans la vie d’une famille riche en se faisant passer pour des professionnels.",
  "synopsis": "Ki‑taek, sa femme et leurs enfants vivent dans un sous‑sol humide. Quand leur fils Ki‑woo est engagé pour donner des cours particuliers chez une famille riche, ils élaborent progressivement un stratagème afin que tous puissent se faire embaucher et profiter du luxe de leurs employeurs, jusqu’à ce que leur plan dérape.",
  "date": "2019",
  "duree": "2h 12m",
  "trailer": "https://youtu.be/isOGD_7hNIY?si=qT4yqZe4WEbXQQGw"
}   
    
]
for film in films_details:
    if not films_collection.find_one({"id": film["id"]}):
        films_collection.insert_one(film)

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
    all_films = films_details
    featured_film = all_films[0]  # Le premier film de la liste
    all_genres = sorted({g for f in films_details for g in f.get("genres", [])})
    return render_template('films.html', films=all_films, featured_film=featured_film, all_genres=all_genres)

@app.route('/se_connecter', methods=['GET','POST'])
def se_connecter():
    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()

        user = users_collection.find_one({
            "email": email,
            "password": hashed
        })

        if user:
            session['user'] = email
            session['role'] = user.get("role", "user")

            # 🔥 ADMIN → dashboard
            if session['role'] == 'admin':
                return redirect(url_for('admin_page'))

            # 👤 USER NORMAL
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

# -------------------- AFFICHER LA PAGE DES NOTES --------------------
@app.route('/note')
def note():
    if 'user' not in session:
        return redirect(url_for('se_connecter'))

    # Récupère toutes les notes de l'utilisateur
    comments = list(comments_collection.find({"user": session['user']}))
    
    # Récupère les films correspondants aux notes
    top5 = []
    for c in comments:
        film = next((f for f in films_details if f["id"] == c["film"]), None)
        if film:
            top5.append(film)

    return render_template('note.html', top5=top5, comments=comments)


@app.route('/delete_note/<film_id>', methods=['POST'])
def delete_note(film_id):
    if 'user' not in session:
        return redirect(url_for('se_connecter'))
    
    comments_collection.delete_one({
        "user": session['user'],
        "film": film_id
    })
    
    flash("La note a été annulée. 🎬", "success")
    return redirect(url_for('note'))


# -------------------- FILM DETAIL --------------------
@app.route('/films/<film_id>')
def film_detail(film_id):
    film = next((f for f in films_details if f["id"] == film_id), None)
    if not film:
        return "Film introuvable", 404

    is_favori = False
    if 'user' in session:
        user = users_collection.find_one({"email": session['user']})
        is_favori = any(f["id"] == film_id for f in user.get("favoris", []))

    return render_template("film_detail.html", film=film, is_favori=is_favori)


# -------------------- FAVORIS --------------------
@app.route('/toggle_favori/<film_id>')
def toggle_favori(film_id):
    if 'user' not in session:
        return redirect(url_for('se_connecter'))

    user = users_collection.find_one({"email": session['user']})
    film = next((f for f in films_details if f["id"] == film_id), None)
    if not film:
        return redirect(url_for('films_page'))

    favoris = user.get("favoris", [])

    if any(f["id"] == film_id for f in favoris):
        # Retirer des favoris
        users_collection.update_one(
            {"email": session['user']},
            {"$pull": {"favoris": {"id": film_id}}}
        )
    else:
        # Ajouter aux favoris
        users_collection.update_one(
            {"email": session['user']},
            {"$addToSet": {"favoris": film}}
        )

    return redirect(request.referrer or url_for('films_page'))


# -------------------- NOTER --------------------
@app.route('/noter/<film_name>', methods=['POST'])
def noter(film_name):
    if 'user' not in session:
        return redirect(url_for('se_connecter'))

    note = int(request.form.get('note'))

    comments_collection.insert_one({
        "film": film_name,
        "user": session['user'],
        "note": note
    })

    return redirect(request.referrer)


# -------------------- ADMIN FILMS --------------------
@app.route('/admin')
def admin_page():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    all_users = list(users_collection.find())
    all_films = list(films_collection.find())  # <- MongoDB
    return render_template('admin/admin.html', users=all_users, films=all_films)


@app.route('/admin/films/ajouter', methods=['GET','POST'])
def add_film():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        films_collection.insert_one({"title": title})
        return redirect(url_for('admin_page'))
    return render_template('admin/add_film.html')


@app.route('/admin/films/<film_id>/modifier', methods=['GET','POST'])
def edit_film(film_id):
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    film = films_collection.find_one({"_id": ObjectId(film_id)})
    if request.method == 'POST':
        new_title = request.form['title']
        films_collection.update_one({"_id": ObjectId(film_id)}, {"$set": {"title": new_title}})
        return redirect(url_for('admin_page'))
    return render_template('admin/edit_film.html', film=film)


@app.route('/admin/films/<film_id>/supprimer')
def delete_film(film_id):
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    films_collection.delete_one({"_id": ObjectId(film_id)})
    return redirect(url_for('admin_page'))

# -------------------- ADMIN USERS --------------------
@app.route('/admin/users/<user_id>/make_admin')
def make_admin(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": "admin"}}
    )

    return redirect(url_for('admin_page'))

@app.route('/admin/users/<user_id>/delete')
def delete_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    users_collection.delete_one({"_id": ObjectId(user_id)})
    return redirect(url_for('admin_page'))


# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)