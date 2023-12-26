from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    numero = db.Column(db.Integer, nullable=False)

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre')
    numero = IntegerField('Número')
    enviar = SubmitField('Guardar')

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    form = UsuarioForm()

    if form.validate_on_submit():
        nuevo_usuario = Usuario(nombre=form.nombre.data, numero=form.numero.data)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('crear_usuario.html', form=form)

@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioForm(obj=usuario)

    if form.validate_on_submit():
        usuario.nombre = form.nombre.data
        usuario.numero = form.numero.data
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editar_usuario.html', form=form, usuario=usuario)

@app.route('/eliminar_usuario/<int:usuario_id>')
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
