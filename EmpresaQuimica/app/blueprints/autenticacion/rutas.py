from flask import Blueprint, render_template

autenticacion_bp = Blueprint('autenticacion', __name__, url_prefix='/autenticacion')

@autenticacion_bp.route('/login')
def login():
    return render_template('autenticacion/login.html')

@autenticacion_bp.route('/registro')
def registro():
    return render_template('autenticacion/registro.html') 
