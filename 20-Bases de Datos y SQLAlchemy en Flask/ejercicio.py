# Ejercicio: Intenta agregar una nueva ruta, por ejemplo, /usuarios, que muestre la lista de usuarios almacenados en la base de datos.

# Bases de Datos y SQLAlchemy:
# Flask se integra fácilmente con bases de datos. Vamos a utilizar SQLAlchemy, que es un ORM (Mapeo Objeto-Relacional)
# para interactuar con bases de datos de una manera más orientada a objetos.

# Primero, instala SQLAlchemy:
# pip install Flask-SQLAlchemy


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Importa la clase datetime para manejar fechas


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite como ejemplo
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)  # Nueva columna



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
    return render_template('cuadrado.html', message=mensaje)


@app.route('/usuarios')
def ver_usuarios():
    usuarios = Usuario.query.all()
    #query = "SELECT * FROM Usuario"
    #db.session.commit()
    return render_template('usuarios.html', lista_usuarios=usuarios)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos
    # print(app.url_map)
    app.run(debug=True)
