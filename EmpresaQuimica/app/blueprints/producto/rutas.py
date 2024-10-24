from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.productos_service import ProductoService  # Importar el servicio de productos
import json

producto_bp = Blueprint('producto', __name__)

@producto_bp.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        nivel = request.form['nivel']
        stock = request.form['stock']
        imagen = request.form.get('imagen', '')  # Puedes manejar la carga de imágenes más adelante

        productos = ProductoService.obtener_productos()  
        nuevo_producto = {
            "id": str(len(productos) + 1),  # Asignar un nuevo ID
            "nombre": nombre,
            "precio": float(precio),  # Asegúrate de convertir el precio a float
            "descripcion": descripcion,
            "nivel": int(nivel),  # Convertir nivel a entero
            "stock": int(stock),  # Convertir stock a entero
            "imagen": imagen
        }

        try:
            if ProductoService.agregar_producto(nuevo_producto):
                flash("Producto agregado exitosamente.", "success")
                return redirect(url_for('producto.ver_productos')) 
            else:
                flash("Error al agregar el producto.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('producto/agregar_producto.html')


@producto_bp.route('/editar_producto/<id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    producto_a_editar = ProductoService.obtener_producto_por_id(id_producto)  # Obtiene el producto por ID

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        nivel = request.form['nivel']
        stock = request.form['stock']
        imagen = request.form.get('imagen', '')  # Puedes manejar la carga de imágenes más adelante

        # Crear un diccionario para el producto actualizado
        producto_actualizado = {
            "id": id_producto,
            "nombre": nombre,
            "precio": float(precio),
            "descripcion": descripcion,
            "nivel": int(nivel),
            "stock": int(stock),
            "imagen": imagen
        }

        try:
            if ProductoService.actualizar_producto(producto_actualizado):  # Método para actualizar producto
                flash("Producto actualizado exitosamente.", "success")
                return redirect(url_for('producto.ver_productos')) 
            else:
                flash("Error al actualizar el producto.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('producto/editar_producto.html', producto=producto_a_editar)


@producto_bp.route('/eliminar_producto/<id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    try:
        if ProductoService.eliminar_producto(id_producto):
            flash("Producto eliminado exitosamente.", "success")
        else:
            flash("Error al eliminar el producto.", "danger")
    except Exception as e:
        flash(f"Ocurrió un error: {str(e)}", "danger")

    return redirect(url_for('producto.ver_productos'))


@producto_bp.route('/ver_productos', methods=['GET'])
def ver_productos():
    print("Hola", flush=True)
    productos = ProductoService.obtener_productos()  
    print(productos)
    return render_template('producto/ver_productos.html', productos=productos)
