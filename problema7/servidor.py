"""
Problema 7: Proxy HTTP - Servidor

Objetivo:
Crear un proxy que reciba peticiones HTTP del cliente,
las reenvíe al servidor destino y devuelva la respuesta.

Conceptos:
- Proxy HTTP
- Reenvío de peticiones
- Modificación de headers
- Logging
- Comunicación bidireccional
- Método CONNECT para HTTPS
"""

import socket
import threading

# Dirección y puerto del proxi
HOST = 'localhost'
PORT = 9000

# Tamaño del buffer
BUFFER = 1024

# CONECTAR CON EL SERVIDOR DESTINO

def conectar_servidor(host, port):
    """
    Crea una conexión con el servidor destino.
    """

    # Crear un socket TCP
    servidor_destino = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Conectar con el servidor destino
    servidor_destino.connect((host, port))

    # Devolver el socket
    return servidor_destino