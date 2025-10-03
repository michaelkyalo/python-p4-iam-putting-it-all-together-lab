# app.py
from flask import Flask, request, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'something-secret'

db.init_app(app)

# ---------------- Signup ----------------
@app.post('/signup')
def signup():
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return make_response({"error": "Invalid signup"}, 422)

    user = User(
        username=data["username"],
        bio=data.get("bio"),
        image_url=data.get("image_url"),
    )
    user.password_hash = data["password"]

    db.session.add(user)
    db.session.commit()
    session["user_id"] = user.id

    return make_response(user.to_dict(), 201)


# ---------------- Login ----------------
@app.post('/login')
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if user and user.authenticate(data.get("password")):
        session["user_id"] = user.id
        return make_response(user.to_dict(), 200)

    return make_response({"error": "Unauthorized"}, 401)


# ---------------- Check Session ----------------
@app.get('/check_session')
def check_session():
    user_id = session.get("user_id")
    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    user = User.query.get(user_id)
    return make_response(user.to_dict(), 200)


# ---------------- Logout ----------------
@app.delete('/logout')
def logout():
    if not session.get("user_id"):
        return make_response({"error": "Unauthorized"}, 401)

    session["user_id"] = None
    return make_response({}, 204)


# ---------------- Recipes ----------------
@app.get('/recipes')
def get_recipes():
    user_id = session.get("user_id")
    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    user = User.query.get(user_id)
    return make_response([r.to_dict() for r in user.recipes], 200)


@app.post('/recipes')
def create_recipe():
    user_id = session.get("user_id")
    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    data = request.get_json()

    if not data.get("instructions") or len(data["instructions"]) < 50:
        return make_response({"error": "Invalid recipe"}, 422)

    recipe = Recipe(
        title=data.get("title"),
        instructions=data.get("instructions"),
        minutes_to_complete=data.get("minutes_to_complete"),
        user_id=user_id
    )
    db.session.add(recipe)
    db.session.commit()

    return make_response(recipe.to_dict(), 201)
