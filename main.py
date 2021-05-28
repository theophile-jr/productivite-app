from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    message = "Flask HTTP Server \n"
    return message


@app.route('/login')
def login():
    message = "Le login marche \n"
    return message


port = 3000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)