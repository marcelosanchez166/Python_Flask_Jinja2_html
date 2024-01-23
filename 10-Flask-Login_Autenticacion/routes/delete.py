from flask import Blueprint

deletes = Blueprint("delete", __name__)

@deletes.route("/delete")
def delete():
    return "Hola desde una ruta Blueprint"