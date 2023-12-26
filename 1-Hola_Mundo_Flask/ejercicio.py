# Ejercicio: Modifica el código para que la ruta sea /saludo y el mensaje sea "Hola, bienvenido al mundo de Flask!"

from flask import Flask

app = Flask(__name__)

@app.route('/saludo')
def hello_world():
    return "Hola, bienvenido al mundo de Flask!"


if __name__ == '__main__':
    app.run(debug=True)