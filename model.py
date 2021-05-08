"""Models for trail locating app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///image_data', echo=False):
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

    added_friends = db.relationship('User_Friend', backref='current_user_friended_by', foreign_keys='User_Friend.user_id') # one to many # your friendlist
    friended_by = db.relationship('User_Friend', backref='current_user_added_friend', foreign_keys='User_Friend.friend_user_id') # one to many #users who have added current user to their friend list (may not be mutual friends); name of the person that you added
    images = db.relationship('Image', backref='images', foreign_keys='Image.user_id')

        # Flask Login Methods
    def is_authenticated(self):
        """If user is authenticated, return true."""

        return True

    def is_active(self):  
        """If user is active, return true."""

        return True           


        return(self.user_id) 
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

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

class Image(db.Model):
    """Images."""

    __tablename__ = 'images'

    image_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    image_name = db.Column(db.String)
    tag1 = db.Column(db.String)
    tag2 = db.Column(db.String)
    tag3 = db.Column(db.String)

    def __repr__(self):
        return f'Image ID image_id={self.image_id}'

if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
