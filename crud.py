"""CRUD operations."""

from model import db, User, connect_to_db, User_Friend, Image
from sqlalchemy import and_
from datetime import datetime, date

# USER FUNCTIONS
def create_user(username, password, user_fname, user_lname, email, profile_picture="/static/img/profile_pictures/default.png"):
    """Create and return a new user."""

    user = User(username=username, password=password, user_fname=user_fname, user_lname=user_lname, profile_picture=profile_picture, email=email)

    db.session.add(user)
    db.session.commit()

    return user

def create_image(user_id, image_name, tag1, tag2, tag3):
    """Create an Image object."""

    image = Image(user_id=user_id, image_name=image_name, tag1=tag1, tag2=tag2, tag3=tag3)

    db.session.add(image)
    db.session.commit()

    return image

# Profile Edit Functions
def update_user_profile_info(user_id, user_fname, user_lname, email):
    """Update basic user profile information."""
    
    user=User.query.filter(User.user_id == user_id).first()

    if email != None:
        user.update_email(email)
    if user_fname != None:
        user.update_first_name(user_fname)
    if user_lname != None:
        user.update_last_name
    
    db.session.commit()


def set_user_profile_picture(user_id, file_name):
    """Update user profile picture."""

    user = User.query.get(user_id)
    
    user.profile_picture = file_name
    db.session.commit()

def update_password(user_id, old_password, new_password):
    """Update user password."""

    # user_password = (User.query.filter(User.user_id == user_id).filter(User.password == old_password).first())
    user_password = User.query.filter(User.user_id == user_id).first()

    if not user_password:
        # flash('That is not your correct password.')
        # return False
        return redirect('/profile_edit')

    # db.session.query(User.user_id == user_id).update({"password": new_password,})
    if user_password:
        user_password.update_password(new_password)

    db.session.commit()
    # flash('Successful password change.')
    return True

def update_friend_list(friend_user_id):
    """Delete a friend."""

    User_friend.query.filter_by(user_)

    db.session.commit()

    return True

def delete_wishlist_trail(trail_id):
    """Delete a wishlist."""

    db.session.delete(trail_id)

    db.session.commit()

    return True

# Friend functions
def create_friend(user_id, friend_user_id):
    """Create and return a new friend."""

    friend = User_Friend(user_id=user_id, friend_user_id=friend_user_id)

    db.session.add(friend)
    db.session.commit()

    return friend

def get_user_friends(user_id):
    """Given a user_id, return an object of that user's friends."""

    friends = db.session.query(User_Friend).filter(User_Friend.user_id==user_id).all() 

    return friends

def get_friend_user_object(friend_user_id):
    """Given a friend user ID, return that user object."""

    user_id = friend_user_id
    friend = User.query.filter(User.user_id == user_id).first()

    return friend

if __name__ == '__main__':
    from server import app
    connect_to_db(app)