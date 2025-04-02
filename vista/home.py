# /vista/home.py
from flask import Blueprint,render_template,session,redirect,url_for

home=Blueprint("home",__name__,static_folder="static",template_folder="templates")

@home.route("/home",methods = ['GET', 'POST'])
@home.route("/")
def vista_home():
    #código de validación de control de acceso al home
    return redirect('/inicio')  
