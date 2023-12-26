# a) Creación de Formularios:

# Flask-WTF es una extensión de Flask que integra WTForms, una biblioteca de formularios de Python. Comencemos con un ejemplo simple de creación de formulario.

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class MiFormulario(FlaskForm):
    nombre = StringField('Nombre')
    edad = IntegerField('Edad')
    enviar = SubmitField('Enviar')


# b) Uso en una Ruta de Flask:

# Ahora, en tu ruta de Flask, puedes renderizar el formulario y manejar las solicitudes.
from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'


@app.route('/formulario_ejemplo', methods=['GET', 'POST'])
def formulario_ejemplo():
    form = MiFormulario()

    if form.validate_on_submit():
        # Aquí manejas la lógica del formulario
        nombre = form.nombre.data
        edad = form.edad.data
        # ... (puedes almacenar estos datos en la base de datos, por ejemplo)
        return f'Nombre: {nombre}, Edad: {edad}'

    return render_template('formulario_ejemplo.html', form=form)


if  __name__ == '__main__':
    app.run(debug=True)