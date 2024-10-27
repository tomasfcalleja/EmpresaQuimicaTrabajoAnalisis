from flask import session, redirect, url_for, render_template, flash, Blueprint, request, jsonify
from app.services.productos_service import ProductoService
from app.services.ventas_service import VentasService
import uuid  # Para generar IDs únicos

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/')
def index():
    productos = ProductoService.obtener_productos()  
    return render_template('inicio/inicio.html', productos=productos)

@inicio_bp.route('/inicio')
def inicio():
    productos = ProductoService.obtener_productos()  
    return render_template('inicio/inicio.html', productos=productos)

@inicio_bp.route('/ver_carrito')
def ver_carrito():
    return render_template('inicio/ver_carrito.html')

@inicio_bp.route('/realizar_pago')
def realizar_pago():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para realizar el pago.', 'warning')
        return redirect(url_for('autenticacion.login'))
    
    carrito = session.get('carrito', [])
    total = sum(item['precioTotal'] for item in carrito)

    return render_template('inicio/realizar_pago.html', carrito=carrito, total=total)

@inicio_bp.route('/procesar-pago', methods=['POST'])
def procesar_pago():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para realizar el pago.', 'warning')
        return redirect(url_for('autenticacion.login'))

    # Obtener los datos del formulario
    nombre_tarjeta = request.form.get('nombreTarjeta')
    numero_tarjeta = request.form.get('numeroTarjeta')
    fecha_expiracion = request.form.get('fechaExpiracion')
    cvv = request.form.get('cvv')

    # Simulación de éxito en el pago
    flash('Pago realizado con éxito.', 'success')

    # Obtener el carrito y el usuario actual
    carrito = session.get('carrito', [])
    usuario_id = session['usuario']['id']  # Asegúrate de que 'usuario' tenga un ID

    if not carrito:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('inicio.ver_carrito'))

    # Generar un nuevo ID para la venta
    venta_id = str(uuid.uuid4())

    # Crear la nueva venta
    nueva_venta = {
        "id": venta_id,
        "idUsuario": usuario_id
    }

    # Agregar la venta a JSONBin
    venta_agregada = VentasService.agregar_venta(nueva_venta)
    
    if not venta_agregada:
        flash('Hubo un error al registrar la venta.', 'danger')
        return redirect(url_for('inicio.ver_carrito'))

    # Registrar los detalles de la venta y reducir el stock
    for item in carrito:
        detalle_venta = {
            "id": str(uuid.uuid4()),  # ID único para cada detalle
            "idVenta": venta_id,
            "idProducto": item['id'],  # ID del producto en el carrito
            "cantidad": item['cantidad'],
            "precio": item['precioUnitario'],
            "subtotal": item['precioTotal']
        }
        
        # Agregar el detalle de la venta
        detalle_agregado = VentasService.agregar_detalle_venta(detalle_venta)
        
        if not detalle_agregado:
            flash(f'Error al registrar el detalle de venta para el producto {item["nombre"]}.', 'danger')
        
        # Reducir el stock del producto vendido
        stock_reducido = ProductoService.reducir_stock(item['id'], item['cantidad'])
        if not stock_reducido:
            flash(f'Error al reducir el stock del producto {item["nombre"]}.', 'danger')

    # Vaciar el carrito una vez realizado el pago y registrado
    session.pop('carrito', None)
    flash('El carrito ha sido vaciado.', 'info')  # Mensaje informativo

    return jsonify({'success': True})

@inicio_bp.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    carrito = request.get_json()  # Obtenemos el carrito desde el cliente
    if carrito:
        session['carrito'] = carrito  # Guardamos el carrito en la sesión
        return jsonify({'success': True})
    return jsonify({'success': False})
