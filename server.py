"""Server for National Park trail app."""

from flask import (Flask, render_template, request, flash, session, redirect)
import flask_login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from model import connect_to_db
import model
import os
import image_helper

import json 

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev" #TODO replace with secrets.sh key
app.jinja_env.undefined = StrictUndefined

# API_KEY = os.environ['WEATHERMAP_KEY']
UPLOAD_FOLDER_PROFILE_PICTURE = "./static/img/profile_pictures/"

#Flask login routes

####
# Flask Login configurations
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Reload the user object from the user ID stored in session."""

    return model.User.query.get(int(user_id))

@app.route('/login')
def show_login():
    """Display login page."""

    if current_user.is_authenticated:
        return redirect('homepage.html')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Log user into account."""

    user = crud.get_user_by_username(request.form['username'])
    password = request.form['password']

    if user == None:
        flash("We could not find an account with that username, please try again or create an account.")
        return redirect('/')
#why does this flash on homepage and not login page?
    elif password != user.password:
        flash('Incorrect password. Please try again.')
        return redirect('login.html')

    else:
        flash(f'Logged in as {user.user_fname}!')
        login_user(user)
        return render_template('homepage.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    flash('Logged out')
    return render_template('homepage.html')

####

# HOME
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

# 404 handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# USER ACCOUNT ROUTES
@app.route('/new_user', methods=['POST'])
def create_new_user():
    """Create a new user."""

    user_fname = request.form.get('user_fname')
    user_lname = request.form.get('user_lname')
    user_email = request.form.get('email')
    user_name = request.form.get('username')
    user_password = request.form.get('password')
    profile_picture = request.form.get('profile_picture')

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
def view_user_profile():
    """View user profile."""

    if not current_user.is_authenticated:
        flash('Please log in to view your account.')
        return redirect('/login')

    user_id = current_user.user_id
    user_object = crud.get_user_by_id(user_id)
    user_friends = crud.get_user_friends(user_id) #object returned is a list, so we index into that list using [0] and then the info stored there is useful and accessbile for user_profile.html
    user_wishlist = crud.get_user_wishes(user_id) #if want return whole list, dont use [0]
    user_hike_log = crud.get_user_hike_log(user_id)
    user_ratings = crud.get_user_ratings(user_id)[0]
    user_goals = crud.get_goals_by_user_id(user_id)

    friends_info =[]
    for friend in user_friends:
        friend = crud.get_friend_user_object(user_friends[0].friend_user_id)
        friends_info.append(friend)

    wish_list_trail_info = []
    for trail in user_wishlist:
        trail = crud.get_wish_trail_object(user_wishlist[0].trail_id)
        wish_list_trail_info.append(trail)

    log_hike_info = []
    for hike in user_hike_log:
        hike = crud.get_log_trail_object(user_hike_log[0].hike_id)
        log_hike_info.append(hike)

    return render_template('user_profile.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals,
                            user_friends=user_friends,
                            user_wishlist=user_wishlist,
                            user_hike_log=user_hike_log,
                            user_ratings=user_ratings,
                            friends_info=friends_info,
                            wish_list_trail_info=wish_list_trail_info,
                            log_hike_info=log_hike_info)

@app.route('/users')
def users_list():
    """View users list."""
    
    all_users = crud.get_all_users()

    return render_template('users.html',
                            all_users=all_users)

@app.route('/users/<user_id>')
def view_user_profiles(user_id):
    """View other user's profiles."""

    # user_id = current_user.user_id #click on user, get user id
    user_object = crud.get_user_by_id(user_id)
    user_goals = crud.get_goals_by_user_id(user_id)
    user_wishlist = crud.get_user_wishes(user_id)

    wish_list_trail_info = []
    for trail in user_wishlist:
        trail = crud.get_wish_trail_object(user_wishlist[0].trail_id)
        wish_list_trail_info.append(trail)

    return render_template('view_users.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals,
                            wish_list_trail_info=wish_list_trail_info,
                            user_wishlist=user_wishlist)
######################################################################################                           

@app.route("/profile_edit")
def show_edit_profile_page():
    """Display to user the Edit Profile Page."""

    if not current_user.is_authenticated:
        return redirect('/login')
    
    user_id = current_user.user_id
    user_object = crud.get_user_by_id(user_id)
    user_goals = crud.get_goals_by_user_id(user_id)

    return render_template('profile_edit.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals)

@app.route('/profile_edit', methods = ["POST"])
def edit_user_profile():
    """Edit user profile with user form responses."""

    if not current_user.is_authenticated:
        return redirect('/')

    user_id = current_user.user_id
    user_object = crud.get_user_by_id(user_id)
   
    form_id = request.form.get("form_id")

    #basic form
    if form_id == "basic_profile_information":
        user_fname = request.form.get("first_name")
        user_lname = request.form.get("last_name")
        email = request.form.get("email")
        crud.update_user_profile_info(user_id, user_fname, user_lname, email)

        return redirect("profile_edit")

    if form_id == "hiking_goals":

        goal_miles = request.form.get('goal_miles')
        goal_number_hikes = request.form.get('goal_number_hikes')
        goal_hike_difficulty = request.form.get('goal_hike_difficulty')

        crud.update_user_hiking_goals(user_id, goal_miles, goal_number_hikes, goal_hike_difficulty)

        return redirect("profile_edit")

    #profile pic
    elif form_id == "profile_picture":
        if "file1" not in request.files:
            flash("We couldn't find your profile picture!")
            return redirect("/user_profile")

        f = request.files["file1"]

        result = image_helper.resize_image_square_crop(f.stream, (400, 400))
        (success, msg, resized_image) = result
        if success is False:
            flash(msg)
            return redirect("/profile_edit")
        else:
            file_name = str(user_id) + ".jpg"
            path = os.path.join(UPLOAD_FOLDER_PROFILE_PICTURE, file_name)
            resized_image.save(path)

            crud.set_user_profile_picture(user_id, file_name) 
        
        return redirect("/profile_edit")

    #password
    # Known bug: if more than one user has the same password (ie. 'test') then all users passwords will be updated (ie. updated to 'Test!')..
    elif form_id == "password_change":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")

        if (crud.update_password(user_id, old_password, new_password) is False): 
            flash("Old password is incorrect")
        else:
            flash("Password Updated")
        return redirect("/profile_edit")

    else:
        flash("Unhandled form submission")
        return redirect("/profile_edit")

    return render_template('profile_edit.html',
                            user_id=user_id,
                            user_object=user_object)

# RATING ROUTES
@app.route('/new_rating', methods=['POST'])
def create_new_rating():
    """Create a new rating."""
    #trail id from whichever hike the user selected
    # hike = crud.create_hike()

    score = request.form.get('score')
    challenge_rating = request.form.get('challenge_rating')
    distance_rating = request.form.get('distance_rating')
    ascent_rating = request.form.get('ascent_rating')
    descent_rating = request.form.get('descent_rating')
    user_comment = request.form.get('comment')

    crud.create_rating(score, hike.hike_id, distance_rating, ascent_rating, descent_rating, user_comment)

    # return redirect('/')

# TRAIL LIST ROUTES
@app.route('/trails')
def trails_list():
    """View trail list."""
    
    all_trails = crud.get_all_trails()

    return render_template('trails.html',
                            all_trails=all_trails)

@app.route('/trails/<trail_id>')
def trail_detail(trail_id):
    """Show individual trail details."""

    trail_details = crud.get_trail_by_id(trail_id)
    ratings = crud.get_all_ratings()
    # for rating in ratings:
    #     total_score = sum(score)
    #     av_total_score = total_score / num_scores
    # for rating in ratings:
        #total_score = score + score ...
        #av_total_score = total_score / num_scores

    # make api call here to get json from Weather Map API
    # give json info to template as variable
    trail_object = crud.get_trail_by_id(trail_id)

    geo = json.loads(trail_object._geoloc.replace("\'", "\""))

    latitude = geo["lat"]
    longitude = geo["lng"]

    return render_template('trail_details.html',
                            trail_details=trail_details,
                            ratings=ratings,
                            latitude=latitude,
                            longitude=longitude
                            #av_total_score=av_total_score
                            )

# PARK LIST ROUTES
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

    park_trails = crud.get_parks_trails_by_name(area_name)

    return render_template('park_details.html',
                            park_trails=park_trails,
                            area_name=area_name)

#STATE LIST ROUTES
@app.route('/states')
def states_list():
    """View states list."""
    
    all_states = crud.get_all_states()

    return render_template('states.html',
                            all_states=all_states)

@app.route('/states/<state_name>')
def state_detail(state_name):
    """Show individual state details."""

    state_parks_details = crud.get_park_states_by_name(state_name)

    return render_template('state_details.html',
                            # trail=trail_details,
                            state_parks_details=state_parks_details,
                            state_name=state_name)

# FIND HIKE ROUTES
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


 
if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port=5001)