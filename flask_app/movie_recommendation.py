from flask import Flask, render_template, redirect, url_for, current_app
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask import g
import pandas as pd

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

def get_db():
    if 'db' not in g:
        g.db = pd.read_csv('output1.csv', index_col=0)
        g.db_ratings = pd.read_csv('output_rating1.csv', index_col=0)
        print("Datastore loaded successfully.")
    return g.db, g.db_ratings

Bootstrap(app)

class NameForm(FlaskForm):
    name = IntegerField('Enter user-id', validators=[DataRequired(), NumberRange(min=0, max=6040, message="User-id should be between 0 and 6040 (inclusive)")])
    submit = SubmitField('Get Recommendations')

@app.route('/', methods=['GET', 'POST'])
def index():
    db, db_ratings = get_db()
    print(db)
    form = NameForm()
    message = ""
    movies = None
    name = form.name.data
    movie_ratings = {}
    if form.validate_on_submit():
        message = db.iloc[name].values.tolist()
        movie_rating = db_ratings.iloc[name].values.tolist()
        for i in range(0, len(message)):
            movie_ratings[message[i]] = round(movie_rating[i],1)
    form.name = ""
    return render_template('index.html', names=name, form=form, message=movie_ratings)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
