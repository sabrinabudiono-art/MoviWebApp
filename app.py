import requests
from flask import Flask, request, redirect, url_for, render_template
from data_manager import DataManager
from models import db, Movie
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()  # Create an object of your DataManager class


@app.route('/')
def index():
    """Show a list of all registered users and a form for adding new users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    """Add a user to the list of users"""
    new_user_name = request.form.get('name')
    data_manager.create_user(new_user_name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """When user clicks on view movies, the app retrieves that user’s list of
    favorite movies and displays it."""
    list_of_movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=list_of_movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to user’s list of favorite movies and displays it.
    Uses omdb API to fetch the movie data."""
    movie_title = request.form.get("title")

    if not movie_title:
        return "Movie title is required", 400

    request_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}"

    try:
        response = requests.get(request_url)
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            return "Movie not found. Please try again.", 404

        new_movie = Movie(
            name=movie_data.get("Title"),
            director=movie_data.get("Director"),
            year=int(movie_data.get("Year")),
            poster_url=movie_data.get("Poster"),
            user_id=user_id
        )

        data_manager.add_movie(new_movie)

        return redirect(url_for('list_movies', user_id=user_id))

    except Exception as e:
        return f"Error fetching movie data: {str(e)}", 500


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list, without depending on OMDb for corrections."""
    new_title = request.form.get('title')
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete(user_id, movie_id):
    """Delete a specific movie from a user’s favorite movie list."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Shows a page not found page when 404."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Shows an internal server error page when 500."""
    return render_template("500.html"), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
