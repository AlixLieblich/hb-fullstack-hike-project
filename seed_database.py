"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

#dbcreate hike_data
os.system('dropdb hike_data')
os.system('createdb hike_data')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/trails.json') as f:
    trails = json.loads(f.read())

trails_in_db = []
for trail in trails:
    trail_name, trail_status, trail_conditions, difficulty, trail_type, 
    physical_rating, total_ascent, total_descent, distance_in_miles, 
    trail_description, location, longitude, latitude = (trail['trail_name'],
                                                        trail['trail_status'],
                                                        trail['trail_conditions'],
                                                        trail['difficult'],
                                                        trail['trail_type'],
                                                        trail['physical_rating'],
                                                        trail['total_ascent'],
                                                        trail['total_descent'],
                                                        trail['distance_in_miles'],
                                                        trail['trail_description'],
                                                        trail['location'],
                                                        trail['longitude'],
                                                        trail['latitude'])

    trail_object = crud.create_trail(trail_name, trail_status, trail_conditions, difficulty, trail_type, 
                physical_rating, total_ascent, total_descent, distance_in_miles, 
                trail_description, location, longitude, latitude)
    trails_in_db.append(trail_object)

for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user_object = crud.create_user(email, password)

    for i in range(10):
        random_trail = choice(trails_in_db)
        score = randint(1,5)
        challenge_rating = randint(1,5)
        distance_rating = randint(1,5)
        asccent_rating = randint(1,5)
        descent_rating = randint(1,5)
        # comment =
        # not sure what to do with comment there

        crud.create_rating(score, user_object, random_trail)

