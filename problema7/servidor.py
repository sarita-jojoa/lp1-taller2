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

# PROCESAR PETICIÓN HTTP

def procesar_http(client, peticion):
    """
    Procesa una petición HTTP normal.
    """
    try:

        # Convertir petición a texto
        texto = peticion.decode('iso-8859-1')

        # Mostrar la petición recibida
        print("\nPetición recibida:")

        # Mostrar solamente la primera línea
        print(texto.split('\r\n')[0])

        # Obtener primera línea
        primera_linea = texto.split('\r\n')[0]

        # Separar los elementos
        partes = primera_linea.split()

        # Comprobar que la petición sea correcta
        if len(partes) < 2:

            client.send(b"HTTP/1.1 400 Bad Request\r\n\r\n")

            return

        # Obtener método
        metodo = partes[0]

        # Obtener URL
        url = partes[1]

        # Mostrar método
        print(f"Método: {metodo}")

        # Mostrar URL
        print(f"URL: {url}")

        # OBTENER HOST

        host = None

        # Buscar el header Host
        for linea in texto.split('\r\n'):

            if linea.lower().startswith('host:'):

                host = linea.split(':', 1)[1].strip()

                break

        # Comprobar que exista Host
        if host is None:

            client.send(b"HTTP/1.1 400 Bad Request\r\n\r\n")

            return

        # OBTENER PUERTO

        # Puerto HTTP
        port = 80

        # Comprobar si el host tiene puerto
        if ':' in host:

            host, puerto = host.rsplit(':', 1)

            port = int(puerto)

        # Mostrar destino
        print(f"Servidor destino: {host}:{port}")

        # MODIFICAR HEADERS

        peticion = modificar_headers(peticion)

        # CONECTAR CON DESTINO

        servidor_destino = conectar_servidor(host, port)

        # ENVIAR PETICIÓN

        servidor_destino.sendall(peticion)

        print("Petición enviada al servidor destino.")

        # RECIBIR RESPUESTA

        while True:

            # Recibir datos
            datos = servidor_destino.recv(BUFFER)

            # Si no hay datos, terminar
            if not datos:
                break

            # Enviar respuesta al cliente
            client.sendall(datos)

        # Cerrar conexión
        servidor_destino.close()

    except Exception as error:

        print(f"Error HTTP: {error}")

# PROCESAR HTTPS

def procesar_https(client, peticion):
    """
    Procesa el método CONNECT utilizado por HTTPS.

    El proxy crea un túnel entre el cliente y
    el servidor destino.
    """

    try:

        # Convertir petición a texto
        texto = peticion.decode('iso-8859-1')

        # Obtener primera línea
        primera_linea = texto.split('\r\n')[0]

        print(f"\nPetición HTTPS: {primera_linea}")

        # Separar los elementos
        partes = primera_linea.split()

        # Obtener destino
        destino = partes[1]

        # Separar host y puerto
        host, port = destino.split(':')

        # Convertir puerto a entero
        port = int(port)

        # Conectar con servidor destino
        servidor_destino = conectar_servidor(host,port)

        # Informar al cliente que el túnel
        # se estableció correctamente
        client.sendall(b"HTTP/1.1 200 Connection Established\r\n"b"\r\n")

        print(f"Túnel HTTPS creado con {host}:{port}")

        # CLIENTE -> SERVIDOR

         hilo_cliente = threading.Thread(target=reenviar_datos, args=(client, servidor_destino))
