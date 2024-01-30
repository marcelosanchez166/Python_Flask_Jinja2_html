from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager,  login_user, login_required, logout_user,current_user
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect #libreria para poder crear tokens esta se instalo con pip y generaremos tokens personalizados con la SECRET_KEY que creamos en el archivo config.py
from werkzeug.security import check_password_hash, generate_password_hash

from configDB import DevelopmentConfig



from models.entities.usuario import Usuario
from models.modelo_usuario import ModeloUsuario


from models.entities.tareas import Tareas
from models.modelo_tareas import ModeloTareas

"""Impoertando los Blueprint"""
# from routes.register import register_user

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


login_manager_app=LoginManager(app)#creamos una variable que hara uso de LoginManager y le pasamos la variable app que hace referencia a nuestra propia app, LoginManager 
#sirve para poder crear un administrador para nuestra app 


#Existe un ataque a formularios que se llama CSRF(Cross-site Request Forgery) (Solicitud de Falsificacion entre sitios) 
#que se enfoca en realizar peticiones al formulario que no son de nuestro sitio
"""Para evitar estos ataques podemos usar una herramienta que nos da Flask que se llama WTF que se instala con pip install Flask-WTF, con esto realizaremos es que cada 
vez que tengamos un formulario vamos a crear un token para identificarnos como los que estamos realizando las peticiones a nuestra aplicacion"""
csrf=CSRFProtect()


db=MySQL(app)#Declaro una variable que instanciara el conector de mysql y se le pasa la variable app que se creo para instanciar Flask(__name__) 
#sobre la cual va a tener efecto para que se pueda conectar a mysql y se usara realizar conexiones atravez de los modelos, los modelos seran unas clases que se van a crear nos 
#permitira tener metodos para hacer CRUD registro de sesion etc que vamos a necesitar para conectarnos a una base


@login_manager_app.user_loader #Se debe implementar para que se gestionen correctamente las sesiones atravez de la libreria flask_login Si no creamos el decorador login_manager_app dara este error Exception: Missing user_loader or request_loader. Refer to http://flask-login.readthedocs.io/#how-it-works for more info. cuando estemos usando login_user y Login_Manager de flask
def load_user(id):#Se crear la funcion load_user y se le pasa el id que vamos a cargar del usuario
    print("Id de la funcion loginmanager",id)
    return ModeloUsuario.obtener_por_id(db, id) #retornamos el metodo obtener_por_id de la clase ModeloUsuario del archivo modelousuario.py y se le pasaran dos valores la conexion a la base y el id que vamos a cargar del usuario



@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(password,"Imprimiendo lo que se le envia desde el formulario en la password")
        #encriptado = generate_password_hash(password, method='pbkdf2:sha256')
        usuario = Usuario(None, username, password, None )
        #usuario = Usuario(None, request.form["username"], request.form["password"], None )
        print(usuario.password, "dato de la password cuando se crea la instancia", usuario.username)
        usuario_logueado=ModeloUsuario.login(db, usuario)
        print("Usuario logueado en app", usuario_logueado)
        if  usuario_logueado !=  None:
                login_user(usuario_logueado)#Utilizando el modulo logQin_user de flask para poder loguear al usuario que se devuelve como inicio de sesion exitoso sirve para ver la sesion del usuario que se ha logueado
                print("Ingresando al index porque el logue fue exitoso" )
                print("usuario actual de", usuario_logueado )
                return redirect( url_for( "task"))#El render_template tambien sirve para dirigir a otra plantilla pero cuando pero para este caso es mejor el redirect ya que funciona como redireccionamiento
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        #password = generate_password_hash(password)
        email = request.form["email"]
        print(username, password, email, "lo que se envia en el formulario \n")
        usuario_re = Usuario(None, username, password, email)
        print(usuario_re.username, usuario_re.password, usuario_re.email, "lo que se le envia a la clase USUARIO \n")
        user_register = ModeloUsuario.RegisterUser(db, usuario_re)
        print("Hola",user_register, "lo que se le envia a la clase MODELOUSUARIO con el Metodo REgisterUser \n")
        if user_register  is not None:
            flash('User successfully registered', 'success')
            return redirect(url_for('login'))
        else:
            flash('error registering user', 'warning')
            return render_template('register.html')
    return render_template("register.html")


@app.route("/task", methods=["GET", "POST"])
@login_required
def task():
    print("usuario autenticado desde task ", current_user.is_authenticated )
    if current_user.is_authenticated:#PReguntamos si el usuario esta autenticado si esta autenticado lo redirije haci la plantilla index.html
        cursor = db.connection.cursor()
        sql = """SELECT id FROM usuarios WHERE id = '{}'""".format(current_user.id)
        cursor.execute(sql)
        data = cursor.fetchone()
        if request.method == "POST":
            nombre_tarea = request.form["tarea"]
            print(data[0], "Id del seletc de la funcion task")
            new_task = Tareas(None, nombre_tarea, "Pending", data[0])
            # print("Metodo STR de Tareas", new_task.id_usuario, new_task.estado, new_task.nombre_tarea, new_task.id)
            # send_task  = ModeloTareas.add_tareas(db, new_task, data[0])
            #print("Hola",send_task, "lo que se le envia a la clase ModeloTareas con el Metodo add_tareas \n")
            try:
                tasks, register_task = ModeloTareas.add_tareas(db, new_task, data[0])
                if tasks is not None:
                    flash('Task added successfully', 'success')
                else:
                    flash('You still dont have assigned tasks', 'danger')
                    return redirect(url_for("task"))
            except Exception as ex:
                print(ex)
                flash("The task exist","warning")
        # Obtener todas las tareas asociadas al usuario en la carga inicial de la página
        cursor = db.connection.cursor()
        select_all_tasks_sql = """SELECT id, nombre_tarea, estado FROM tareas WHERE id_usuario = '{}'""".format(data[0])
        cursor.execute(select_all_tasks_sql)
        send_tasks = cursor.fetchall()
        print("Entrando a html task")
        return render_template("task.html", send_tasks=send_tasks)
        #return render_template("task.html")  # Asegúrate de tener este bloque return para solicitudes GET
    else:#Si no esta logueado el usuario lo rederijira hacia la ruta login para que se pueda loguear
        return redirect(url_for('login'))


@app.route("/delete_task/<int:id>")
@login_required
def delete_task(id):#EL id lo recibo del boton eliminar que esta en la plantilla task.html que tiene un atributo id=task[0]
    print(id, "imprimiendo el id que recibo a travez de la url del boto de la plantilla task.html ")
    cursor = db.connection.cursor()
    sql = """ SELECT id FROM tareas WHERE id = '{}' """.format(id)#hago el select para ver si el id existe en la base de datos 
    cursor.execute(sql)
    ids = cursor.fetchone()#obtengo solo un valor que es el id, Si el select devolvio un valor 
    print(ids, "imprimiendo el id que obtengo al hacer el select en la funcion delete_task")
    if ids is not None:#Pregunto si el id que obtuve es diferente de None entonces hara el codigo de mas abajo 
        id_task = Tareas(ids[0], None, None, None)#Le envio el id en la posicion cero obtenido a la y los demas valores como None a la clase Tareas ya que no los voy a necesitar
        print(id_task.estado, id_task.id_usuario, id_task.nombre_tarea, id_task.id, "Lo que se le envia a la clase TAreas")
        id_tareas = ModeloTareas.delete_tarea(db, id_task)#creo una instancia del metodo de clase  ModeloTareas.delete_tarea el cual espera recibir dos valores la instancia de la base y la instancia de la clase Tareas que enrealidad solo envio en id los demas valores van como None
        print("lo que se le envia al metodo de clase delete_tarea", id_tareas)
        if id_tareas is  not None:#Pregunto si la instancia del metodo de clase es diferente de None entonces que envie un mensaje flash diciendo que se elimino la tarea ya que el proceso de eliminacion se hara en el metodo de instancia de  ModeloTareas.delete_tarea
            flash("Task deleted correctly", "success")
        #return redirect(url_for("task"))
        else:
            flash("Error deleting the task", "error")#Si la eliminacion de la tarea en el metodo de clase  ModeloTareas.delete_tarea falla se mostrara este msj

        # Obtener todas las tareas asociadas al usuario después de eliminar la tarea en el metodo de clase  ModeloTareas.delete_tarea, esta nueva lista de tareas se envia con la renderizacion de la plantilla task.html de la siguiente forma return render_template("task.html", send_tasks=send_tasks)
        select_all_tasks_sql = """SELECT id, nombre_tarea, estado FROM tareas WHERE id_usuario = '{}'""".format(current_user.id)
        cursor.execute(select_all_tasks_sql)
        send_tasks = cursor.fetchall()
        return render_template("task.html", send_tasks=send_tasks)
    else:
        return redirect(url_for("task"))#Si el id que me envia desde la plantilla task.html es igual a None entonces redirigira hacia la funcion task, esto es en el caso que el usuario envie dos veces a eliminar la misma tarea o que no exista la tarea




@app.route("/edit_task/<int:id>", methods=["GET", "POST"])
@login_required
def edit_task(id):
    print(id, "Id que recibo de la plantilla task del boton edit_task con atributo id=task[0]")
    cursor = db.connection.cursor()
    sql = """ SELECT id, nombre_tarea FROM tareas WHERE id = '{}'""".format(id)
    cursor.execute(sql)
    data = cursor.fetchone()
    print(data[0], data[1], data, "Data obtenida del select de edit_task")
    if request.method == "POST" :
        if data is not None:
            name_task = request.form['tarea']
            print("Entro al post desde el formulario el nombre nuevo de la tarea", name_task)
            update = Tareas(data[0], name_task, None, None)
            try:
                update_task = ModeloTareas.update_task(db, update) 
                print(update.id, update.nombre_tarea, update.estado,update.id_usuario, "lo que se le envia a la clase Tareas \n")
                if update_task is  not None:#Pregunto si la instancia del metodo de clase es diferente de None entonces que envie un mensaje flash diciendo que se elimino la tarea ya que el proceso de eliminacion se hara en el metodo de instancia de  ModeloTareas.delete_tarea
                    flash("Task updated correctly", "success")
                    return redirect(url_for("task"))
                else:
                    flash("Error deleting the task", "error")#Si la eliminacion de la tarea en el metodo de clase  ModeloTareas.delete_tarea falla se mostrara este msj
            except  Exception as ex:
                print ("Error al actualizar la tarea",ex)
        return render_template("edit_task.html")
        # Obtener todas las tareas asociadas al usuario después de eliminar la tarea en el metodo de clase  ModeloTareas.delete_tarea, esta nueva lista de tareas se envia con la renderizacion de la plantilla task.html de la siguiente forma return render_template("task.html", send_tasks=send_tasks)
    select_all_tasks_sql = """SELECT id, nombre_tarea, estado FROM tareas WHERE id_usuario = '{}' AND id = '{}'""".format(current_user.id, id)
    cursor.execute(select_all_tasks_sql)
    sends_tasks = cursor.fetchall()
    return render_template("edit_task.html", sends_tasks= sends_tasks )


@app.route("/done/<int:id>")
def done_task(id):
    cursor = db.connection.cursor()
    sql = """SELECT id, nombre_tarea, estado FROM tareas WHERE id = '{}'""".format(id)
    cursor.execute(sql)
    data =  cursor.fetchone()
    print(data[0], data[1], data[2]," el select para validar si existe la tarea")
    if data is not None:
        new_status = "Done"
        taskdone = Tareas(data[0], data[1], new_status, None)
        print(taskdone.id, taskdone.nombre_tarea, taskdone.estado, taskdone.id_usuario, "Esto es ccuando se instancia la clase tareas ")
        try:
            sendtask = ModeloTareas.update_estado(db, taskdone)
            if sendtask is not None:
                flash('The task has been marked as completed', 'success')
                return redirect(url_for("task"))
            else:
                flash('Could not mark the task as completed.','warning')
        except  Exception as ex:
            print ("Error al actualizar la tarea",ex)
    # Obtener todas las tareas asociadas al usuario después de eliminar la tarea en el metodo de clase  ModeloTareas.delete_tarea, esta nueva lista de tareas se envia con la renderizacion de la plantilla task.html de la siguiente forma return render_template("task.html", send_tasks=send_tasks)
    select_all_tasks_sql = """SELECT id, nombre_tarea, estado FROM tareas WHERE id_usuario = '{}'""".format(current_user.id)
    cursor.execute(select_all_tasks_sql)
    send_tasks = cursor.fetchall()
    return render_template("task.html", send_tasks=send_tasks)

        



# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Session closed', 'info')
    return redirect(url_for('login'))


if __name__ == "__main__":
    # app.register_blueprint(register_user)
    app.run(debug=True, host="0.0.0.0", port="5001")