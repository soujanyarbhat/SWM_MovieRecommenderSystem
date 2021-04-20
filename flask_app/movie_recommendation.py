from flask import Flask, render_template, redirect, url_for, current_app
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask import g
import pandas as pd
import csv
import random

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

def get_db():
    if 'db' not in g:
        g.db = pd.read_csv('output1.csv', index_col=0)
        g.db_ratings = pd.read_csv('output_rating1.csv', index_col=0)
        g.db_rated = pd.read_csv('output_rated1.csv', index_col=0)
        g.db_ratings_rated = pd.read_csv('output_rating_rated1.csv', index_col=0)
        g.movies = pd.read_csv('movies.dat', sep = '::', header = None, engine = 'python', encoding = 'latin-1')
        g.movies.columns = ['movieid', 'movie', 'genre']
        print("Datastore loaded successfully")
    return g.db, g.db_ratings, g.db_rated, g.db_ratings_rated, g.movies

Bootstrap(app)

class NameForm(FlaskForm):
    name = IntegerField('Enter user-id', validators=[DataRequired(message="Invalid argument"), NumberRange(min=0, max=6040, message="User-id must be between 0 and 6040 (inclusive)")])
    submit = SubmitField('Get Recommendations')

@app.route('/', methods=['GET', 'POST'])
def index():
    db, db_ratings, db_rated, db_ratings_rated, db_movies = get_db()
    form = NameForm()
    name = form.name.data
    recommendations = []
    watched = []
    if form.validate_on_submit():
        movies = db.iloc[name].values.tolist()
        movie_rating = db_ratings.iloc[name].values.tolist()
        movies_rated = []
        movie_rating_rated = []
        if name in db_rated.index:
            movies_rated = db_rated.iloc[name].values.tolist()
            movie_rating_rated = db_ratings_rated.iloc[name].values.tolist()
        for i in range(0, len(movies)):
            recommendation = []
            recommendation.append(movies[i])
            recommendation.append(round(movie_rating[i],1))
            genre_string = db_movies[db_movies['movie'] == movies[i]]['genre'].values
            recommendation.append(genre_string)
            recommendations.append(recommendation)

        for i in range(0, len(movies_rated)):
            watch = []
            watch.append(movies_rated[i])
            watch.append(round(movie_rating_rated[i],1))
            genre_string = db_movies[db_movies['movie'] == movies_rated[i]]['genre'].values
            watch.append(genre_string)
            watched.append(watch)
    else:
        form.name = None
    return render_template('index.html', names=name, form=form, recommendations=recommendations, watched=watched)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
