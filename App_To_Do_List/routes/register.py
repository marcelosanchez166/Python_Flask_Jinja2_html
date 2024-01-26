from flask import Blueprint, render_template

register_user = Blueprint("register_user", __name__)

@register_user.route("/register")
def register():
    return render_template("register.html")