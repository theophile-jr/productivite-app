# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@login_required
@auth.route('/ecoledirecte')
def ecoledirecte():
    return render_template('ecoledirecte.html')

@login_required
@auth.route('/ecoledirecte', methods=['POST'])
def ecoledirecte_post():
    user = current_user

    # If an account is already given, stop here
    if user.ed_username:
        return redirect(url_for("main.index"))

    EDusername = request.form.get('username')
    EDpassword = request.form.get('password')

    #Check if the informations are valid.
    response, token = login(EDusername, EDpassword)
    if not token : 
        return redirect(url_for("auth.ecoledirect"))


    user.ed_username = EDusername
    user.ed_password = EDpassword
    db.session.commit()

    return redirect(url_for('main.index'))

def ED_login(username, password):
    payload = 'data={ "identifiant": "' + username + \
              '", "motdepasse": "' + password + '", "acceptationCharte": true }'
    try:
        response = req(
            "POST", "https://api.ecoledirecte.com/v3/login.awp", data=payload).json()
        token = response['token'] or token
        return response, token
    except Exception as exception:
        if type(exception).__name__ == "ConnectionError":
            print("[reverse bold red]La connexion a échoué[/]")
            print("[red]Vérifiez votre connexion Internet.[/]")
        else:
            print("[reverse bold red]Une erreur inconnue est survenue.[/]")
        calm_exit()