from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/formulario', methods=['GET', 'POST'])
def procesar_formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        return f'Hola, {nombre}!'
    return render_template('formulario.html')


@app.route('/cuadrado/<int:numero>')
def cuadrado(numero):
    res = 'El cuadrado de {}, es {}'.format(numero, numero**2)
    return render_template('cuadrado.html', message=res)


if __name__ == '__main__':
    app.run(debug=True)
    

# Explicación : methods=['GET', 'POST'] en @app.route('/formulario', methods=['GET', 'POST']) indica que esta ruta acepta tanto solicitudes GET como POST
# El nombre de la funcion es la que le paso en la plantilla action="{{ url_for('procesar_formulario') }}" para que pueda llamar y mostrar renderizado lo que debe de mostrar 