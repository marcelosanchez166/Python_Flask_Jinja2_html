from flask import Flask, render_template,redirect, url_for, request, flash 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meliodas1506@localhost/users'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'


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
            db.session.execute(text(f" INSERT INTO `usuario`(`Id`, `Nombre`) VALUES (NULL ,'{nombre}') "))
            db.session.commit()
            return redirect(url_for("listar"))
    else:
        return render_template('crear.html')



@app.route("/editar", methods=["GET", "POST"])
def editar():
    if request.method == "POST":
        datos = request.args.get('usuarios', '')
        print(datos)
        nombre = request.form["nombre"]
        ids = request.form["Ids"]

        if nombre is not None and ids is not None:
            count = db.session.execute(text(f"SELECT COUNT(*) FROM usuario WHERE Id = {ids}")).scalar()
            print(count)
            if count > 0:
                print("ID enviado desde el form y comparado con la consulta select ", ids)
                #Esta consulta cuenta los usuarios que tienen el id que es enviado desde el input del formulario
                db.session.execute(text("""UPDATE usuario SET Nombre = '{}' WHERE Id = '{}' """.format(nombre, ids)))
                db.session.commit()
                flash("Usuario agregado exitosamente", 'success')
                return redirect(url_for("listar"))
            else:
                flash("El usuario no existe", 'warning')
    else:
        return render_template("editar.html")
    


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        ids = request.form.getlist("Ids")
        print("IDS obtenidos del delete ",ids)
        # Eliminar los usuarios con los IDs seleccionados
        for user_id in ids:
            usuarios = db.session.execute(text("""DELETE FROM `usuario` WHERE Id = {}""".format(user_id)))
        db.session.commit()
        # Redirigir a la página de listar después de eliminar
    usuarios = db.session.execute(text("SELECT * FROM usuario"))
    usuarios = usuarios.fetchall()
    print(usuarios)
    return render_template('delete.html', usuarios=usuarios)        





if __name__ == '__main__':
    app.run(debug=True)
