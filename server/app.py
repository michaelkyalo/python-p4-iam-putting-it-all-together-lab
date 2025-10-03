from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api

# initialize extensions (not bound to app yet)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # set up API
    api = Api(app)

    # import models so Alembic can detect them
    from models import User, Recipe  

    # register resources here if needed
    # from resources import UserResource, RecipeResource
    # api.add_resource(UserResource, '/users')
    # api.add_resource(RecipeResource, '/recipes')

    return app

# expose app for flask CLI
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5555)
