"""Uso de Flask-WTF en tu Aplicación:
Importa las clases necesarias en tu archivo de aplicación (app.py)."""
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, RadioField,BooleanField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "ajsdahdujj123123123"   
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meliodas1506@localhost/prueba'


db = SQLAlchemy(app)

class prueba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class registro_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(25), nullable=False)
    direccion = db.Column(db.String(300), nullable=False)
    telefono = db.Column(db.Integer, nullable=False) 

""""Creación de Formularios:
Crea una clase para cada formulario que desees utilizar. Por ejemplo:"""
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


""""Creación de Formularios:
Crea una clase para cada formulario que desees utilizar. Por ejemplo: formulario de registro"""
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    nombre = StringField('Nombre',validators=[DataRequired()] )
    apellido = StringField("apellido", validators=[DataRequired()])
    edad = IntegerField("Edad", validators=[DataRequired()])
    genero = RadioField("Genero",choices=[("H","Hombre"), ("M", "Mujer")], validate_choice=[DataRequired()])
    direccion = StringField('Direccion' , validators=[DataRequired()])
    telefono = IntegerField("Telefono", validators=[DataRequired()])
    submit = SubmitField('Registro')


"""Manejo de Formularios en Rutas:
Utiliza el formulario en tus rutas para procesar y validar los datos del formulario. Por ejemplo:"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        
        if form.validate_on_submit():
            # Acciones a realizar cuando el formulario se envía correctamente
            email = form.email.data
            password = form.password.data
            # return f"Bienvenido usuario {email}"
            if email and password !=None:
                # Realizar autenticación consultando la base de datos
                user = registro_user.query.filter_by(email=email, password=password).first()
                if user:
                    return f'Bienvenido usuario {email}  <a href="/registro">Desea agregar otro usuario?</a>'
                else:
                    return "Usuario o contraseña incorrectos"
    return render_template('form.html', form=form)


@app.route('/registro',  methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        form = RegisterForm()
    
        if form.validate_on_submit():
            # Guarda los datos en la base de datos o realiza alguna acción
            email = form.email.data
            password = form.password.data
            nombre = form.nombre.data
            apellido = form.apellido.data
            edad = form.edad.data
            genero = form.genero.data
            direccion = form.direccion.data
            telefono = form.telefono.data

            if email and password and nombre and apellido and edad and genero and direccion and telefono != None:
                    # Utilizar SQLAlchemy para insertar el nuevo usuario
                    nuevo_usuario = registro_user(email=email, password=password, nombre=nombre, apellido=apellido, edad=edad, genero=genero, direccion=direccion, telefono=telefono )
                    db.session.add(nuevo_usuario)
                    db.session.commit()
                    return redirect(url_for('login'))
            else:
                render_template("registro.html", form=form)

        return render_template("registro.html", form=form)
    else:
        form = RegisterForm()
        return render_template('registro.html', form=form)






class EditarFormulario(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    nombre = StringField('Nombre')
    submit = SubmitField('Guardar Cambios')


@app.route('/editar/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):

    usuario = registro_user.query.get_or_404(user_id)
    print(usuario)
    form = EditarFormulario(obj=usuario)#El parametro obj=usuario se utiliza para prellenar el formulario cuando se va actualizar esto si la consulta de arriba devuelve algun valor

    if form.validate_on_submit():
        form.populate_obj(usuario)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('editar.html', form=form)


class EliminarFormulario(FlaskForm):
    submit = SubmitField('Eliminar Usuario')


@app.route('/eliminar/<int:user_id>', methods=["GET",'POST'])
def eliminar_usuario(user_id):
    usuario = registro_user.query.get_or_404(user_id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('login'))


"""Personalización de Formularios:
Puedes personalizar la apariencia y el comportamiento de los formularios utilizando las clases y funciones proporcionadas por WTForms y Flask-WTF."""

#Contexto para que cuando se ejecute la aplicacion pueda crear la tabla con los atributos y si ya existe no la crea
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)