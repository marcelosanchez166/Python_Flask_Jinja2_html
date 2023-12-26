from flask import Flask, render_template

app = Flask(__name__)

class Usuario:
    def __init__(self, nombre, logged_in):
        self.nombre = nombre
        self.logged_in = logged_in

# Ruta de inicio
@app.route('/')
def inicio():
    # Supongamos que tienes un objeto Usuario, podrías pasarlo a la plantilla
    usuario = Usuario("John Doe", logged_in=False)
    return render_template('inicio.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
