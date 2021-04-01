"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev" #TODO replace with secrets.sh key
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/new_user', methods=['POST'])
def create_new_user():
    """Create a new user."""

    user_name = request.form.get('username')
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    user_existence = crud.get_user_by_email(user_email)
    
    if user_existence:
        flash('You can\'t create an account with that email. Try again.')
    else:
        crud.create_user(user_name, user_email, user_password)
        flash('Your account was successfully created. WelCoMe tO thE ComMunItYYY, you can now log in!')

    return redirect('/')

@app.route('/find-a-hike-form')
def display_hike_form():
    """View hike form."""
    
    

    return render_template('find-a-hike-form.html')

@app.route('/view-hikes')
def hike_list():
    """View hike form."""
    
    

    return render_template('view-hikes.html')

@app.route('/show-form')
def show_madlib():
    """Show user their form filled out."""

    trail_type = request.args.get("trail_type")   
    physical_rating = request.args.get("physical_rating")
    difficulty = request.args.get("difficulty")

    return render_template("show-form.html",
                           trail_type=trail_type,
                           physical_rating=physical_rating,
                           difficulty=difficulty,
                            )

@app.route('/hikes.json')
def hike():
    """Return a trail for this trail_type."""

    trail_type = request.args.get('trail_type')
    trail_type_info = WEATHER.get(trail_type, DEFAULT_WEATHER)
    return jsonify(trail_type_info)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port=5000)