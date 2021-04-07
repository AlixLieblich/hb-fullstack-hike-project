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
    email = db.Column(db.String, nullable=False, unique=True)

    # hikes = a list of Hike objects

    goals = db.relationship('Goal', backref='users')


    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

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
    num_miles_total = db.Column(db.Integer) #total miles want to complete; subtract miles when complete hikes
    num_hikes_total = db.Column(db.Integer)
    difficulty_hike_goal = db.Column(db.Integer) 
    

    # hikes = a list of Hike objects

    def __repr__(self):
        return f'<Goal goal_id={self.goal_id} name={self.trail_name}>'

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

    # hikes = a list of Hike objects

def __repr__(self):
    return f'<Hike hike_id={self.hike_id} name={self.hike_name}>'

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
