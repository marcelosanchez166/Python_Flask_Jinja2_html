# Sesiones en Flask:
# Las sesiones en Flask son instancias de la clase Session. Puedes acceder a la sesión desde el objeto request y session desde el objeto g (contexto global).

# Configuración Básica:
# Antes de usar sesiones, necesitas configurar una clave secreta para tu aplicación Flask. Esta clave se utiliza para firmar las cookies de sesión
# y protegerlas contra manipulaciones externas. Agrega la siguiente línea a tu aplicación:

from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'



# Almacenar Datos en la Sesión:
# Puedes almacenar datos en la sesión de la siguiente manera:
# En este ejemplo, la clave 'usuario' se almacena en la sesión con el valor 'ejemplo_usuario'.
@app.route('/')
def sett_session():
    session['usuario'] = 'ejemplo_usuario'
    return 'Datos almacenados en la sesión.'




# Recuperar Datos de la Sesión:
# Para recuperar datos de la sesión, simplemente accede a la clave correspondiente:
# En este caso, si la clave 'usuario' está presente en la sesión, se recupera su valor. De lo contrario, se devuelve 'Invitado'.
@app.route('/obtener')
def get_session():
    usuario = session.get('usuario', 'Invitado')
    return f'Bienvenido, {usuario}.'


# Eliminar Datos de la Sesión:
# Puedes eliminar datos de la sesión utilizando el método pop o del:
# Esto elimina la clave 'usuario' de la sesión si existe.
@app.route('/eliminar')
def delete_session():
    # Eliminar la clave 'usuario' de la sesión si existe
    session.pop('usuario', None)
    return 'Datos eliminados de la sesión.'


# Cerrar Sesión (Logout):
# Para cerrar la sesión (logout), simplemente elimina todas las claves de la sesión:
@app.route('/cerrar_sesion')
def logout():
    session.clear()  # Eliminar todas las claves de la sesión
    return 'Sesión cerrada.'


@app.route('/index')
def index():
    return 'Hola, visita la página <a href="/saludo">Saludo</a>'


# print(type(session),"tipo de la session")

@app.route('/saludo', methods=['GET', 'POST'])
def saludo():
    if request.method == 'POST':
        nombre = request.form['name']
        session['usuario'] = nombre #En la clave name del objeto sesion se guarda el nombre del usuario que se obtiene del formulario cuando lo envia
        return redirect(url_for('saludo'))
    return render_template('saludo.html', nombre_session=session.get('usuario'))#El parametro name que se le pasa al session.get es la clave que se guardo en el objeto session['clave'] 
                                                                             #para poder mostrarlo en la plantilla html.





if __name__ == '__main__':
    app.run(debug=True)
