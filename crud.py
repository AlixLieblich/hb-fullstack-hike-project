"""CRUD operations."""

from model import db, User, Hike, Rating, Goal, Trail, connect_to_db

def create_user(username, password, email):
    """Create and return a new user."""

    user = User(username=username, password=password, email=email)

    db.session.add(user)
    db.session.commit()

    return user

def get_all_users():
    """Display all users."""

    return db.session.query(User).all()

def get_user_by_id(user_id): #hiking_object.user_id
    """Return a user object given a user id."""

    return User.query.get(user_id)  # using info from other tables to get info from other tables -> #hiking_object.user_id

def get_user_by_email(email):
    """Return a user object given an email, else None."""

    return User.query.filter(User.email == email).first()

def create_trail(trail_name, trail_status, trail_conditions, difficulty, trail_type, 
                physical_rating, total_ascent, total_descent, distance_in_miles, 
                trail_description, location, longitude, latitude):
    """Create and return a new trail."""

    trail = Trail(trail_name=trail_name,
                  trail_status=trail_status, 
                  trail_conditions=trail_conditions, 
                  difficulty=difficulty,
                  trail_type=trail_type,
                  physical_rating=physical_rating,
                  total_ascent=total_ascent,
                  total_descent=total_descent,
                  distance_in_miles=distance_in_miles,
                  trail_description=trail_description,
                  location=location,
                  longitude=longitude,
                  latitude=latitude)
    
    db.session.add(trail)
    db.session.commit()

    return trail

def get_all_trails():
    """Display all trails."""

    return db.session.query(Trails).all()

def get_trail_by_id(trail_id):
    """Return a trail object given a trail id."""

    return Trail.query.get(trail_id)

def create_rating(score, hike_id, challenge_rating, distance_rating, ascent_rating, descent_rating, comment):
    """Create and return a new rating."""

    rating = Rating(score=score,
                    hike_id=hike_id,
                    challenge_rating=challenge_rating,
                    distance_rating=distance_rating,
                    ascent_rating=ascent_rating,
                    descent_rating=descent_rating,
                    comment=comment) #not sure if user and hike are right
    
    db.session.add(rating)
    db.session.commit()

    return rating

def create_goal(num_miles_total, num_hikes_total, user):
    """Create and return a new rating (score)."""

    goal = Goal(num_miles_total=num_miles_total,
                num_hikes_total=num_hikes_total,
                difficulty_hike_goal=difficulty_hike_goal,
                user=user) #not sure if user is right
    
    db.session.add(goal)
    db.session.commit()

    return goal

def create_hike(user_id, trail_id, hike_completed_on, hike_total_time, status_completion):
    """Create and return a new hike."""

    hike = Hike(user_id=user_id,
                trail_id=trail_id,
                hike_completed_on=hike_completed_on,
                hike_total_time=hike_total_time,
                status_completion=status_completion)
    
    db.session.add(hike)
    db.session.commit()

    return hike


if __name__ == '__main__':
    from server import app
    connect_to_db(app)