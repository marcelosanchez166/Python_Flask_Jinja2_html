# Sesiones en Flask:
# Las sesiones son un mecanismo para almacenar datos del usuario entre solicitudes. Flask utiliza cookies para gestionar las sesiones de forma predeterminada, 
# y puedes acceder a la sesión desde el objeto request.


# Ejemplo de Sesiones en Flask:
# Vamos a crear un ejemplo simple donde almacenaremos el nombre del usuario en la sesión y lo mostraremos en diferentes rutas.

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

@app.route('/')
def index():
    return 'Hola, visita la página <a href="/saludo">Saludo</a>'


# print(type(session),"tipo de la session")

@app.route('/saludo', methods=['GET', 'POST'])
def saludo():
    if request.method == 'POST':
        nombre = request.form['name']
        session['clave'] = nombre #En la clave name del objeto sesion se guarda el nombre del usuario que se obtiene del formulario cuando lo envia
        return redirect(url_for('saludo'))
    return render_template('saludo.html', nombre_session=session.get('clave'))#El parametro name que se le pasa al session.get es la clave que se guardo en el objeto session['clave'] 
                                                                             #para poder mostrarlo en la plantilla html.


if __name__ == '__main__':
    app.run(debug=True)

# Este ejemplo muestra cómo se puede almacenar y recuperar información de la sesión en Flask.