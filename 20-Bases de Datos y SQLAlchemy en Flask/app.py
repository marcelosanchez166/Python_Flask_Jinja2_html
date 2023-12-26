# Bases de Datos y SQLAlchemy:
# Flask se integra fácilmente con bases de datos. Vamos a utilizar SQLAlchemy, que es un ORM (Mapeo Objeto-Relacional) 
# para interactuar con bases de datos de una manera más orientada a objetos.

# Primero, instala SQLAlchemy:
# pip install Flask-SQLAlchemy


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite como ejemplo
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    numero = db.Column(db.Integer, nullable=False)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/formulario', methods=['GET', 'POST'])
def procesar_formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        numero = int(request.form['numero'])

        # Guardar en la base de datos
        nuevo_usuario = Usuario(nombre=nombre, numero=numero)
        db.session.add(nuevo_usuario)
        db.session.commit()

        res = numero ** 2
        mensaje = 'Bienvenido {}, el cuadrado del número {} que ingresó es {}: '.format(nombre, numero, res)
        return redirect(url_for('cuadrado', numero=numero, message=mensaje))
    return render_template('formulario.html')

@app.route('/cuadrado/<int:numero>')
def cuadrado(numero):
    # Recuperar el mensaje de la variable de consulta 'message'
    mensaje = request.args.get('message', '')
    print(mensaje)
    return render_template('cuadrado.html', message=mensaje)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos
    app.run(debug=True)
