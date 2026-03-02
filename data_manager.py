from models import db, User, Movie


class DataManager():
    """Handles CRUD operations for Users and Movies."""


def create_user(self, name):
    """Create a new user."""
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()


def get_users(self):
    """Return all users."""
    return User.query.all()


def get_movies(self, user_id):
    """Return all movies belonging to a specific user."""
    return Movie.query.filter_by(user_id=user_id).all()


def add_movie(self, movie):
    """Add a new movie for a specific user."""
    db.session.add(movie)
    db.session.commit()


def update_movie(self, movie_id, new_title):
    """Update a movie's title by id."""
    movie_to_update = Movie.query.get(movie_id)

    if movie_to_update:
        movie_to_update.name = new_title
        db.session.commit()


def delete_movie(self, movie_id):
    """Delete a movie by ID."""
    movie = Movie.query.get(movie_id)

    if movie:
        db.session.delete(movie)
        db.session.commit()
