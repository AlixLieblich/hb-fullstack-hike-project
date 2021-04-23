"""Models for trail locating app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///hike_data', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class User(db.Model):
    """A user.""" #more descriptive docstrings

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # created_on = db.Column(db.DateTime)
    user_fname = db.Column(db.String)
    user_lname = db.Column(db.String)
    profile_picture = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)

    # hikes = a list of Hike objects

    goals = db.relationship('Goal', backref='user')
    added_friends = db.relationship('User_Friend', backref='current_user_friended_by', foreign_keys='User_Friend.user_id') # one to many # your friendlist
    friended_by = db.relationship('User_Friend', backref='current_user_added_friend', foreign_keys='User_Friend.friend_user_id') # one to many #users who have added current user to their friend list (may not be mutual friends); name of the person that you added
    wishes = db.relationship('Wishlist', backref='user')
    ratings = db.relationship('Rating',
                                secondary='hikes',
                                backref='users')

        # Flask Login Methods
    def is_authenticated(self):
        """If user is authenticated, return true."""

        return True

    def is_active(self):  
        """If user is active, return true."""

        return True           

    def is_anonymous(self):
        """If user is anonymous, return true."""
        return False          

    def update_email(self, email):
        """Update user email."""

        self.email = email

    def update_first_name(self, user_fname):
        """Update user first name."""

        self.user_fname = user_fname

    def update_last_name(self, user_lname):
        """Update user last night."""

        self.user_lname = user_lname

    def update_password(self, password):
        """Update user password."""
        
        self.password = password


    def get_id(self):
        """Return ID that uniquely identifies user."""

        return(self.user_id) # this doesnt work, 'AttributeError: 'str' object has no attribute 'user_id'' when click on My Account .... idk, it works one line below sooo i guess profile pages are on hold

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

##################################################################
class User_Friend(db.Model):
    """User's Friends."""

    __tablename__ = 'user_friends'

    user_friend_list_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True) #the ID of the relationship itself
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #the user logged in (ME)
    friend_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #the user I am friending (not me)

    def __repr__(self):
        return f'<User ID user_id={self.user_id} Friend user ID friend_user_id={self.friend_user_id}>'

class Wishlist(db.Model):
    """User's wishlist of trails to hike."""

    __tablename__ = 'user_wishlist'

    wish_trail_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return f'<Wish trail wish_trail_id={self.wish_trail_id} User user_id={self.user_id}>'

# hike log iz ded to me now gang gang
class Hike_Log(db.Model):
    """User's list of completed hikes."""

    __tablename__ = 'user_hike_log'

    completed_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    hike_id = db.Column(db.Integer, db.ForeignKey('hikes.hike_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return f'<Completed hike completed_id={self.completed_id} User user_id={self.user_id}>'

###########################################################3######

class Trail(db.Model):
    """A Trail."""

    __tablename__ = 'trails'

    trail_id = db.Column(db.Integer, 
                          autoincrement=True, 
                          primary_key=True)
    # trail_id = db.Column(db.Integer)
    name = db.Column(db.String)
    area_name = db.Column(db.String)
    city_name = db.Column(db.String) 
    state_name = db.Column(db.String)
    country_name = db.Column(db.String)
    _geoloc = db.Column(db.String)
    popularity = db.Column(db.String)
    length = db.Column(db.String)
    elevation_gain = db.Column(db.String)
    difficulty_rating = db.Column(db.Integer)
    route_type = db.Column(db.String)
    visitor_usage = db.Column(db.String)
    features = db.Column(db.String)
    activities = db.Column(db.String)
    units = db.Column(db.String)
        
    # hikes = a list of Hike objects
    wishes = db.relationship('Wishlist', backref='trail')

    def __repr__(self):
        return f'<Trail trail_id={self.trail_id} name={self.name}>'

class Rating(db.Model):
    """A rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hike_id = db.Column(db.Integer, db.ForeignKey('hikes.hike_id')) # fk to hikes
    score = db.Column(db.Integer)
    challenge_rating = db.Column(db.Integer)
    distance_rating = db.Column(db.Integer)
    ascent_rating = db.Column(db.Integer)
    descent_rating = db.Column(db.Integer)
    comment = db.Column(db.String)

    # hikes = a list of Hike objects

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'

class Goal(db.Model):
    """A Goal."""

    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, 
                          autoincrement=True, 
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    goal_miles = db.Column(db.Integer) #total miles want to complete; subtract miles when complete hikes
    goal_number_hikes = db.Column(db.Integer)
    goal_hike_difficulty = db.Column(db.Integer) 
    

    # hikes = a list of Hike objects

    def update_goal_miles(self, goal_miles):
        """Update user goal_miles."""

        self.goal_miles = goal_miles

    def update_goal_number_hikes(self, goal_number_hikes):
        """Update user goal_number_hikes."""

        self.goal_number_hikes = goal_number_hikes

    def update_goal_hike_difficulty(self, goal_hike_difficulty):
        """Update user last night."""
        
        self.goal_hike_difficulty = goal_hike_difficulty

    def __repr__(self):
        return f'<Goal goal_id={self.goal_id} user_id={self.user_id}>'

class Hike(db.Model):
    """A Hike."""

    __tablename__ = 'hikes'

    hike_id = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'))
    hike_completed_on = db.Column(db.DateTime)
    hike_total_time = db.Column(db.Integer)
    status_completion = db.Column(db.Boolean)

    user = db.relationship('User', backref='hikes')
    ratings = db.relationship('Rating', backref='hikes') 
    trails = db.relationship('Trail', backref='hikes')
    logs = db.relationship('Hike_Log', backref='hikes')

    # hikes = a list of Hike objects

def __repr__(self):
    return f'<Hike hike_id={self.hike_id} name={self.hike_name}>'

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
