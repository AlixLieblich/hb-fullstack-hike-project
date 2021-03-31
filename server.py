"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev" #TODO replace with secrets.sh key
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/find-a-hike-form')
def movie_list():
    """View hike form."""
    
    

    return render_template('find-a-hike-form.html')

# @app.route('/movies/<movie_id>')
# def movie_detail(movie_id):
#     """Show individual movie details."""

#     movie_details = crud.get_movie_by_id(movie_id)

#     return render_template('movie_details.html',
#                             movie=movie_details)


# @app.route('/new_user', methods=['POST'])
# def create_new_user():
#     """Create a new user."""

#     user_email = request.form.get('email')
#     user_password = request.form.get('password')

#     user_existence = crud.get_user_by_email(user_email)
    
#     if user_existence:
#         flash('You can\'t create an account with that email. Try again.')
#     else:
#         crud.create_user(user_email, user_password)
#         flash('Your account was successfully created. WelCoMe tO thE ComMunItYYY, you can now log in!')

#     return redirect('/')

# @app.route('/login', methods=['POST'])
# def login():
#     """ """

#     user_email = request.form.get('email')
#     user_password = request.form.get('password')

#     check_user = crud.get_user_by_email(user_email)
#     if check_user.password == user_password:

#         session['user_id'] = check_user.user_id
#         print(session['user_id'])
#         flash('Login Successful. 😄')   
#     else: 
#         flash('Email or password incorrect.') 
#     return redirect('/')
    
# @app.route('/users')
# def user_list():
#     """View user list."""
    
#     all_users = crud.get_all_users()

#     return render_template('users.html',
#                             all_users=all_users)


# @app.route('/users/<user_id>')
# def user_details(user_id):
#     """Show individual user details."""

#     user_details = crud.get_user_by_id(user_id)

#     return render_template('user_details.html',
#                             user=user_details)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True, port=5001)