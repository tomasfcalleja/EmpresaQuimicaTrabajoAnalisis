from flask import Blueprint, render_template
from app.services.productos_service import ProductoService

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/inicio')
def inicio():
    productos = ProductoService.obtener_productos()  
    return render_template('inicio/inicio.html', productos=productos)

from flask import Blueprint, render_template
from app.services.productos_service import ProductoService

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/inicio')
def inicio():
    productos = ProductoService.obtener_productos()  
    return render_template('inicio/inicio.html', productos=productos)

@inicio_bp.route('/ver_carrito')
def ver_carrito():
    return render_template('inicio/ver_carrito.html')


@inicio_bp.route('/realizar_pago')
def realizar_pago():
    return render_template('inicio/realizar_pago.html')
