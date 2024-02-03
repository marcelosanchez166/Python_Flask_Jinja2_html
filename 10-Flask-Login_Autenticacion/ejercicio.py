from flask import Flask, flash, session, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash #Importando los metodos para encriptar y desencriptar las passwords, metodo para desencriptar(check_password_hash),metodo para encriptar(generate_password_hash)
import env

app =Flask(__name__)


"""Impoertando los Blueprint"""
from routes.delete import deletes


app.config["SECRET_KEY"] = "12313213nb12j3b123bg21"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Meliodas1506@localhost/prueba"
db=SQLAlchemy(app)

login_manager = LoginManager(app)#instanciando el metodo LoginManager para poder hacer uso de el mediante la variable donde se instancio
print(login_manager, "imprimiendo login manager")
login_manager.login_view = 'login'


#UserMixin es necesario para autenticar al usuario, es necesario para mantener la sesion, 
#Clase para crear la tabla en la base de datos que se definio en la app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Meliodas1506@localhost/prueba"
class Usuario(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    

class RegisterUser(FlaskForm):#Clase para crear el formulario RegisterUser con FlaskForm 
    name = StringField("Nombre", validators=[DataRequired(),Length(min=3)])
    password = StringField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Register User")
                                                                   

class LoginUser(FlaskForm):#Clase para crear el formulario LoginUser con FlaskForm 
    name = StringField('Nombre', validators=[DataRequired(), Length(min=3)])
    password = StringField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Login")


#se utiliza para cargar un usuario de la base de datos a partir de su ID almacenado en la sesión. Esta función debe ser 
#implementada para permitir que Flask-Login administre la sesión del usuario.
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route("/")
def index():
    return redirect("login")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUser()
    if request.method == "POST" and form.validate_on_submit():
        name=form.name.data
        password=form.password.data
        encriptado = generate_password_hash(password, method='pbkdf2:sha256')
        # coincide = check_password_hash(user.password, password)
        print(encriptado)
        if name and password !=None:
            user = Usuario.query.filter_by(name=name).first()
            if user and check_password_hash(user.password, password):
                if user:
                    login_user(user)
                    flash('Inicio de sesión exitoso', 'success')
                    return redirect(url_for('store'))
                else:
                    flash('Usuario o contraseña incorrectos', 'danger')
        
    return render_template('login_ejercicio.html', form=form)
   

@app.route("/register", methods=["GET","POST"])
def register_user():
    form = RegisterUser()
    if request.method == "POST" and form.validate_on_submit() :
        name = form.name.data
        password = form.password.data
        password=generate_password_hash(password, method='pbkdf2:sha256')
        new_user = Usuario(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return  redirect(url_for("login"))
    else:
        return render_template("register.html",form=form)        


@app.route("/store", methods=["GET"])
@login_required
def store():
    if current_user.is_authenticated:
        # Accede a la sesión del usuario
        user_name = current_user.name
        return  render_template("store.html", user=user_name)
 

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
    app.register_blueprint(deletes)
    app.run(debug=True)