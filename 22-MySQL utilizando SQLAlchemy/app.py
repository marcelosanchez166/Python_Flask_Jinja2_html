from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meliodas1506@localhost/equipofutbol'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index_sqlalchemy.html', usuarios=usuarios)

# Agrega las rutas para las demás operaciones CRUD

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
