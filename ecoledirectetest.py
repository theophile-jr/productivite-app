from getpass import getpass
import locale

from requests import request as req
from rich import print
from rich.console import Console
from rich.table import Table
import inquirer

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
console = Console()


def calm_exit():
    console.input(password=True)
    exit()

# Crée un menu de sélection


def choose(message: str, choices: list):
    questions = [
        inquirer.List('a', message, choices)
    ]
    answer = inquirer.prompt(questions)['a']
    return answer


# Se connecte à EcoleDirecte
def login(username: str, password: str, token: str = None):
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


# Sélectionne ou demande le compte à retourner
def select_account(accounts: list):
    # Filtre les comptes de type E
    e_accounts = list(filter(lambda account: bool(
        account['typeCompte'] == "E"), accounts))
    # Met en page les choix
    choices = list(
        map(lambda account: (str(account['id']) + " | " + account['prenom'] + " " + account['nom']),
            e_accounts))
    # Choix automatique
    choice = None
    if len(choices) > 1:
        choice = choose("Sélectionnez un compte disponible: ", choices=choices)
    elif len(choices) < 1:
        choice = None
    elif len(choices) == 1:
        choice = choices[0]
    if not choice:
        # Pas de compte supporté
        print("[reverse bold red]Aucun compte compatible trouvé[/]")
        print("[red]Essayez de vous connecter avec un compte Elève.[/]")
        calm_exit()

    account = next(filter(lambda account: (
        str(account['id']) == choice[0:4]), e_accounts))
    return account


# Récupère les notes
def fetch_work(account, token: str):
    payload = 'data={"token": "' + token + '"}'
    response = req("POST", "https://api.ecoledirecte.com/v3/Eleves/" +
                   str(account['id']) + "/cahierdetexte.awp?verbe=get&", data=payload).json()
    #print(response)
    token = response['token'] or token
    return response, token
#https://api.ecoledirecte.com/v3/Eleves/6097/cahierdetexte.awp?verbe=get&
#https://api.ecoledirecte.com/v3/Eleves/6097/cahierdetexte/2021-06-08.awp?verbe=get&

def handle_work(data):
    for task in data.items():
        print(task)


def main():
    username = input("Identifiant: ")
    password = getpass("Mot de passe: ")
    print("Connexion...")
    loginRes, token = login(username, password)
    if not token:
        print(loginRes['message'])
        calm_exit()

    account = select_account(loginRes['data']['accounts'])
    print(f"[blue]Bonjour, [bold]{account['prenom']}[/].[/]")

    WorkRes, token = fetch_work(account, token)
    print(WorkRes['code'])
    if WorkRes['code'] != 200:
        print(WorkRes['message'])
        calm_exit()
    handle_work(WorkRes['data'])
    print("[reverse green]Terminé.[/] Pressez [reverse]ENTER[/] pour quitter.")
    calm_exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
