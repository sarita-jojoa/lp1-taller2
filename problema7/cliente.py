"""
Problema 7: Proxy HTTP - Cliente

Objetivo:
Conectarse al proxy y enviar una petición HTTP.

El cliente permite probar:
- Peticiones HTTP
- Comunicación con el proxy
- Respuesta del servidor destino
"""

import socket
import threading

# Dirección y puerto del proxi
HOST = 'localhost'
PORT = 9000

# Tamaño del buffer
BUFFER = 1024
