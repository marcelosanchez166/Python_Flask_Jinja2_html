#Este archivo servira para tener la logica del inicio de sesion
from models.entities.usuario import Usuario
# from app import db


class ModeloUsuario():
    @classmethod
    def login(self, db, usuario):
        print(usuario.username,"usuarios enviados desde instancia de app", usuario.id)
        try:
            cursor=db.connection.cursor()
            print(cursor,"Imprimiendo el cursor")
            sql ="""SELECT id, username, password, email FROM usuarios WHERE
                        username = '{}'""".format(usuario.username)
            cursor.execute(sql)
            data= cursor.fetchone()#Usamos el metodo fecthone porque solo esperamos recibir un registro en este caso solo el usuario 
            print("password de data modelo usuario",data[2], data[0])
            print("password desde modelo usuario",usuario.password)
            if data != None :  # Verifica si hay datos y tiene al menos 3 elementos:
                    coincide=Usuario.verificar_Password(data[2],  usuario.password)
                    if coincide:#Si la variable coincide es verdadera 
                        #usuario_logueado=Jugadores(data[0], None, None, None, None, None, None, data[1], data[2] )#Instanciamos la clase Usuario del archivo usuario.py y solo les pasamos los argumentos de las posiciones 0 y 1 que corresponden al id y al Nombre_usuario y la password y el tipo de usuario le ponemos None para no exponer esos campos
                        usuario_logueado = Usuario(id=data[0], username=data[1],  password=data[2], email=data[3])
                        print(usuario_logueado)
                        return usuario_logueado
                    else:
                        return None
            else:
                    return None
        except Exception as ex:
            raise Exception(ex)



#Este metodo sirve para que se pueda usar el id como inicio de sesion el id_jugador se recibe del metodo def load_user(id_jugador) que esta en el archivo app.py 
    @classmethod
    def obtener_por_id(self,db,id):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id, username, password, email FROM usuarios WHERE
                        id = '{}'""".format(id)#En el format se le pasa el atributo que recibe el metodo obtener_por_id  
            cursor.execute(sql)
            data=cursor.fetchone()#Usamos el metodo fecthone porque solo esperamos recibir un registro en este caso solo el id 
            #print("Imprimiendo la data de oobtener por ID ",data)
            # if data is not None:
            usuario_logueado= Usuario(id=data[0], username=data[1], password=data[2], email=data[3])#Creamos una instancia de la clase Usuario y le pasamos las posiciones 0 que corresponde al id del usuario 1 de Nombre_usuario None para la clave ya que no la usaremos y la variable tipousuario que contiene las posiciones de 2 y 3 de la tupla data que son el id del tipo y el nombre del tipo
            return usuario_logueado #Este se almacena en la funcion load_user del archivo __init__.py
            # else:
            #     # Puedes decidir qué hacer si no se encuentra un usuario con ese ID
            #     return None
        except Exception as ex:
            raise Exception(ex)



