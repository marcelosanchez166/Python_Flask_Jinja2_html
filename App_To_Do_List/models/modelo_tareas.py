
from models.entities.tareas import Tareas
#from app import current_user
from flask import flash, render_template, redirect, url_for
class ModeloTareas():
    @classmethod
    def add_tareas(self, db, new_task, id_user):
        print(new_task.nombre_tarea, "Valor que recibe la funcion add tareas", id_user)
        try:
            # if current_user.is_authenticated:
                cursor = db.connection.cursor()
                               # Verificar si la tarea ya existe para evitar duplicados
                existing_task_sql = """SELECT id FROM tareas WHERE nombre_tarea = '{}' AND id_usuario = '{}'""".format(new_task.nombre_tarea, id_user)
                cursor.execute(existing_task_sql)
                existing_task = cursor.fetchone()

                if not existing_task:
                    #Si La tarea no existe, podemos insertarla
                    #sql = """SELECT id, nombre_tarea, estado, id_usuario WHERE id_usuario = '{}'""" .format(usuario.id)
                    insert_sql  = """INSERT INTO tareas (nombre_tarea, estado, id_usuario) VALUES ('{}', '{}', '{}' )""".format(new_task.nombre_tarea, new_task.estado, id_user )
                    cursor.execute(insert_sql )
                    db.connection.commit()
                    #new_user_id = cursor.lastrowid
                    #print("data cuando hago el insert en el metodo registeruser \n", new_user_id)

                    # Obtener todas las tareas asociadas al usuario después de agregar una nueva
                    select_all_tasks_sql = """SELECT id, nombre_tarea, estado, id_usuario FROM tareas WHERE id_usuario = '{}'""".format(id_user)
                    cursor.execute(select_all_tasks_sql)
                    tasks = cursor.fetchall()


                    register_task = Tareas(id = None , nombre_tarea=new_task.nombre_tarea, estado=new_task.estado, id_usuario=id_user)
                    print(register_task, "Imprimiendo lo que se le envia a la clase Usuario desde cuando se le envian las cosas despues de hacer el insert")
                    return tasks, register_task
                else:
                    flash("The task exist","warning")
                    return render_template("task.html")
            # else:
            #     # Manejar el caso en el que el usuario no esté autenticado
            #     raise Exception("Usuario no autenticado.")
        except Exception as ex:
            print(f"Error durante la inserción: {ex}")
            raise Exception(str(ex))


    @classmethod
    def delete_tarea(self,db,id_tarea):
        cursor = db.connection.cursor()
        sql= """SELECT id  FROM tareas WHERE id = '{}' """.format(id_tarea.id)
        cursor.execute(sql)
        ids = cursor.fetchone()
        if ids is not None:
            delete_id = """DELETE FROM tareas WHERE id = '{}'""".format(ids[0])
            cursor.execute(delete_id)
            db.connection.commit()
            # flash('Task deleted successfully','success')
            return delete_id
        else:
            flash('Error deleting the task', 'error')
            return redirect(url_for("task"))
        

    @classmethod
    def update_task(self, db, update):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, nombre_tarea, estado, id_usuario FROM tareas  WHERE id = '{}'""".format(update.id)
            cursor.execute(sql)
            data = cursor.fetchone()
            print(data[1],data[0], "Id de la tarea antes de actualizar ")
            if data is not None :
                update_tasks = """ UPDATE tareas SET nombre_tarea = '{}' WHERE id = '{}' """.format(update.nombre_tarea, data[0])
                cursor.execute(update_tasks)
                db.connection.commit()

                # # Obtener todas las tareas asociadas al usuario después de agregar una nueva
                # select_all_tasks_sql = """SELECT id, nombre_tarea, estado, id_usuario FROM tareas WHERE id_usuario = '{}'""".format(data[3])
                # cursor.execute(select_all_tasks_sql)
                # tasks = cursor.fetchall()

                register_task = Tareas(id = None , nombre_tarea=update.nombre_tarea, estado=None, id_usuario=None)
                print(register_task, "Imprimiendo lo que se le envia a la clase Usuario desde cuando se le envian las cosas despues de hacer el insert")

                return update_tasks, register_task
            else:
                flash('Failed to update task', 'error')
                return render_template("task.html")
        except  Exception as ex:
            print(f"Error durante la actualizacion: {ex}")
            raise Exception(str(ex))