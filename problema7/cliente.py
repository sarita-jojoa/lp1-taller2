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

# ENVIAR PETICIÓN HTTP

def enviar_peticion():
    """
    Envía una petición HTTP al proxy.
    """

    # Pedir servidor destino
    servidor_destino = input("Ingrese el servidor destino: ")

    # Crear petición HTTP
    peticion = (f"GET / HTTP/1.1\r\n " f"Host: {servidor_destino}\r\n" f"Connection: close\r\n"f"\r\n")

    # Crear socket TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectarse al proxy
    cliente.connect((HOST, PORT))

    print("\nConectado al proxy.")

    # Enviar petición
    cliente.sendall(peticion.encode())

    print("Petición enviada al proxy.")

    # RECIBIR RESPUESTA

    while True:

        # Recibir datos del proxy
        datos = cliente.recv(BUFFER)

        # Si no se reciben datos, terminar
        if not datos:

            break

        # Mostrar respuesta
        print(datos.decode('iso-8859-1'), end='')

    # Cerrar conexión
    cliente.close()

    print("\n\nConexión cerrada.")
