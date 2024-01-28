class Tareas:
    def __init__(self, id, nombre_tarea, estado, id_usuario ):
        self.id = id
        self.nombre_tarea = nombre_tarea
        self.estado = estado
        self.id_usuario = id_usuario
    

    def __str__(self):
        return f"Tareas(id={self.id}, nombre_tarea={self.nombre_tarea}, estado={self.estado}, id_usuario={self.id_usuario})"

    def get_id(self):
        return str(self.id)