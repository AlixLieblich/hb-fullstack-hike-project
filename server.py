"""Server for National Park trail app."""

from flask import (Flask, render_template, request, flash, session, redirect)
import flask_login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from model import db, connect_to_db, User, Trail, Goal, Rating, User_Friend, Hike, Wishlist
import model
import os
import image_helper
from sqlalchemy import and_

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
# TODO: bug here
    user = crud.get_user_by_username(request.form['username']) # this one is a little complicated, wanna keep it
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

    user_existence = crud.get_user_by_email(user_email) # somewhat complicated, wanna keep
    
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
    # user_object = crud.get_user_by_id(user_id)
    user_object = User.query.get(user_id)
    # user_friends = crud.get_user_friends(user_id) #object returned is a list, so we index into that list using [0] and then the info stored there is useful and accessbile for user_profile.html
    # user_friends = db.session.query(User_Friend).filter(User_Friend.user_id==user_id).all() #maybe
    user_friends = user_object.added_friends
    # user_wishlist = crud.get_user_wishes(user_id) #if want return whole list, dont use [0]
    # user_wishlist = Wishlist.query.get(user_id) #maybe
    user_wishlist = user_object.wishes
    # user_hike_log = crud.get_user_hike_log(user_id) 
    user_hike_log = user_object.hikes
    user_ratings = user_object.ratings
    # user_goals = crud.get_goals_by_user_id(user_id)
    # user_goals = user_object.goals # why doesnt this work but the following line does
    user_goals = Goal.query.filter(Goal.user_id == user_id).first()

    # friends_info =[]
    # for friend in user_friends:
    #     friend = crud.get_friend_user_object(user_friends[0].friend_user_id)
    #     friends_info.append(friend)

    # wish_list_trail_info = []
    # for trail in user_wishlist:
    #     trail = crud.get_wish_trail_object(user_wishlist[0].trail_id)
    #     wish_list_trail_info.append(trail)

    # log_hike_info = []
    # for hike in user_hike_log:
    #     hike = crud.get_log_trail_object(user_hike_log[0].hike_id)
    #     log_hike_info.append(hike)

    return render_template('user_profile.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals,
                            user_friends=user_friends,
                            user_wishlist=user_wishlist,
                            user_hike_log=user_hike_log,
                            user_ratings=user_ratings,
                            # friends_info=friends_info,
                            # wish_list_trail_info=wish_list_trail_info,
                            # log_hike_info=log_hike_info
                            )

@app.route('/users')
def users_list():
    """View users list."""
    
    all_users = db.session.query(User).all()

    return render_template('users.html',
                            all_users=all_users)

@app.route('/users/<user_id>')
def view_user_profiles(user_id):
    """View other user's profiles."""

    user_id = current_user.user_id #click on user, get user id
    # user_object = crud.get_user_by_id(user_id)
    user_object = User.query.filter(User.user_id == user_id).first()
    # user_goals = crud.get_goals_by_user_id(user_id)
    user_goals = Goal.query.filter(Goal.user_id == user_id).first()
    # user_wishlist = crud.get_user_wishes(user_id)
    user_wishlist = db.session.query(Wishlist).filter(Wishlist.user_id==user_id).all()

    # wish_list_trail_info = []
    # for trail in user_wishlist:
    #     trail = crud.get_wish_trail_object(user_wishlist[0].trail_id)
    #     wish_list_trail_info.append(trail)

    return render_template('view_users.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals,
                            # wish_list_trail_info=wish_list_trail_info,
                            # user_wishlist=user_wishlist
                            )
######################################################################################                           

@app.route("/profile_edit")
def show_edit_profile_page():
    """Display to user the Edit Profile Page."""

    if not current_user.is_authenticated:
        return redirect('/login')
    
    user_id = current_user.user_id
    user_object = User.query.get(user_id)
    user_goals = Goal.query.filter(Goal.user_id == user_id).first()

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
    user_object = User.query.get(user_id)
   
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
@app.route('/new_rating/<trail_id>', methods=['POST'])
def create_new_rating(trail_id):
    """Create a new rating."""

    if not current_user.is_authenticated:
        return redirect('/login')
    
    user_id = current_user.user_id
    hike = crud.create_hike(user_id, trail_id) #TypeError: create_hike() missing 5 required positional arguments: 'user_id', 'trail_id', 'hike_completed_on', 'hike_total_time', and 'status_completion'
                                # how do i create a hike id so that it is added to the users log, for example Hike Log -Harding Ice Trail; and then have no details, but the user has the option 
                                # to fill in the details?
                                # how to create the object with optional fields

    score = request.form.get('score')
    challenge_rating = request.form.get('challenge_rating')
    distance_rating = request.form.get('distance_rating')
    ascent_rating = request.form.get('ascent_rating')
    descent_rating = request.form.get('descent_rating')
    user_comment = request.form.get('comment')

    crud.create_rating(score, hike.hike_id, challenge_rating, distance_rating, ascent_rating, descent_rating, user_comment)
    flash('Rating Created')
    return redirect(f'/trails/{trail_id}')

# TRAIL LIST ROUTES
@app.route('/trails')
def trails_list():
    """View trail list."""
    
    all_trails = db.session.query(Trail).all()

    return render_template('trails.html',
                            all_trails=all_trails)

@app.route('/trails/<trail_id>')
def trail_detail(trail_id):
    """Show individual trail details."""

    user_id = current_user.user_id
    user_object = User.query.get(user_id)
    trail_details = Trail.query.get(trail_id)
    user_ratings = user_object.ratings
    # for rating in ratings:
    #     total_score = sum(score)
    #     av_total_score = total_score / num_scores
    # for rating in ratings:
        #total_score = score + score ...
        #av_total_score = total_score / num_scores

    # make api call here to get json from Weather Map API
    # give json info to template as variable

    geo = json.loads(trail_details._geoloc.replace("\'", "\""))

    latitude = geo["lat"]
    longitude = geo["lng"]

    return render_template('trail_details.html',
                            trail_details=trail_details,
                            user_ratings=user_ratings,
                            latitude=latitude,
                            longitude=longitude,
                            trail_id = trail_id
                            #av_total_score=av_total_score
                            )

@app.route('/hike_edit', methods = ["POST"])
def edit_user_hike_goals_and_log():
    """Edit user hike log and trail wishlist."""

    if not current_user.is_authenticated:
        return redirect('/login')

    user_id = current_user.user_id
    user_object = User.query.get(user_id)
   
    form_id = request.form.get("form_id")

    #wishlist form
    if form_id == "add_wishlist":
        trail_id = request.form.get("trail_id") 
        wish = crud.create_wishlist_item(trail_id, user_id)

        return redirect("/") #how stay on same page when html is /trails/<trail_id> -- got error when tried this

    #hike log form
    if form_id == "add_hike_log":
        trail_id = request.form.get("trail_id") 
        
        crud.create_hike(user_id, trail_id) #TODO: Update to hike not hikelog #same as ratings, how to create a hike object / id without all the details (to be edited later by user)

        return redirect("/")

@app.route('/add_friend/<user_id>', methods = ["POST"])
def user_add_friend(user_id):
    """Edit user friend list with new friend."""

    if not current_user.is_authenticated:
        return redirect('/login')

    friend_user_id = user_id #UnboundLocalError: local variable 'user_id' referenced before assignment #TODO: fix this bug
    user_id = current_user.user_id
    user_object = User.query.get(user_id)
    print("-------------------------------------------------")
    print("made it this far")
   
    form_id = request.form.get("form_id")
    crud.create_friend(user_id, friend_user_id)

    return redirect(f"/users/{user_id}")

# PARK LIST ROUTES
@app.route('/parks')
def parks_list():
    """View National Park list."""
    
    all_trails = db.session.query(Trail).all()
    all_parks = crud.get_all_parks() #two parter, keeping this crud function

    return render_template('parks.html',
                            all_parks=all_parks,
                            all_trails=all_trails)

@app.route('/parks/<area_name>')
def park_detail(area_name):
    """Show individual park details."""

    park_trails = db.session.query(Trail).filter(Trail.area_name==area_name).all()

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

    state_parks_details = crud.get_park_states_by_name(state_name) # two parter, keeping this crud function

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

    server_trail = crud.query_trail(route_type, park, state, difficulty) # this function is the crown jewel, kinda wanna keep the crud function

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