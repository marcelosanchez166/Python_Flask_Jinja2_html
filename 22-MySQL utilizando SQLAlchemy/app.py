from flask import Flask, render_template,redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meliodas1506@localhost/users'
db = SQLAlchemy(app)
#app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_sqlalchemy')
def listar():
    # Utiliza text() para declarar la expresión SQL
    usuarios = db.session.execute(text("SELECT * FROM usuario"))
    usuarios = usuarios.fetchall()
    print(usuarios)
    return render_template('index_sqlalchemy.html', usuarios=usuarios)


@app.route('/crear', methods=["GET","POST"])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if nombre != None:
            nuevo_usuario = db.session.execute(text(f" INSERT INTO `usuario`(`Id`, `Nombre`) VALUES (NULL ,'{nombre}') "))
            db.session.commit()
            return redirect(url_for("listar"))
    else:
        return render_template('crear.html')



@app.route("editar", methods=["GET", "POST"])
def editar():
    if request.method == "POST":
        id = int(request.args.get('id'))




if __name__ == '__main__':
    app.run(debug=True)
