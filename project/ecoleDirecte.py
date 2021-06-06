from requests import request as req
from flask_login import current_user
from werkzeug.security import generate_password_hash
from urllib.parse import quote_plus
from . import db

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

    def link(username, password):
        current_user.ed_username = username
        current_user.ed_password = generate_password_hash(password, method="sha256")
        db.session.commit()

    def unlink():
        current_user.ed_username = None
        current_user.ed_password = None
        db.session.commit()
    
    def getWork():
        # Get login token from ED
        response, token = EcoleDirecte.login(current_user.ed_username, current_user.ed_password)

        if not token:
            print("Une erreur est survenue lors de la récupération des devoirs")
            return [], token

        # Get all work
        response, token = EcoleDirecte.fetch_work(response["data"]["accounts"]["id"], token)

        if not token:
            print("Une erreur est survenue lors de la récupération des devoirs")
            return [], token

    def fetch_work(accountID, token):
        def convert_work(data):
            """Convert raw work data to usable tasks for main"""
            #https://api.ecoledirecte.com/v3/Eleves/6097/cahierdetexte/2021-06-08.awp?verbe=get&
            for task in data.items():
                print(task)
                # send a request for each day to get the description for each work
                r = req("POST", "https://api.ecoledirecte.com/v3/Eleves/" +
                    str(accountID) + f"/cahierdetexte/{task[0]}.awp?verbe=get&", data=payload).json()
                # get the description
                r["data"]



        payload = 'data={"token": "' + token + '"}'
        response = req("POST", "https://api.ecoledirecte.com/v3/Eleves/" +
                    str(accountID) + "/cahierdetexte.awp?verbe=get&", data=payload).json()
        #print(response)
        token = response['token'] or token
        return convert_work(response["data"]), token
