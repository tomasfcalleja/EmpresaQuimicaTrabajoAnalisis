from flask import Blueprint, render_template
from app.services.usuarios_service import UsuarioService 

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    return render_template('dashboard/index.html')

@dashboard_bp.route('/ver_usuarios')
def dashboardverusuarios():
    usuarios = UsuarioService.obtener_usuarios()
    return render_template('usuario/ver_usuarios.html', usuarios=usuarios)

@dashboard_bp.route('/ver_clientes')
def dashboardverclientes():
    usuarios = "Ghami"
    return render_template('cliente/ver_clientes.html', usuarios=usuarios)

@dashboard_bp.route('/ver_pedidos')
def dashboardverpedidos():
    usuarios = "Ghami"
    return render_template('pedido/ver_pedidos.html', usuarios=usuarios)

@dashboard_bp.route('/ver_ventas')
def dashboardverventas():
    usuarios = "Ghami"
    return render_template('venta/ver_ventas.html', usuarios=usuarios)

@dashboard_bp.route('/ver_productos')
def dashboardverproductos():
    return render_template('producto/ver_productos.html')

