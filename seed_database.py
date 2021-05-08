"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime, date

import crud
import model
from model import Image
import server

import csv
from model import db

#dbcreate image_data
os.system('dropdb image_data')
os.system('createdb image_data')

model.connect_to_db(server.app)
model.db.create_all()



#fake comments list
comments = ['wow!', 'too  muddy', 'perfect hike!']

files=os.listdir("static/img/images!")
fnames = ['Melissa', 'Alena', 'Tina', 'Jenny', 'Steph', 'Kristen', 'Emily', 'Deborah', 'Muna', 'Kelsi', 'Samatha', 'Madiha', 'Seale']
lnames = ['Lieblich', 'Sutherland', 'Ong', 'Ainawaer', 'Flatland', 'Gerrity', 'Latif', 'Wong']
tags = ['nature', 'trail', 'Denali', 'Yosemite', 'Acadia', 'Arches','Carlsbad', 'Everglades', 'Glacier', 'Mesa Verde', 'Olympic']

user_list = []
#create fake 10 fake users
for n in range(10):
    username = f'Test{n}'
    password = 'test'
    user_fname = choice(fnames)
    user_lname = choice(lnames)
    profile_picture = choice(files)
    email = f'hiker{n}@gmail.com'

#create user
    user_object = crud.create_user(username, password, user_fname, user_lname, email, profile_picture)
    user_list.append(user_object)
# images
    for i in range(5):
        image = crud.create_image(user_object.user_id,
                                    choice(files),
                                    choice(tags),
                                    choice(tags),
                                    choice(tags))

# friends
for users in user_list:
    friend_object = crud.create_friend(users.user_id, randint(1,10))

