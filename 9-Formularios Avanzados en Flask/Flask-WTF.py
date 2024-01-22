# Vamos a introducir Flask-WTF, una extensión de Flask que integra el paquete WTForms para facilitar la creación y validación de formularios.

# Trabajando con Formularios Avanzados en Flask
# Instalación de Flask-WTF:
# Antes de comenzar, asegúrate de tener Flask-WTF instalado. Puedes instalarlo usando el siguiente comando:
# pip install Flask-WTF

"""Uso de Flask-WTF en tu Aplicación:
Importa las clases necesarias en tu archivo de aplicación (app.py)."""
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = "ajsdahdujj123123123"   


""""Creación de Formularios:
Crea una clase para cada formulario que desees utilizar. Por ejemplo:"""
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


"""Manejo de Formularios en Rutas:
Utiliza el formulario en tus rutas para procesar y validar los datos del formulario. Por ejemplo:"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Acciones a realizar cuando el formulario se envía correctamente
        email = form.email.data
        password = form.password.data
        return f"Bienvenido usuario {email}"
        # Realizar autenticación u otras acciones según sea necesario
    return render_template('form.html', form=form)


"""Personalización de Formularios:
Puedes personalizar la apariencia y el comportamiento de los formularios utilizando las clases y funciones proporcionadas por WTForms y Flask-WTF."""


if __name__ == "__main__":
    app.run(debug=True)