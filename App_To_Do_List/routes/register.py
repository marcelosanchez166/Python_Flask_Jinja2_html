# from flask import Blueprint, render_template, request, redirect, flash, url_for
# from models.modelo_usuario import ModeloUsuario
# from models.entities.usuario import Usuario
# from configDB import DevelopmentConfig
# from  werkzeug.security import generate_password_hash, check_password_hash

# db = DevelopmentConfig

# register_user = Blueprint("register_user", __name__)

# @register_user.route("/register", methods=['GET', 'POST'])
# def register():
#     if request.form == 'POST':
#         username = request.form["username"]
#         password = request.form["password"]
#         password= generate_password_hash(password)
#         email = request.form["email"]
#         print(username, password, email, "lo que se envia en el formulario")
#         usuario = Usuario(None, username, password, email)
#         print(usuario.username, usuario.password, usuario.email, "lo que se le envia a la clase USUARIO")
#         user_register = ModeloUsuario.RegisterUser(db , usuario)
#         print(user_register, "lo que se le envia a la clase MODELOUSUARIO con el Metodo REgisterUser")
#         if user_register is not None:
#             flash('User successfully registered', 'success')
#             return redirect(url_for('login'))
#         else:
#             return render_template('register.html')
#     return render_template("register.html")