from config import JSONBIN_URL_VENTA, HEADERS  
import requests
import json

class VentasService:
    
    @staticmethod
    def obtener_ventas():
        try:
            response = requests.get(JSONBIN_URL_VENTA, headers=HEADERS)
            ventas = response.json().get('record', [])
            return ventas
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener ventas: {e}")
            return []

    @staticmethod
    def agregar_venta(nueva_venta):
        try:
            response = requests.get(JSONBIN_URL_VENTA, headers=HEADERS)
            ventas = response.json().get('record', [])

            ventas.append(nueva_venta)

            update_response = requests.put(JSONBIN_URL_VENTA, json=ventas, headers=HEADERS)

            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al agregar venta: {e}")
            return False

    @staticmethod
    def obtener_venta_por_id(id_venta):
        try:
            ventas = VentasService.obtener_ventas()
            return next((venta for venta in ventas if venta['id'] == id_venta), None)
        except Exception as e:
            print(f"Error al obtener la venta por ID: {e}")
            return None
    
    @staticmethod
    def actualizar_venta(venta_actualizada):
        try:
            ventas = VentasService.obtener_ventas()

            for index, venta in enumerate(ventas):
                if venta['id'] == venta_actualizada['id']:
                    ventas[index] = venta_actualizada
                    break

            update_response = requests.put(JSONBIN_URL_VENTA, json=ventas, headers=HEADERS)
            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al actualizar la venta: {e}")
            return False

    @staticmethod
    def eliminar_venta(id_venta):
        try:
            ventas = VentasService.obtener_ventas()
            ventas_actualizadas = [venta for venta in ventas if venta['id'] != id_venta]

            update_response = requests.put(JSONBIN_URL_VENTA, json=ventas_actualizadas, headers=HEADERS)
            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar la venta: {e}")
            return False