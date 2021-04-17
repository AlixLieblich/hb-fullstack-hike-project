"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime, date

import crud
import model
import server

import csv
from crud import create_trail
from model import db

#dbcreate hike_data
os.system('dropdb hike_data')
os.system('createdb hike_data')

model.connect_to_db(server.app)
model.db.create_all()

# read csv and write to trails_in_db
with open('nationalpark.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    trails_in_db = []
    for row in reader:
        # print(row['trail_id'])
        trail_object = create_trail(row['name'],row['area_name'],row['city_name'],row['state_name'],row['country_name'],row['_geoloc'],row['popularity'],row['length'],row['elevation_gain'],row['difficulty_rating'],row['route_type'],row['visitor_usage'],row['avg_rating'],row['num_reviews'],row['features'],row['activities'],row['units'])
        trails_in_db.append(trail_object)

#fake comments list
comments = ['wow!', 'too  muddy', 'perfect hike!']

files=os.listdir("static/img/profile_pictures")

user_list = []
#create fake 10 fake users
for n in range(10):
    username = f'Test{n}'
    password = 'test'
    user_fname = f'Balloonicorn{n}' #running seed does not generate these f and l names
    user_lname = f'Hackbright{n}'
    profile_picture = choice(files)
    email = f'user{n}@test.com'

    #create user
    user_object = crud.create_user(username, password, user_fname, user_lname, profile_picture, email)
    user_list.append(user_object)

    #create 1 hike associated with user above
    hike_object = crud.create_hike(user_object.user_id, 
                                   choice(trails_in_db).trail_id,
                                   date.today(),   # date.today is hike date completed on,
                                   1,              # 1 is time to complete
                                   True)           # true is booll for hike completed

    # Create User Goals
    goal_miles = randint(1,20)
    goal_number_hikes = randint(1,20)
    goal_hike_difficulty = randint(1,10)

    goal_object = crud.create_goal(goal_miles, goal_number_hikes, goal_hike_difficulty, user_object.user_id)

    # # Create 1 friend per user
    # friend_object = crud.create_friend(user_object.user_id, randint(0,9))

    # 1 trail for user wishlist
    wishlist_item = crud.create_wishlist_item(choice(trails_in_db).trail_id, user_object.user_id)

    # 1 trail for Hike Log
    hike_log_item = crud.create_hike_log_item(hike_object.hike_id, user_object.user_id)

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

for users in user_list:
    # Create 1 friend per user
    friend_object = crud.create_friend(users.user_id, randint(1,10))
    wishlist_item = crud.create_wishlist_item(choice(trails_in_db).trail_id, users.user_id)
    hike_log_item = crud.create_hike_log_item(hike_object.hike_id, users.user_id)

for users in user_list:
    # Create 1 friend per user
    friend_object = crud.create_friend(users.user_id, randint(1,10))
    wishlist_item = crud.create_wishlist_item(choice(trails_in_db).trail_id, users.user_id)
    hike_log_item = crud.create_hike_log_item(hike_object.hike_id, users.user_id)


