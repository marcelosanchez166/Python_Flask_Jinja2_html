from flask import Flask,render_template, redirect, session, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SECRET_KEY"] = "12312431412dadfad"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meliodas1506@localhost/prueba'

db = SQLAlchemy(app)

class prueba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


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


@app.route('/crear_cuentas', methods=["GET", "POST"])
def crear():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form["password"]
        if email and password:
            try:
                # Utilizar SQLAlchemy para insertar el nuevo usuario
                nuevo_usuario = prueba(email=email, password=password)
                db.session.add(nuevo_usuario)
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                # Manejar errores de manera adecuada (por ejemplo, loggear el error)
                return render_template('error.html', error=str(e))
        return redirect(url_for("login"))
    else:
        return render_template('registro_usuarios.html')



with app.app_context():
    db.create_all()  # Crear las tablas en la base de datos
print(usuarios)



if __name__ == '__main__':

    app.run(debug=True)