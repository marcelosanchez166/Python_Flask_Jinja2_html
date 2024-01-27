from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager,  login_user, login_required, logout_user,current_user
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect #libreria para poder crear tokens esta se instalo con pip y generaremos tokens personalizados con la SECRET_KEY que creamos en el archivo config.py
from werkzeug.security import check_password_hash, generate_password_hash

from configDB import DevelopmentConfig



from models.entities.usuario import Usuario
from models.modelo_usuario import ModeloUsuario

"""Impoertando los Blueprint"""
# from routes.register import register_user

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


login_manager_app=LoginManager(app)#creamos una variable que hara uso de LoginManager y le pasamos la variable app que hace referencia a nuestra propia app, LoginManager sirve para poder crear un administrador para nuestra app 


#Existe un ataque a formularios que se llama CSRF(Cross-site Request Forgery) (Solicitud de Falsificacion entre sitios) 
#que se enfoca en realizar peticiones al formulario que no son de nuestro sitio
"""Para evitar estos ataques podemos usar una herramienta que nos da Flask que se llama WTF que se instala con pip install Flask-WTF, con esto realizaremos es que cada 
vez que tengamos un formulario vamos a crear un token para identificarnos como los que estamos realizando las peticiones a nuestra aplicacion"""
csrf=CSRFProtect()


db=MySQL(app)#Declaro una variable que instanciara el conector de mysql y se le pasa la variable app que se creo para instanciar Flask(__name__) 
#sobre la cual va a tener efecto para que se pueda conectar a mysql y se usara realizar conexiones atravez de los modelos, los modelos seran unas clases que se van a crear nos 
#permitira tener metodos para hacer CRUD registro de sesion etc que vamos a necesitar para conectarnos a una base


@login_manager_app.user_loader #Se debe implementar para que se gestionen correctamente las sesiones atravez de la libreria flask_login Si no creamos el decorador login_manager_app dara este error Exception: Missing user_loader or request_loader. Refer to http://flask-login.readthedocs.io/#how-it-works for more info. cuando estemos usando login_user y Login_Manager de flask
def load_user(id):#Se crear la funcion load_user y se le pasa el id que vamos a cargar del usuario
    print("Id de la funcion loginmanager",id)
    return ModeloUsuario.obtener_por_id(db, id) #retornamos el metodo obtener_por_id de la clase ModeloUsuario del archivo modelousuario.py y se le pasaran dos valores la conexion a la base y el id que vamos a cargar del usuario



@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(password,"Imprimiendo lo que se le envia desde el formulario en la password")
        #encriptado = generate_password_hash(password, method='pbkdf2:sha256')
        usuario = Usuario(None, username, password, None )
        #usuario = Usuario(None, request.form["username"], request.form["password"], None )
        print(usuario.password, "dato de la password cuando se crea la instancia", usuario.username)
        usuario_logueado=ModeloUsuario.login(db, usuario)
        print("Usuario logueado en app", usuario_logueado)
        if  usuario_logueado !=  None:
                login_user(usuario_logueado)#Utilizando el modulo logQin_user de flask para poder loguear al usuario que se devuelve como inicio de sesion exitoso sirve para ver la sesion del usuario que se ha logueado
                print("Ingresando al index porque el logue fue exitoso" )
                print("usuario actual de", usuario_logueado )
                return redirect( url_for( "task"))#El render_template tambien sirve para dirigir a otra plantilla pero cuando pero para este caso es mejor el redirect ya que funciona como redireccionamiento
        else:
            flash("Usuario o Contrasena incorrectos", "warning")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        password = generate_password_hash(password)
        email = request.form["email"]
        print(username, password, email, "lo que se envia en el formulario \n")
        usuario = Usuario(None, username, password, email)
        print(usuario.username, usuario.password, usuario.email, "lo que se le envia a la clase USUARIO \n")
        user_register = ModeloUsuario.RegisterUser(db, usuario)
        print("Hola",user_register, "lo que se le envia a la clase MODELOUSUARIO con el Metodo REgisterUser \n")
        if user_register is not None:

            flash('User successfully registered', 'success')
            return redirect(url_for('login'))
        else:
            flash('error registering user', 'warning')
            return render_template('register.html')
    return render_template("register.html")


@app.route("/task")
@login_required
def task():
    print("usuario autenticado desde task ", current_user.is_authenticated )
    if current_user.is_authenticated:#PReguntamos si el usuario esta autenticado si esta autenticado lo redirije haci la plantilla index.html
        print("Entrando a html task")
        return render_template("task.html")
    else:#Si no esta logueado el usuario lo rederijira hacia la ruta login para que se pueda loguear
        return redirect(url_for('login'))


# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))


if __name__ == "__main__":
    # app.register_blueprint(register_user)
    app.run(debug=True, host="0.0.0.0", port="5001")