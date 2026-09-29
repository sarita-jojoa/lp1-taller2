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
