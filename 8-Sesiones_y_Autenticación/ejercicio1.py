from flask import Flask,render_template, redirect, session, url_for, request

app = Flask(__name__)

app.config["SECRET_KEY"] = "12312431412dadfad"


# Lista de usuarios (en un entorno de producción, usaríamos una base de datos)
usuarios = {'usuario1': 'clave1', 'usuario2': 'clave2'}

@app.route('/')
def index():
    if 'usuario' in session:#Aqui pregunta si la clave usuario esta en la session creada
        return f'Hola, {session["usuario"]}! <a href="/logout">Cerrar sesión</a>'#Aqui mostrara el nombre de usuario tomandolo desde la clave que se guardo en la sesion y a la par mostrara un mensaje para cerrar la sesion que llama a la funcion logout que esta mas abajo en el codigo 
    return 'Bienvenido. <a href="/login">Iniciar sesión</a>, <a href="/crear_cuentas">crear cuenta</a>'

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


@app.route("/crear_cuentas", methods=["GET", "POST"])
def crear_cuenta():
    if request.method=="POST": #Si el formulario envia los valores del formulario mediante POST entonces guardara los valores en la variables asignadas
        email = request.form["email"]
        password = request.form["password"]
        usuarios[email] = password
        print(usuarios)
        return 'Cuenta Creada! <a href="/login">Iniciar sesión</a>'

    else: #Devuelve el html para poder rellenar el formulario
        return render_template("registro_usuarios.html")



print(usuarios)



if __name__ == '__main__':
    app.run(debug=True)