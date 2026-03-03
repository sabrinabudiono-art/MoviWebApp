from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Represents a user who owns movies."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    """Represents a movie belonging to a user."""
    # Define all the Movie properties
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(255), nullable=False)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
