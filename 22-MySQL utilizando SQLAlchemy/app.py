from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Meliodas1506@localhost/users'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

@app.route('/')
def index():
    # Utiliza text() para declarar la expresión SQL
    usuarios = db.session.execute(text("SELECT * FROM usuario"))
    usuarios = usuarios.fetchall()
    print(usuarios)
    return render_template('index_sqlalchemy.html', usuarios=usuarios)


if __name__ == '__main__':
    app.run(debug=True)
