"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime, date

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
    # print('***********************************')
    # print('TRAILS', trails)

trails_in_db = []
for trail in trails:
    # print("----------------------------------")
    # print('TRAIL', trail)
    trail_name = trail['trail_name']
    trail_status = trail['trail_status']
    trail_conditions = trail['trail_conditions']
    difficulty = trail['difficulty']
    trail_type = trail['trail_type']
    physical_rating = trail['physical_rating']
    total_ascent =trail['total_ascent']
    total_descent= trail['total_descent']
    distance_in_miles = trail['distance_in_miles']
    trail_description = trail['trail_description']
    location= trail['location']
    longitude = trail['longitude']
    latitude = trail['latitude'] 
    
    # trail_name, trail_status, trail_conditions, difficulty, trail_type, 
    # physical_rating, total_ascent, total_descent, distance_in_miles, 
    # trail_description, location, longitude, latitude = (trail['trail_name'],
    #                                                     trail['trail_status'],
    #                                                     trail['trail_conditions'],
    #                                                     trail['difficulty'],
    #                                                     trail['trail_type'],
    #                                                     trail['physical_rating'],
    #                                                     trail['total_ascent'],
    #                                                     trail['total_descent'],
    #                                                     trail['distance_in_miles'],
    #                                                     trail['trail_description'],
    #                                                     trail['location'],
    #                                                     trail['longitude'],
    #                                                     trail['latitude'])

    trail_object = crud.create_trail(trail_name, trail_status, trail_conditions, difficulty, trail_type, 
                physical_rating, total_ascent, total_descent, distance_in_miles, 
                trail_description, location, longitude, latitude)
    trails_in_db.append(trail_object)
comments = ['wow!', 'too  muddy']
for n in range(10):
    username = 'Test'
    email = f'user{n}@test.com'
    password = 'test'

    #create user
    user_object = crud.create_user(username, password, email)

    #create 1 hike associated with user above
    hike_object = crud.create_hike(user_object.user_id, 
                                    choice(trails_in_db).trail_id,
                                    date.today(), # date.today is hike date completed on,
                                    1,  #1 is time to complete
                                    True)  #true is booll for hike completed

    # #create 10 raatings associated with user above
    # for i in range(10):
    #     random_trail = choice(trails_in_db)
    #     score = randint(1,5)
    #     challenge_rating = randint(1,5)
    #     distance_rating = randint(1,5)
    #     asccent_rating = randint(1,5)
    #     descent_rating = randint(1,5)
    #     comment = choice(comments)

    # print(hike_object)
    
    #create 1 rating associated with above user and hike
    # crud.create_rating(score, trail_object, challenge_rating, distance_rating, asccent_rating, descent_rating, comment)

    rating = crud.create_rating(hike_id = hike_object.hike_id, 
                        score = randint(1,5), 
                        challenge_rating = randint(1,5), 
                        distance_rating = randint(1,5), 
                        ascent_rating = randint(1,5), 
                        descent_rating = randint(1,5), 
                        comment = choice(comments))
    print(rating)


