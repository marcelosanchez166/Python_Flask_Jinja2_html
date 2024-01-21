# Autenticación Básica:
# La autenticación es un aspecto fundamental de muchas aplicaciones web. Vamos a implementar una autenticación básica utilizando sesiones y una simple lista de usuarios.

# Ejemplo de Autenticación Básica:


from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

# Lista de usuarios (en un entorno de producción, usaríamos una base de datos)
usuarios = {'usuario1': 'clave1', 'usuario2': 'clave2'}

@app.route('/')
def index():
    if 'usuario' in session:#Aqui pregunta si la clave usuario esta en la session creada
        return f'Hola, {session["usuario"]}! <a href="/logout">Cerrar sesión</a>'#Aqui mostrara el nombre de usuario tomandolo desde la clave que se guardo en la sesion y a la par mostrara un mensaje para cerrar la sesion que llama a la funcion logout que esta mas abajo en el codigo 
    return 'Bienvenido. <a href="/login">Iniciar sesión</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if usuario in usuarios and usuarios[usuario] == clave:
            session['usuario'] = usuario
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


# Este ejemplo muestra cómo implementar una autenticación básica con Flask.

