"""Server for National Park trail app."""

from flask import (Flask, render_template, request, flash, session, redirect)
import flask_login
from flask_login import current_user

from model import connect_to_db
import model

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev" #TODO replace with secrets.sh key
app.jinja_env.undefined = StrictUndefined

####
# lets my app and flask-login work togther
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

@app.route('/login')
def show_login():
    """Display login page."""

    if current_user.is_authenticated:
        return redirect('/homepage')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Log user into account."""
# cant get user by username, only user id just like trail id vs trail state name?
    user = crud.get_user_by_username(request.form['username'])
    password = request.form['password']

    if user == None:
        flash("We could not find an account with that username, please try again or create an account.")
        return redirect('/')

    elif password != user.password:
        flash('Incorrect password. Please try again.')
        return redirect('/login')

    else:
        flash(f'Logged in as {user.user_fname}!')
        lofin_user(user)
        return redirect('/homepage')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

####


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/new_user', methods=['POST'])
def create_new_user():
    """Create a new user."""

    user_fname = request.form.get('user_fname')
    user_lname = request.form.get('user_lname')
    user_email = request.form.get('email')
    user_name = request.form.get('username')
    user_password = request.form.get('password')

    user_existence = crud.get_user_by_email(user_email)
    
    if user_existence:
        flash('You can\'t create an account with that email. Try again.')
    else:
        crud.create_user(user_name, user_email, user_password)
        flash('Your account was successfully created. WelCoMe tO thE ComMunItYYY, you can now log in!')

    return redirect('/')

@app.route('/create-account')
def display_create_account_form():
    """View create account form."""
    
    return render_template('create-account.html')

@app.route('/user_profile')
def view_user_profile(user_id):
    """View user profile."""

    user = crud.get_user_by_id(user_id)
    # need to return user info to be used in user_profile
    # when you click on 'My Profile,' does user-id come from session?

    return render_template('user_profile.html',
                            user=user)

@app.route('/new_rating', methods=['POST'])
def create_new_rating():
    """Create a new rating."""

    score = request.form.get('score')
    challenge_rating = request.form.get('challenge_rating')
    distance_rating = request.form.get('distance_rating')
    ascent_rating = request.form.get('ascent_rating')
    descent_rating = request.form.get('descent_rating')
    comment = request.form.get('comment')

    crud.create_rating(score, challenge_rating, distance_rating, ascent_rating, descent_rating, comment)

    return redirect('/')

@app.route('/trails')
def trails_list():
    """View trail list."""
    
    all_trails = crud.get_all_trails()

    return render_template('trails.html',
                            all_trails=all_trails)

@app.route('/parks')
def parks_list():
    """View National Park list."""
    
    all_trails = crud.get_all_trails()
    all_parks = crud.get_all_parks()

    return render_template('parks.html',
                            all_parks=all_parks,
                            all_trails=all_trails)

@app.route('/parks/<area_name>')
def park_detail(area_name):
    """Show individual park details."""

    park_trails = crud.get_parks_trails_by_name()
    # trail_details = crud.get_trail_by_id(trail_id)

    return render_template('park_details.html',
                            # trail=trail_details,
                            park_trails=park_trails,
                            area_name=area_name)

@app.route('/trails/<trail_id>')
def trail_detail(trail_id):
    """Show individual trail details."""

    trail_details = crud.get_trail_by_id(trail_id)
    ratings = crud.get_all_ratings()
    print(ratings)

    return render_template('trail_details.html',
                            trail=trail_details,
                            ratings=ratings)

@app.route('/find-a-hike-form')
def display_hike_form():
    """View hike form."""
    
    return render_template('find-a-hike-form.html')



@app.route('/show-form')
def show_form_response():
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

# @app.route('/hikes.json')
# def hike():
#     """Return a trail for this trail_type."""

#     trail_type = request.args.get('trail_type')
#     trail_type_info = WEATHER.get(trail_type, DEFAULT_WEATHER)
#     return jsonify(trail_type_info)
 

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port=5001)