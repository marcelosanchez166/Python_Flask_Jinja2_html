
class Config:#Clase que servira para tener la clave secreta que se pondra mas adelante en una instruccion
    SECRET_KEY="TWVsaW9kYXMxNTA2JCQ="#Esta es la clave secreta que la app va utilizar debe estar encriptada y servira para poder crear tokens personalizados para cada formulario y para cada peticion que se realice 



class DevelopmentConfig(Config):#clase que hereda de la clase Config y que activara el modo debug en true para que los cambios los tome en automatico el server
    MYSQL_HOST="localhost"
    MYSQL_USER="root"
    MYSQL_PASSWORD="Meliodas1506"
    MYSQL_DB="todolist"


