from requests import request as req
from flask_login import current_user
from werkzeug.security import generate_password_hash
from . import db

class EcoleDirecte():

    def login(username, password):
        payload = 'data={ "identifiant": "' + username + \
                '", "motdepasse": "' + password + '", "acceptationCharte": true }'
        try:
            response = req(
                "POST", "https://api.ecoledirecte.com/v3/login.awp", data=payload).json()
            print(payload)
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