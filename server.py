"""Server for National Park trail app."""

from flask import (Flask, render_template, request, flash, session, redirect)
import flask_login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from model import db, connect_to_db, User, Trail, Goal, Rating, User_Friend, Hike, Wishlist
import model
import os
import image_helper
from sqlalchemy import and_
from secrets import GOOGLE_API_KEY
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

    user_existence = crud.get_user_by_email(user_email) # somewhat complicated, wanna keep
    
    if user_existence:
        flash('You can\'t create an account with that email. Try again.')
    else:
        crud.create_user(user_name, user_password, user_fname, user_lname, user_email)
        flash('Your account was successfully created. WelCoMe tO thE ComMunItYYY, you can now log in!')

    return render_template('create-account.html')

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
    user_object = User.query.get(user_id)
    user_friends = user_object.added_friends
    user_wishlist = user_object.wishes
    user_hike_log = user_object.hikes
    user_ratings = user_object.ratings
    user_goals = Goal.query.filter(Goal.user_id == user_id).first()
    trails = db.session.query(Trail)

    return render_template('user_profile.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals,
                            user_friends=user_friends,
                            user_wishlist=user_wishlist,
                            user_hike_log=user_hike_log,
                            user_ratings=user_ratings,
                            trails=trails)

@app.route('/users')
def users_list():
    """View users list."""
    
    all_users = db.session.query(User).all()

    return render_template('users.html',
                            all_users=all_users)

@app.route('/users/<user_id>')
def view_user_profiles(user_id):
    """View other user's profiles."""

    user_object = User.query.filter(User.user_id == user_id).first()
    user_goals = Goal.query.filter(Goal.user_id == user_id).first()
    user_wishlist = db.session.query(Wishlist).filter(Wishlist.user_id==user_id).all()

    return render_template('view_users.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals)

@app.route("/profile_edit")
def show_edit_profile_page():
    """Display to user the Edit Profile Page."""

    if not current_user.is_authenticated:
        return redirect('/login')
    
    user_id = current_user.user_id
    user_object = User.query.get(user_id)
    user_goals = Goal.query.filter(Goal.user_id == user_id).first()
    trails = db.session.query(Trail)

    return render_template('profile_edit.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_goals=user_goals,
                            trails=trails)

@app.route('/profile_edit', methods = ["POST"])
def edit_user_profile():
    """Edit user profile with user form responses."""

    if not current_user.is_authenticated:
        return redirect('/login')

    user_id = current_user.user_id
    user_object = User.query.get(user_id)
   
    form_id = request.form.get("form_id")

    #basic form
    if form_id == "basic_profile_information":
        user_fname = request.form.get("first_name")
        user_lname = request.form.get("last_name")
        email = request.form.get("email")
        crud.update_user_profile_info(user_id, user_fname, user_lname, email)

        return redirect("user_profile")

    if form_id == "hiking_goals":

        goal_miles = request.form.get('goal_miles')
        goal_number_hikes = request.form.get('goal_number_hikes')
        goal_hike_difficulty = request.form.get('goal_hike_difficulty')

        crud.update_user_hiking_goals(user_id, goal_miles, goal_number_hikes, goal_hike_difficulty)

        return redirect("user_profile")

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
            return redirect("user_profile")
        else:
            file_name = str(user_id) + ".jpg"
            path = os.path.join(UPLOAD_FOLDER_PROFILE_PICTURE, file_name)
            resized_image.save(path)

            crud.set_user_profile_picture(user_id, file_name) 
        
        return redirect("user_profile")
    #edit friends
    elif form_id == "edit_friends":
        unfriend_id = request.form.get("friends")
        friend = User.query.get(unfriend_id)
        crud.update_friend_list(unfriend_id)
        flash("Friend Removed")

        return redirect("user_profile")

    #edit wishlist
    elif form_id == "edit_wishlist_remove":
        trail_delete_id = request.form.get("wish_remove")

        crud.delete_wishlist_trail(trail_delete_id)
        flash("Trail Deleted")

        return redirect("user_profile")
    #password
    elif form_id == "password_change":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")

        if (crud.update_password(user_id, old_password, new_password) is False): 
            flash("Old password is incorrect")
        else:
            flash("Password Updated")
        return redirect("user_profile")

    else:
        flash("Unhandled form submission")
        return redirect("user_profile")

    return render_template('profile_edit.html',
                            user_id=user_id,
                            user_object=user_object)

# TWILIO ROUTE
@app.route('/send_sms', methods=['POST'])
def send_text():
    """Use Twilio API to send location of a trail when a user has added it to their wishlist."""

    location = trail._geoloc

    client.messages.create(
        body="Hello {{% current_user.user_fname %}}, you have added a trail at location {{% location %}} to your wishlist at National Treasures.",
        from_= '192',
        to='19258081646'
    )
    
# RATING ROUTES
@app.route('/new_rating/<trail_id>', methods=['POST'])
def create_new_rating(trail_id):
    """Create a new rating."""

    if not current_user.is_authenticated:
        return redirect('/login')
    
    user_id = current_user.user_id
    hike = crud.create_hike(user_id, trail_id) 

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
@app.route('/home-alt')
def home_alt():
    """View trail list."""

    return render_template('home-alt.html')
# TRAIL LIST ROUTES
@app.route('/trails')
def trails_list():
    """View trail list."""
    
    all_trails = db.session.query(Trail).order_by('name').all()

    return render_template('trails.html',
                            all_trails=all_trails)

@app.route('/trails/<trail_id>')
def trail_detail(trail_id):
    """Show individual trail details."""

    trail_details = Trail.query.get(trail_id)
    ratings = db.session.query(Rating).all()
 
    av_ratings = crud.get_average_ratings(ratings)

    geo = json.loads(trail_details._geoloc.replace("\'", "\""))

    latitude = geo["lat"]
    longitude = geo["lng"]

    return render_template('trail_details.html',
                            trail_details=trail_details,
                            ratings=ratings,
                            latitude=latitude,
                            longitude=longitude,
                            trail_id = trail_id,
                            av_ratings=av_ratings,
                            geo=geo,
                            GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route('/hike_edit/<trail_id>', methods = ["POST"])
def edit_user_hike_goals_and_log(trail_id):
    """Edit user hike log and trail wishlist."""

    if not current_user.is_authenticated:
        flash('Please Login First!')
        return redirect('/login')


    user_id = current_user.user_id
    user_object = User.query.get(user_id)   
   
    form_id = request.form.get("form_id")

    #wishlist form
    if form_id == "add_wishlist":
        wish = crud.create_wishlist_item(trail_id, user_id)

        return redirect(f'/trails/{trail_id}')

    #hike log form
    if form_id == "add_hike_log":
        trail_id = request.form.get("trail_id") 
        crud.create_hike(user_id, trail_id)

        return redirect(f'/trails/{trail_id}')

@app.route('/add_wishlist', methods = ["POST"])
def edit_user_wishlist(trail_id):
    """Edit user hike log and trail wishlist."""

    if not current_user.is_authenticated:
        flash('Please Login First!')
        return redirect('/login')


    user_id = current_user.user_id
    user_object = User.query.get(user_id)   
   
    form_id = request.form.get("form_id")

    #wishlist form
    if form_id == "add_wishlist":
        wish = crud.create_wishlist_item(trail_id, user_id)

        return redirect(f'/trails/{trail_id}')

        return redirect('/#')

@app.route('/add_friend/<user_id>', methods = ["POST"])
def user_add_friend(user_id):
    """Edit user friend list with new friend."""

    if not current_user.is_authenticated:
        return redirect('/login')

    friend_user_id = user_id 
    user_id = current_user.user_id
    user_object = User.query.get(user_id)
   
    form_id = request.form.get("form_id")
    crud.create_friend(user_id, friend_user_id)

    return redirect(f"/users/{user_id}")

# PARK LIST ROUTES
@app.route('/parks')
def parks_list():
    """View National Park list."""

    all_trails = db.session.query(Trail).all()
    # all_parks = crud.get_all_parks() #two parter, keeping this crud function

    all_parks = db.session.query(Trail.area_name).all()
    all_parks = set(all_parks)
    all_parks = sorted(all_parks)
    # halfway_point = int(len(all_parks)/2)
    # print("len")
    # print(len(all_parks))
    all_parks1 = all_parks[:20]
    all_parks2 = all_parks[21:40]
    all_parks3 = all_parks[41:60]

    return render_template('parks.html',
                            all_parks1=all_parks1,
                            all_parks2=all_parks2,
                            all_parks3=all_parks3,
                            all_trails=all_trails)

@app.route('/parks/<area_name>')
def park_detail(area_name):
    """Show individual park details."""

    park_trails = db.session.query(Trail).filter(Trail.area_name==area_name).order_by('name').all()

    return render_template('park_details.html',
                            park_trails=park_trails,
                            area_name=area_name)

#STATE LIST ROUTES
@app.route('/states')
def states_list():
    """View states list."""
    
    all_states = crud.get_all_states()
    all_states = sorted(all_states)

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

    all_states = crud.get_all_states()
    states = sorted(all_states)

    return render_template('find-a-hike-form.html',
                            states=states)

@app.route('/process_search')
def process_search():
    """Search database for user specifications to find trail."""

    print("15:55")
    all_states = crud.get_all_states()
    states = sorted(all_states)

    session['trail_query'] = {'state_name': request.args.get('state_name'),
                              'difficulty': request.args.get('difficulty_select'),
                              'park': request.args.get('park')}

    trail_query_arguments = {}
    for argument in session['trail_query']:
        if session['trail_query'][argument]:
            trail_query_arguments[argument] = session['trail_query'][argument]
    print("--------------------------------------")
    print(trail_query_arguments)
    
    db_results = crud.query_trail(trail_query_arguments=trail_query_arguments)
    db_results_dict = {}
    for trail in db_results:
        db_results_dict[trail.area_name] = {'park': trail.area_name }
    print("----------------------------------")
    print(db_results_dict)
    return db_results_dict
    



@app.route('/show-form')
def show_form_response():
    """Show user their form filled out."""

    park = request.args.get("chosen-item")   
    difficulty = request.args.get("difficulty")

    server_trail = crud.query_trail_two(park, difficulty) # this function is the crown jewel, kinda wanna keep the crud function
    print(server_trail)
    if server_trail == []:
        server_trail='Sorry, no hikes matched your specifications, please try again with less parameters.'

    return render_template("show-form.html",
                           park=park,
                           difficulty=difficulty,
                           server_trail=server_trail)


 
if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port=5001)