# main.py

from flask import Blueprint, render_template, request, jsonify, Flask
from flask_login import login_required, current_user

import sqlite3
import json

from .ecoleDirecte import EcoleDirecte as ED

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/todo')
@login_required
def todo():
    return render_template('todo.html', name=current_user.name)

# Todo section
# Add the elements added by the user in the DB
@main.route('/', methods=['POST'])
@login_required
def todo_post():
#     Get data from the DOM
    data = request.get_data()
    data = data.decode("utf-8") # Convert to UTF-8, currently in byte
    data = json.loads(data) # Convert string to dictionary

    connection = sqlite3.connect('db.sqlite') #Connect to DB
    cursor = connection.cursor()

    #Update the task status in the DB
    if data['goal'] == "updateStatus":
        cursor.execute("UPDATE todo SET status ='"+data['status']+"' WHERE taskID="+data['taskID']+"")
        cursor.execute("SELECT * FROM todo WHERE userID='" + current_user.name + "' ORDER BY taskID DESC LIMIT 1")
        data_list = cursor.fetchall()
        print(f"DEBUG : TaskID -> {data_list[0][0]}") #DEBUG

    elif data['goal'] == "addElement":
        cursor.execute("INSERT INTO todo (userID, task, date, priority) VALUES ('" + current_user.name + "', '" + data['task'] + "', '" + data['date'] + "', '" + data['priority'] + "')")

    connection.commit() #Save changes
    connection.close()

    return jsonify(data_list[0][0] if 'data_list' in locals() else "Success") #Return the taskID

@main.route('/getdata')
@login_required
def getdata():
    return render_template('getdata.html')

@main.route('/getdata', methods=['POST'])
@login_required
def todo_get():
    # get all tasks of the current user
    connection = sqlite3.connect('db.sqlite') #Connect to DB
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM todo WHERE userID='{current_user.name}'")
    data_list = cursor.fetchall()
    #print(data_list)

    connection.commit() #Save changes
    connection.close()
    print (data_list)
    return jsonify(data_list)


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
    print(response)
    print(token)
    if not token :
        flash('Invalid username or password, please try again.')
        return redirect(url_for("main.ecoledirecte"))

    # Add informations in the database.
    ED.link(ED_username, ED_password)

    return redirect(url_for('main.profile'))
