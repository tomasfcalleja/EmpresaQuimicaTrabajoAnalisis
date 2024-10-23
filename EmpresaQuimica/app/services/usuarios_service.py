from config import JSONBIN_URL_USUARIOS, HEADERS
import requests
import json

class UsuarioService:
    
    @staticmethod
    def obtener_usuarios():
        response = requests.get(JSONBIN_URL_USUARIOS, headers=HEADERS)
        usuarios = response.json().get('record', [])
        return usuarios

    @staticmethod
    def agregar_usuario(nuevo_usuario):
        # Obtener los usuarios actuales
        response = requests.get(JSONBIN_URL_USUARIOS, headers=HEADERS)
        usuarios = response.json().get('record', [])

        # Añadir el nuevo usuario a la lista
        usuarios.append(nuevo_usuario)

        # Actualizar JSONBin con el array directamente
        update_response = requests.put(JSONBIN_URL_USUARIOS, json=usuarios, headers=HEADERS)


        return update_response.status_code == 200
    
    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        usuarios = UsuarioService.obtener_usuarios()
        return next((usuario for usuario in usuarios if usuario['id'] == id_usuario), None)
    
    @staticmethod
    def actualizar_usuario(usuario_actualizado):
        usuarios = UsuarioService.obtener_usuarios()

        # Actualizar el usuario en la lista
        for index, usuario in enumerate(usuarios):
            if usuario['id'] == usuario_actualizado['id']:
                usuarios[index] = usuario_actualizado
                break

        # Actualizar JSONBin con el array actualizado
        update_response = requests.put(JSONBIN_URL_USUARIOS, json=usuarios, headers=HEADERS)

        return update_response.status_code == 200

    @staticmethod
    def eliminar_usuario(id_usuario):
        usuarios = UsuarioService.obtener_usuarios()

        # Filtrar usuarios que no son el que se va a eliminar
        usuarios_actualizados = [usuario for usuario in usuarios if usuario['id'] != id_usuario]

        # Actualizar JSONBin con el array modificado
        update_response = requests.put(JSONBIN_URL_USUARIOS, json=usuarios_actualizados, headers=HEADERS)

        return update_response.status_code == 200
