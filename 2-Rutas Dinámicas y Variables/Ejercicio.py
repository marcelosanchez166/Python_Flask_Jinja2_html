# Ejercicio: Crea una nueva ruta que tome un número como variable y devuelva su cuadrado. Por ejemplo, /cuadrado/5 debería devolver "El cuadrado de 5 es 25".


from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return f'Hola, {nombre}!'

@app.route('/cuadrado/<int:numero>')
def cuadrado(numero):
    res = numero**2 
    return "El cuadrado de {} es {}".format(numero, res)

if __name__ == '__main__':
    app.run(debug=True)