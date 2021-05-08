"""Server for National Park trail app."""

from flask import (Flask, render_template, request, flash, session, redirect)
import flask_login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from model import db, connect_to_db, User, User_Friend, Image
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

UPLOAD_FOLDER_PROFILE_PICTURE = "./static/img/profile_pictures/"
UPLOAD_FOLDER_IMAGE = "./static/img/images!/"

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

# SEARCH BAR
@app.route('/search_bar')
def search_bar():
    """Use navbar search bar."""
    print("-------------------------------------------------")

    print("howdy")

    form_id = request.form.get("form_id")
    print('1 form id:')
    print(form_id)
    #add image
    if form_id == "search":
        print('form id:')
        print(form_id)
    
        search_query = request.form.get('search_query')
        print("--------------------------------")
        print('search query:')
        print(search_query)

        search_query = db.session.query(Image).filter(Image.tag1==search_query).all()
        if search_query == None:
            print('1')
            search_query = db.session.query(Image).filter(Image.tag2==(search_query)).all()
            if search_query == None:
                print('2')
                search_query = db.session.query(Image).filter(Image.tag3==(search_query)).all()
    
    return render_template('show-form.html',
                            search_query=search_query)

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
    user_images = user_object.images

    return render_template('user_profile.html',
                            user_id=user_id,
                            user_object=user_object,
                            user_images=user_images)

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


    return render_template('view_users.html',
                            user_id=user_id,
                            user_object=user_object)

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
    print("-----------------------------")
    print("trying someting dif")
    print(form_id)
    #add image
    if form_id == "add_image":
        tag1 = request.form.get("tag1")
        tag2 = request.form.get("tag2")
        tag3 = request.form.get("tag3")

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
            path = os.path.join(UPLOAD_FOLDER_IMAGE, file_name)
            resized_image.save(path)
        
        image = crud.create_image(user_id, file_name, tag1, tag2, tag3)

        return redirect("user_profile")

    #basic form
    if form_id == "basic_profile_information":
        user_fname = request.form.get("first_name")
        user_lname = request.form.get("last_name")
        email = request.form.get("email")
        crud.update_user_profile_info(user_id, user_fname, user_lname, email)

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

# GALLERY
@app.route('/all_images')
def display_gallery():
    """Display all images in database."""

    images = db.session.query(Image).all()

    return render_template('all_images.html',
                            images=images)

@app.route('/add_image/<user_id>', methods = ["POST"])
def edit_user_hike_goals_and_log(trail_id):
    """Edit user hike log and trail wishlist."""

    if not current_user.is_authenticated:
        flash('Please Login First!')
        return redirect('/login')


    user_id = current_user.user_id
    user_object = User.query.get(user_id)   
   
    form_id = request.form.get("form_id")

    #wishlist form
    if form_id == "add_image":
        wish = crud.create_wishlist_item(trail_id, user_id)

        return redirect(f'/trails/{trail_id}')


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
 
if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port=5001)