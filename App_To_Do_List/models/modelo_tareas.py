from models.entities.usuario import Usuario


class ModeloTareas:
    @classmethod
    def tareas(self, db, usuario):
        cursor = db.connection.cursor()
        sql = """SELECT id, nombre_tarea, estado, id_usuario WHERE id_usuario = '{}'""" .format(usuario.id)