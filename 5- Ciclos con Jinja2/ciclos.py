# a) Ciclos:

# Jinja2 admite bucles for que te permiten iterar sobre listas, diccionarios, etc. Veamos un ejemplo más detallado:
from flask import Flask, render_template

app= Flask(__name__)

@app.route('/ejemplo_ciclo')
def ejemplo_ciclo():
    numeros = [1, 2, 3, 4, 5]
    return render_template('ejemplo_ciclo.html', listas_numeros=numeros)


if __name__ == '__main__':
    app.run(debug=True) 
