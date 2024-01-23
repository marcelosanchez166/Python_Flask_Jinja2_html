#  La autenticación es un componente crucial para la mayoría de las aplicaciones web, ya que permite a los usuarios acceder a funciones personalizadas y garantiza 
# la seguridad de la información.

# La autenticación suele involucrar la verificación de las credenciales del usuario, como el nombre de usuario y la contraseña. 
# Flask proporciona herramientas y extensiones, y usaremos Flask-Login para gestionar la autenticación de usuarios.

# Vamos a revisar cómo implementar un sistema de autenticación básico con Flask-Login. Comencemos con la instalación de la extensión. 
# Puedes hacerlo ejecutando el siguiente comando en tu entorno virtual:

"""pip install Flask-Login"""


from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config["SECRET_KEY"] = "tu_clave_secreta_aqui"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meliodas1506@localhost/prueba'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Definir el modelo de usuario, Asi se llamara la tabla que se creara cuando la aplicacion se ejecute la primera vez si no esta creada la crea y si ya esta creada no hara nada
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Configuración de Flask-Login
    """@login_manager.user_loader: Esto es un decorador proporcionado por Flask-Login. Le dice a Flask-Login que la siguiente función (load_user) debe usarse para cargar usuarios.
def load_user(user_id):: Esta función toma un argumento user_id, que es el ID del usuario almacenado en la sesión. Flask-Login usa este ID para cargar el usuario correspondiente.
return User.query.get(int(user_id)): Dentro de la función, se utiliza User.query.get() para obtener el usuario de la base de datos basándose en su ID. 
User es la clase de modelo de usuario que has definido en tu aplicación. query.get() busca un usuario por su clave primaria (ID, en este caso). 
El int(user_id) es necesario porque el ID generalmente se almacena como una cadena en la sesión, y necesitas convertirlo a un entero para buscarlo en la base de datos."""
# la función user_loader se utiliza para cargar un usuario de la base de datos a partir de su ID almacenado en la sesión. 
#Esta función debe ser implementada para permitir que Flask-Login administre la sesión del usuario.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Formulario de inicio de sesión
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')


# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        #session['usuario'] = username #En la clave name del objeto sesion se guarda el nombre del usuario que se obtiene del formulario cuando lo envia
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)


# Ruta para el perfil del usuario (requiere inicio de sesión)
@app.route('/profile')
@login_required
def profile():
    return f'Bienvenido, {current_user.username}! <a href="/logout">Cerrar sesión</a>'


# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)


# Este código establece una autenticación de usuario básica utilizando Flask-Login. Siéntete libre de adaptarlo según las necesidades específicas de tu aplicación. 
# La ruta /login maneja el inicio de sesión, /profile muestra el perfil del usuario (requiere inicio de sesión), y /logout cierra la sesión del usuario.

