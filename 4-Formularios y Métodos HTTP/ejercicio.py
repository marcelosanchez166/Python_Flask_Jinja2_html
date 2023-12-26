# Ejercicio: Mejora el formulario para que también solicite un número y, al enviar el formulario, redirija a la ruta /cuadrado/numero con el nombre y el cuadrado del número.


from flask import Flask, request, render_template, redirect, url_for

app =Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/formulario', methods=['GET', 'POST'])
def procesar_formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = int(request.form['numero'])
        res = numero**2
        mensaje = 'Bienvenido {}, el cuadrado del numero {} que ingreso es {} : '.format(nombre, numero, res)
        return redirect(url_for('cuadrado',numero=numero, message=mensaje))
    return render_template('formulario.html')


@app.route('/cuadrado/<int:numero>')
def cuadrado(numero):
    # Recuperar el mensaje de la variable de consulta 'message'
    mensaje = request.args.get('message', '')
    return render_template('cuadrado.html', message=mensaje)



if __name__ == '__main__':
    app.run(debug=True)