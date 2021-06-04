# main.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .ecoleDirecte import EcoleDirecte as ED

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, ecoledirecte=bool(current_user.ed_username))

@main.route('/ecoledirecte')
@login_required
def ecoledirecte():
    # If an account is already given, stop here
    if current_user.ed_username:
        return redirect(url_for("main.profile"))
    return render_template('ecoledirecte.html')

@main.route('/ecoledirecte_unlink')
@login_required
def ecoledirecte_unlink():
    ED.unlink()
    return redirect(url_for("main.profile"))

@main.route('/ecoledirecte', methods=['POST'])
@login_required
def ecoledirecte_post():
    # Get informations throught the form.
    ED_username = request.form.get('username')
    ED_password = request.form.get('password')

    #Check if the informations are valid, and display an error if not.
    response, token = ED.login(ED_username, ED_password)
    if not token :
        flash('Invalid username or password, please try again.')
        return redirect(url_for("main.ecoledirecte"))

    # Add informations in the database.
    ED.link(ED_username, ED_password)

    return redirect(url_for('main.profile'))
