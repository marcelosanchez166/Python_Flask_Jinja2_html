# Ejercicio: Crea una nueva plantilla HTML llamada cuadrado.html que reciba el número y su cuadrado como argumentos y los muestre de una manera más estilizada.


from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/saludo/<nombre>')
def saludo(nombre):
    mensaje = 'Hola {}'.format(nombre)
    return render_template('saludo.html', message=mensaje)


@app.route('/cuadrado/<int:numero>')
def cuadrado(numero):
    res = 'el cuadrado de {}, es {}'.format(numero, numero**2)
    return render_template('cuadrado.html', message=res)

if __name__ == "__main__":
    app.run(debug=True)