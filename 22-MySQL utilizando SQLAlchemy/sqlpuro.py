from flask import Flask, request, redirect, flash,render_template, url_for
from flask_mysqldb import MySQL

class Config:#Clase que servira para tener la clave secreta que se pondra mas adelante en una instruccion
    SECRET_KEY="TWVsaW9kYXMxNTA2JCQ="#Esta es la clave secreta que la app va utilizar debe estar encriptada y servira para poder crear tokens personalizados para cada formulario y para cada peticion que se realice 



class DevelopmentConfig(Config):#clase que hereda de la clase Config y que activara el modo debug en true para que los cambios los tome en automatico el server
    MYSQL_HOST="localhost"
    MYSQL_USER="root"
    MYSQL_PASSWORD="Meliodas1506"
    MYSQL_DB="users"


app = Flask(__name__)
db=MySQL(app)#Declaro una variable que instanciara el conector de mysql y se le pasa la variable app que se creo para instanciar Flask(__name__) 
#sobre la cual va a tener efecto para que se pueda conectar a mysql y se usara para realizar conexiones atravez de los modelos, los modelos seran unas clases que se van a crear nos 
#permitira tener metodos para hacer CRUD registro de sesion etc que vamos a necesitar para conectarnos a una base


app.config.from_object(DevelopmentConfig)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_sqlalchemy')
def listar():
    cursor=db.connection.cursor()
    # Utiliza text() para declarar la expresión SQL
    usuarios = """SELECT * FROM usuario"""
    cursor.execute(usuarios)
    usuarios = cursor.fetchall()
    # for i in usuarios:
    #     print(i)
    print(usuarios)
    return render_template('index_sqlalchemy.html', usuarios=usuarios)



@app.route('/crear', methods=["GET","POST"])
def crear():
    cursor=db.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        if nombre != None:
            sql= f"INSERT INTO usuario(Id, Nombre) VALUES (NULL ,'{nombre}') "
            cursor.execute(sql)
            print
            return redirect(url_for("listar"))
    else:
        return render_template('crear.html')



@app.route("/editar", methods=["GET", "POST"])
def editar():
    cursor=db.connection.cursor()
    if request.method == "POST":
        datos = request.args.get('usuarios', '')
        print(datos)
        nombre = request.form["nombre"]
        ids = request.form["Ids"]

        if nombre is not None and ids is not None:
            #count = """SELECT COUNT(*) FROM usuario WHERE Id = {}""".format(ids)
            #print(type(count))
            #if int(count) > 0:
            print("ID enviado desde el form y comparado con la consulta select ", ids)
            #Esta consulta cuenta los usuarios que tienen el id que es enviado desde el input del formulario
            sql= """UPDATE usuario SET Nombre = '{}' WHERE Id = '{}' """.format(nombre, ids)
            cursor.execute(sql)
            flash("Usuario agregado exitosamente", 'success')
            return redirect(url_for("listar"))
            #else:
            #    flash("El usuario no existe", 'warning')
        return render_template('editar.html')
    else:
        return render_template("editar.html")
    


@app.route("/delete", methods=["GET", "POST"])
def delete():
    cursor=db.connection.cursor()
    if request.method == "POST":
        ids = request.form.getlist("Ids")
        print("IDS obtenidos del delete ",ids)
        # Eliminar los usuarios con los IDs seleccionados
        for user_id in ids:
            usuarios = """DELETE FROM `usuario` WHERE Id = {}""".format(user_id)
        cursor.execute(usuarios)
        # Redirigir a la página de listar después de eliminar
    usuarios = """SELECT * FROM usuario"""
    usuarios = cursor.fetchall()
    print(usuarios)
    return render_template('delete.html', usuarios=usuarios)        





if __name__ == '__main__':
    app.run(debug=True)
