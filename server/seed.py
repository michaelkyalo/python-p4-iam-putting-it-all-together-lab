from app import create_app, db
from models import User, Recipe

# create the app instance using the factory
app = create_app()

with app.app_context():
    # If you really want a clean slate, uncomment these:
    # db.drop_all()
    # db.create_all()

    # Create a user
    u1 = User(
        username="mike",
        image_url="https://i.pravatar.cc/150?img=3",
        bio="I love cooking"
    )
    u1.password_hash = "password123"  # will trigger your model's setter

    # Create a recipe
    r1 = Recipe(
        title="Spaghetti",
        instructions="Boil pasta, cook sauce, and mix together. Serve hot with cheese." * 3,
        minutes_to_complete=30,
        user=u1
    )

    # Add and commit
    db.session.add_all([u1, r1])
    db.session.commit()
    print("✅ DB seeded!")
