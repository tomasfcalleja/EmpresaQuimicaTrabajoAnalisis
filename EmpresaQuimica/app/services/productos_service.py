from config import JSONBIN_URL_PRODUCTOS, HEADERS
import requests
import json

class ProductoService:

    @staticmethod
    def obtener_productos():
        response = requests.get(JSONBIN_URL_PRODUCTOS, headers=HEADERS)
        productos = response.json().get('record', [])
        return productos
        
    @staticmethod
    def agregar_producto(nuevo_producto):
        # Obtener los productos actuales
        response = requests.get(JSONBIN_URL_PRODUCTOS, headers=HEADERS)
        productos = response.json().get('record', [])

        # Añadir el nuevo producto a la lista
        productos.append(nuevo_producto)

        # Actualizar JSONBin con el array directamente
        update_response = requests.put(JSONBIN_URL_PRODUCTOS, json=productos, headers=HEADERS)

        return update_response.status_code == 200
    
    @staticmethod
    def obtener_producto_por_id(id_producto):
        productos = ProductoService.obtener_productos()
        return next((producto for producto in productos if producto['id'] == id_producto), None)
    
    @staticmethod
    def actualizar_producto(producto_actualizado):
        productos = ProductoService.obtener_productos()

        # Actualizar el producto en la lista
        for index, producto in enumerate(productos):
            if producto['id'] == producto_actualizado['id']:
                productos[index] = producto_actualizado
                break

        # Actualizar JSONBin con el array actualizado
        update_response = requests.put(JSONBIN_URL_PRODUCTOS, json=productos, headers=HEADERS)

        return update_response.status_code == 200

    @staticmethod
    def eliminar_producto(id_producto):
        productos = ProductoService.obtener_productos()

        # Filtrar productos que no son el que se va a eliminar
        productos_actualizados = [producto for producto in productos if producto['id'] != id_producto]

        # Actualizar JSONBin con el array modificado
        update_response = requests.put(JSONBIN_URL_PRODUCTOS, json=productos_actualizados, headers=HEADERS)

        return update_response.status_code == 200
