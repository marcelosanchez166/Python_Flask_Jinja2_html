from flask import Flask, render_template, request

app = Flask(__name__)

class Usuario:
    def __init__(self, nombre, logged_in):
        self.nombre = nombre
        self.logged_in = logged_in

# Ruta de inicio
@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        logged_in = bool(request.form.get('logged_in'))  # Convertir a booleano
        usuario = Usuario(nombre, logged_in)
        return render_template('inicio.html', usuario=usuario)
    else:
        # Mostrar el formulario inicial
        return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)
