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

@app.route('/trails')
def trails_list():
    """View trail list."""
    
    all_trails = crud.get_all_trails()

    return render_template('trails.html',
                            all_trails=all_trails)

@app.route('/trails/<trail_id>')
def trail_detail(trail_id):
    """Show individual movie details."""

    trail_details = crud.get_trail_by_id(trail_id)

    return render_template('trail_details.html',
                            trail=trail_details)

@app.route('/find-a-hike-form')
def display_hike_form():
    """View hike form."""
    
    return render_template('find-a-hike-form.html')



@app.route('/show-form')
def show_madlib():
    """Show user their form filled out."""

    route_type = request.args.get("route_type")   
    park = request.args.get("park")   
    state = request.args.get("state")
    difficulty = request.args.get("difficulty")

    server_trail = crud.query_trail(route_type, park, state, difficulty).all()

    if server_trail == []:
        server_trail='Sorry, no hikes matched your specifications, please try again with less parameters.'
    


    return render_template("show-form.html",
                           route_type=route_type,
                           park=park,
                           state=state,
                           difficulty=difficulty,
                           server_trail=server_trail)
                            #trail.all() is a list of sqlAlchemy objects

@app.route('/hikes.json')
def hike():
    """Return a trail for this trail_type."""

    trail_type = request.args.get('trail_type')
    trail_type_info = WEATHER.get(trail_type, DEFAULT_WEATHER)
    return jsonify(trail_type_info)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port=5000)