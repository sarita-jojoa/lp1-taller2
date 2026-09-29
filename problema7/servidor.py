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

# MODIFICAR HEADERS

def modificar_headers(peticion):
    """
    Agrega un header a la petición HTTP.
    """

    # Convertir los datos a texto
    texto = peticion.decode('iso-8859-1')

    # Agregar un header personalizado
    texto = texto.replace('\r\n\r\n', '\r\nX-Proxy: Problema7\r\n\r\n')

    # Convertir nuevamente a bytes
    return texto.encode('iso-8859-1')

# REENVIAR DATOS

def reenviar_datos(origen, destino):
    """
    Recibe datos de un socket y los envía a otro.

    Esta función permite realizar comunicación
    bidireccional entre cliente y servidor.
    """

    try:

        while True:

            # Recibir datos
            datos = origen.recv(BUFFER)

            # Si no se reciben datos, terminar
            if not datos:
                break

            # Enviar datos al destino
            destino.sendall(datos)

    except:

        pass
