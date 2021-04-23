"""CRUD operations."""

from model import db, User, Hike, Rating, Goal, Trail, connect_to_db, User_Friend, Wishlist
from sqlalchemy import and_
from datetime import datetime, date

# USER FUNCTIONS
def create_user(username, password, user_fname, user_lname, profile_picture, email):
    """Create and return a new user."""

    user = User(username=username, password=password, user_fname=user_fname, user_lname=user_lname, profile_picture=profile_picture, email=email)

    db.session.add(user)
    db.session.commit()

    return user

# def get_all_users():
#     """Display all users."""

#     return db.session.query(User).all()


def greeting():
    """Display greeting header. Gives visual knowledge of wheter user is logged in or not."""
# under construction

    # if session is empty:
    #   greeting_message = "Hello! Feel free to find a hike, or <a Login> here for user functionality"
    # else:
    #   greeting_message = "Hello f'user.fname'!"

    return db.session.query(User).all()

def get_user_by_username(username): #hiking_object.user_id
    """Return a user object given a user id."""

    return User.query.filter_by(username=username).first() # using info from other tables to get info from other tables -> #hiking_object.user_id

def get_user_by_email(email):
    """Return a user object given an email, else None."""

    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    """Return a user object given a user_id, else None."""

    return User.query.filter(User.user_id == user_id).first()

def get_goals_by_user_id(user_id):
    """Return user goals given a user_id."""

    return Goal.query.filter(Goal.user_id == user_id).first()

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

def update_user_hiking_goals(user_id, goal_miles, goal_number_hikes, goal_hike_difficulty):
    """Update users hiking goals."""

    user_goals = Goal.query.filter(Goal.user_id == user_id).first()

    if goal_miles != None:
        user_goals.update_goal_miles(goal_miles)
    if goal_number_hikes != None:
        user_goals.update_goal_number_hikes(goal_number_hikes)
    if goal_hike_difficulty != None:
        user_goals.update_goal_hike_difficulty(goal_hike_difficulty)

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

    # friends_info = []
    # for friend in friends:
    user_id = friend_user_id
    friend = User.query.filter(User.user_id == user_id).first()
    # friends_info.append(friend)

    return friend

# Wishlist functions
def create_wishlist_item(trail_id, user_id):
    """Create and return a new wishlist item."""

    wishlist_item = Wishlist(trail_id=trail_id, user_id=user_id)

    db.session.add(wishlist_item)
    db.session.commit()

    return wishlist_item
    # this funciton can be replaced with 'users.wishes.append(Trail.query.get(trail_id))' this needs to be paired with db.session.commit

# def get_user_wishes(user_id):
#     """Given a user_id, return an object of that user's wishlist trails."""

#     return db.session.query(Wishlist).filter(Wishlist.user_id==user_id).all()

def get_wish_trail_object(trail_id):
    """Given a tail ID, return the object for that trail."""

    # return db.session.query(Trail).filter(Trail.trail_id==100).all()
    # trail_id = wish_trail_id
    trail = Trail.query.filter(Trail.trail_id == trail_id).first()
    return trail

# # Hike Log functions
# def create_hike_log_item(user_id, hike_id):
#     """Create and return a new completed hike item for hike log."""

#     completed_hike_item = Hike_Log(user_id=user_id, hike_id=hike_id)

#     db.session.add(completed_hike_item)
#     db.session.commit()

#     return completed_hike_item

# def get_user_hike_log(user_id):
#     """Given a user_id, return an object of that user's wishlist trails."""

#     return db.session.query(Hike_Log).filter(Hike_Log.user_id==user_id).all()

# def get_log_trail_object(hike_id):
#     """Given a hike ID, return the object for that trail."""

#     hike = Hike.query.filter(Hike.hike_id == hike_id).first()
#     return hike

#goalz
def create_goal(goal_miles, goal_number_hikes, goal_hike_difficulty, user_id):
    """Create and return a new goal."""

    goal = Goal(goal_miles=goal_miles,
                goal_number_hikes=goal_number_hikes,
                goal_hike_difficulty=goal_hike_difficulty,
                user_id=user_id) 
    
    db.session.add(goal)
    db.session.commit()

    return goal

# TRAIL FUNCTIONS
def create_trail(name,area_name,city_name,state_name,country_name,_geoloc,popularity,length,elevation_gain,difficulty_rating,route_type,visitor_usage,avg_rating,num_reviews,features,activities,units
):
    """Create and return a new trail."""

    trail = Trail(name=name,
                  area_name=area_name,
                  city_name=city_name,
                  state_name=state_name,
                  country_name=country_name,
                  _geoloc=_geoloc,
                  popularity=popularity, 
                  length=length,
                  elevation_gain=elevation_gain,
                  difficulty_rating=difficulty_rating,
                  route_type=route_type,
                  visitor_usage=visitor_usage,
                  features=features,
                  activities=activities,
                  units=units)
    
    db.session.add(trail)
    db.session.commit()

    return trail

# def get_all_trails():
#     """Display all trails."""

#     return db.session.query(Trail).all()

def get_trail_by_id(trail_id):
    """Return a trail object given a trail id."""

    return Trail.query.get(trail_id)

# def update_wish_list(user_id, trail_id):
#     """Update users wishlist."""

#     user_wishlist = Goal.query.filter(Goal.user_id == user_id).first()

#     if goal_miles != None:
#         user_goals.update_goal_miles(goal_miles)
#     if goal_number_hikes != None:
#         user_goals.update_goal_number_hikes(goal_number_hikes)
#     if goal_hike_difficulty != None:
#         user_goals.update_goal_hike_difficulty(goal_hike_difficulty)

#     db.session.commit()

# PARK FUNCTIONS
def get_all_parks():
    """Display all National Parks."""

    all_parks = db.session.query(Trail.area_name).all()
    all_parks = set(all_parks)
    return all_parks

def get_park_by_name(area_name):
    """Return a park object given an area_name."""

    return Trail.query.filter_by(area_name=area_name).all()

# there is an error on this helper function "TypeError: get_parks_trails_by_name() missing 1 required positional argument: 'area_name'"; which
# makes some sence bc its a twin function the def get_trail_by_id below which means that area_name is not translated but trail_id is, and since
# parks dont have IDs but trails do... im not sure how to fix this problem.
# def get_parks_trails_by_name(area_name):
#     """Return a list of trails given an area_name."""

#     park_trails = db.session.query(Trail).filter(Trail.area_name==area_name).all()
#     return park_trails

# STATE FUNCTIONS
def get_all_states():
    """Display all States."""

    all_states = db.session.query(Trail.state_name).all()
    all_states = set(all_states)
    return all_states

def get_park_states_by_name(state_name):
    """Return a set of state name variables given an state_name."""

    state_parks = db.session.query(Trail.area_name).filter(Trail.state_name==state_name).all()
    # state_parks = Trail.query.filter_by(state_name=state_name).all()
    state_parks = set(state_parks)
    print("****************************")
    print(state_parks)

    return state_parks

# RATING FUNCTIONS
def create_rating(score, hike_id, challenge_rating, distance_rating, ascent_rating, descent_rating, comment):
    """Create and return a new rating."""

    rating = Rating(score=score,
                    hike_id=hike_id,
                    challenge_rating=challenge_rating,
                    distance_rating=distance_rating,
                    ascent_rating=ascent_rating,
                    descent_rating=descent_rating,
                    comment=comment) 

    db.session.add(rating)
    db.session.commit()

    return rating


def create_rating(hike_id, score, challenge_rating, distance_rating, ascent_rating, descent_rating, comment):
    """Create and return a new rating (score)."""

    rating = Rating(hike_id=hike_id,
                    score=score,
                    challenge_rating=challenge_rating,
                    distance_rating=distance_rating,
                    ascent_rating=ascent_rating,
                    descent_rating=descent_rating,
                    comment=comment) 
    
    db.session.add(rating)
    db.session.commit()

    return rating

def get_all_ratings():
    """Display all ratings."""

    return db.session.query(Rating).all()

def get_user_ratings(user_id):
    """Given a user_id, return all ratings made by that user."""

    hikes = Hike.query.get(user_id)
    ratings = hikes.ratings
    # ratings = Hike.query.filter(Hike.user_id == user_id).on

    return ratings

# HIKE FUNCTIONS
def create_hike(user_id, trail_id, hike_completed_on=date.today(), hike_total_time=1, status_completion=True):
    """Create and return a new hike."""

    hike = Hike(user_id=user_id,
                trail_id=trail_id,
                hike_completed_on=hike_completed_on,
                hike_total_time=hike_total_time,
                status_completion=status_completion)
    
    db.session.add(hike)
    db.session.commit()

    return hike

# FIND A TRAIL FUNCTION
def query_trail(route_type, park, state, difficulty):
    """Take in form responses and query for a resultant trail."""

    # trail = Trail.query.filter(and_(Trail.route_type==route_type, Trail.area_name==park, Trail.state_name==state, Trail.difficulty_rating==difficulty)) 
    trail = db.session.query(Trail).filter(and_(Trail.difficulty_rating==difficulty, Trail.route_type==route_type, Trail.state_name==state))
    # print("-----------------------------------------")
    # for trails in trail:
    #     print(trail)

    return trail.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)