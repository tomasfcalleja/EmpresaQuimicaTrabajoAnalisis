
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.ventas_service import VentasService  # Importa el servicio de ventas

ventas_bp = Blueprint('venta', __name__)

@ventas_bp.route('/agregar_venta', methods=['GET', 'POST'])
def agregar_venta():
    if request.method == 'POST':
        id = request.form['id']  # Suponiendo que tendrás este campo en el formulario
        id_usuario = request.form['idUsuario']  # Suponiendo que tendrás este campo en el formulario

        # Crear un diccionario para la nueva venta
        nueva_venta = {
            "id": id,
            "idUsuario": id_usuario
        }

        try:
            if VentasService.agregar_venta(nueva_venta):  # Método para agregar venta
                flash("Venta agregada exitosamente.", "success")
                return redirect(url_for('venta.ver_ventas')) 
            else:
                flash("Error al agregar la venta.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('venta/agregar_venta.html')  # Ruta a la plantilla para agregar venta

@ventas_bp.route('/editar_venta/<id_venta>', methods=['GET', 'POST'])
def editar_venta(id_venta):
    venta_a_editar = VentasService.obtener_venta_por_id(id_venta)  # Obtiene la venta por ID

    if request.method == 'POST':
        id= request.form['id']
        id_usuario = request.form['idUsuario']

        # Crear un diccionario para la venta actualizada
        venta_actualizada = {
            "id": id,
            "idUsuario": id_usuario
        }

        try:
            if VentasService.actualizar_venta(venta_actualizada):  # Método para actualizar venta
                flash("Venta actualizada exitosamente.", "success")
                return redirect(url_for('venta.ver_ventas')) 
            else:
                flash("Error al actualizar la venta.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('venta/editar_venta.html', venta=venta_a_editar)  # Ruta a la plantilla de edición

@ventas_bp.route('/eliminar_venta/<id_venta>', methods=['POST'])
def eliminar_venta(id_venta):
    try:
        if VentasService.eliminar_venta(id_venta):
            flash("Venta eliminada exitosamente.", "success")
        else:
            flash("Error al eliminar la venta.", "danger")
    except Exception as e:
        flash(f"Ocurrió un error: {str(e)}", "danger")

    return redirect(url_for('venta.ver_ventas'))

@ventas_bp.route('/ver_ventas', methods=['GET'])
def ver_ventas():
    ventas = VentasService.obtener_ventas()  # Obtener todas las ventas
    return render_template('venta/ver_venta.html', ventas=ventas)  # Ruta a la plantilla para ver ventas