from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/saludo/<nombre>')
def saludo(nombre):
    mensaje = f'Hola, {nombre}!'
    return render_template('saludo.html', message=mensaje)

@app.route('/cuadrado/<int:numero>')
def cuadrado(numero):
    res = numero**2
    return "El cuadrado de {} es {}".format(numero, res)

if __name__ == '__main__':
    app.run(debug=True)
