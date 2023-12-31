from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Meliodas1506'
app.config['MYSQL_DB'] = 'equipofutbol'

db = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute('SELECT * FROM jugadores')
    usuarios = cursor.fetchall()
    return render_template('index_mysql.html', jugadores=usuarios)

# Agrega las rutas para las demás operaciones CRUD

if __name__ == '__main__':
    app.run(debug=True)
