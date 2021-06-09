from requests import request as req
from flask_login import current_user
from werkzeug.security import check_password_hash
from urllib.parse import quote_plus
from . import db
# modules pour décodage base64 en string
import base64
import html
import re
import sqlite3
#from rich import print

class EcoleDirecte():

    def login(username, password):
        payload = 'data={ "identifiant": "' + username + \
                '", "motdepasse": "' + password + '", "acceptationCharte": true }'
        try:
            response = req(
                "POST", "https://api.ecoledirecte.com/v3/login.awp", data=quote_plus(payload)).json()
            token = response['token']
            return response, token
        except Exception as exception:
            if type(exception).__name__ == "ConnectionError":
                print("[reverse bold red]La connexion a échoué[/]")
                print("[red]Vérifiez votre connexion Internet.[/]")
            else:
                print("[reverse bold red]Une erreur inconnue est survenue.[/]")

    def link(username, password, passwordKey):
        def encrypt(key, msg):
            encryped = []
            for i, c in enumerate(msg):
                key_c = ord(key[i % len(key)])
                msg_c = ord(c)
                encryped.append(chr((msg_c + key_c) % 127))
            return ''.join(encryped)

        if not check_password_hash(current_user.password, passwordKey): # Check if the given password is correct
            return False

        current_user.ed_username = username
        current_user.ed_password = encrypt(passwordKey, password)
        db.session.commit()

        return True

    def unlink():
        current_user.ed_username = None
        current_user.ed_password = None
        db.session.commit()
    
    def AddWork(passwordKey):
        """
        Récupère le travail de la semaine d'école directe (cahier de texte) et l'ajoute à la BDD
        """
        def decrypt(key, encryped):
            msg = []
            for i, c in enumerate(encryped):
                key_c = ord(key[i % len(key)])
                enc_c = ord(c)
                msg.append(chr((enc_c - key_c) % 127))
            return ''.join(msg)

        # Get login token from ED
        response, token = EcoleDirecte.login(current_user.ed_username, decrypt(passwordKey, current_user.ed_password))

        if not token:
            return [], token
        # Get all work
        work, token = EcoleDirecte.fetch_work(response["data"]["accounts"][0]["id"], token)

        connection = sqlite3.connect('db.sqlite') #Connect to DB
        cursor = connection.cursor()

        # add work to BDD
        for data in work:
            cursor.execute("INSERT INTO todo (userID, task, date, priority, status, tag) VALUES ('{}','{}','{}','{}','{}','{}')"
                .format(current_user.name, data['task'], data['date'], data['priority'], data['status'], data['tag']))
            
        connection.commit() #Save changes
        connection.close()

        return work, token

    def fetch_work(accountID, token):
        """
        Sous fonction qui récupère les devoirs
        """
        def convert_work(data):
            """Convert raw work data to usable tasks for main
            task format : [task: "{subject} : {desc}", date, priority: medium, tag: "Contrôle"||"Devoir"]"""
            tasks = []
            for date in data.keys(): # each date, which is the key for the works for each day
                # send a request for the day to get the description for each work
                rtask = req("POST", "https://api.ecoledirecte.com/v3/Eleves/" +
                    str(accountID) + f"/cahierdetexte/{date}.awp?verbe=get&", data=payload).json()
                devoirs = rtask["data"]["matieres"]
                # Sort the response to keep only the work and nothing else
                devoirs = [task for task in devoirs if "aFaire" in task.keys()]
                #print(devoirs)
                for task in devoirs: # each work of the day
                    #print(task)
                    # get the description
                    a = base64.b64decode(task["aFaire"]["contenu"])
                    descriptionHTML = a.decode("UTF-8")
                    description = html.unescape(descriptionHTML)
                    # Conversion Regex en string normale
                    desc = re.sub(r"<\/?[a-z]+>|\n", "", description)
                    # remove special characters that break the SQL execution
                    descfiltered = [carac for carac in desc if carac not in ["(",")",":","'"]]
                    desc = ""
                    for carac in descfiltered:
                        desc += carac
                    # get subject
                    subject = task['matiere']
                    # add the task to the list
                    tasks.append({ #
                        "task" : f"{subject}  {desc}",
                        "date" : date,
                        "priority" : "hight" if task["interrogation"] else "medium",
                        "tag" : "Contrôle" if task["interrogation"] else "Devoir",
                        "status" : "disable" if task["aFaire"]["effectue"] else "enable"})
            #print(tasks)
            return tasks

        payload = 'data={"token": "' + token + '"}'
        response = req("POST", "https://api.ecoledirecte.com/v3/Eleves/" +
                    str(accountID) + "/cahierdetexte.awp?verbe=get&", data=payload).json()
        token = response['token'] or token
        return convert_work(response["data"]), token
