"""
Problema 9: Sistema Distribuido - Backend

Objetivo:
Crear un servidor backend que atienda clientes
y mantenga datos sincronizados.

El mismo programa se puede ejecutar en dos puertos:
- 9001
- 9002
"""

import socket
import threading
import sys


# TODO: Definir la dirección del servidor

HOST = 'localhost'

# Tamaño del buffer
BUFFER = 1024

# PUERTO DEL SERVIDOR

# Obtener puerto desde la línea de comandos

if len(sys.argv) > 1:

    PORT = int(sys.argv[1])

else:

    PORT = 9001

# DATOS DEL SERVIDOR

# Diccionario donde se guardan los datos
datos = {}

# Lock para proteger los datos
lock = threading.Lock()

# MOSTRAR DATOS

def mostrar_datos():
    """
    Devuelve los datos almacenados.
    """

    # Comprobar si no existen datos
    if not datos:

        return "No hay datos almacenados."

    # Crear mensaje
    mensaje = "Datos almacenados:\n"

    # Recorrer datos
    for clave in datos:

        mensaje += (f"{clave}: {datos[clave]}\n" )

    return mensaje

# GUARDAR DATO

def guardar_dato(clave, valor):
    """
    Guarda un dato en el servidor.
    """

    with lock:

        # Guardar información
        datos[clave] = valor

    return "Dato guardado correctamente."

# MANEJAR CLIENTE

def handle_client(client, addr):
    """
    Maneja la conexión de un cliente.
    """

    print(f"Cliente conectado desde {addr}")

    # Enviar nombre del servidor
    client.send(f"Backend conectado en puerto {PORT}".encode())

    while True:

        try:

            # Recibir datos
            data = client.recv(BUFFER)

            # Si no hay datos
            if not data:

                break

            # Convertir a texto
            mensaje = data.decode()

            # Separar comando
            partes = mensaje.split()

            # Comprobar comando
            if not partes:

                continue

            # Obtener comando
            comando = partes[0].upper()

            # SET

            if comando == 'SET':

                if len(partes) < 3:

                    client.send("Uso: SET clave valor".encode())

                else:

                    # Obtener clave
                    clave = partes[1]

                    # Obtener valor
                    valor = ' '.join(partes[2:])

                    # Guardar dato
                    respuesta = guardar_dato(clave,valor)

                    # Enviar respuesta
                    client.send(respuesta.encode())

            # GET

            elif comando == 'GET':

                if len(partes) < 2:

                    client.send("Uso: GET clave".encode())

                else:

                    # Obtener clave
                    clave = partes[1]

                    with lock:

                        # Buscar dato
                        valor = datos.get(clave )

                    # Comprobar si existe
                    if valor is None:

                        client.send("El dato no existe.".encode())

                    else:

                        client.send(f"{clave}: {valor}".encode())

            # LIST

            elif comando == 'LIST':

                # Obtener todos los datos
                respuesta = mostrar_datos()

                # Enviar respuesta
                client.send(respuesta.encode())

            # STATUS

            elif comando == 'STATUS':

                # Informar estado
                client.send(f"Servidor activo: puerto {PORT}".encode())
            # EXIT

            elif comando == 'EXIT':

                client.send("Desconectando...".encode())

                break

            # COMANDO INCORRECTO

            else:

                client.send("Comando no válido.".encode())

        except Exception as error:

            print(f"Error: {error}")
            break


    # Cerrar conexión
    client.close()

    print(f"Cliente desconectado: {addr}")
    
# CREAR SOCKET

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ENLAZAR SOCKET

servidor.bind((HOST, PORT))

# ESCUCHAR CONEXIONES

servidor.listen()

print(f"Servidor backend iniciado en el puerto {PORT}")

# ACEPTAR CLIENTES

while True:

    # Aceptar conexión
    client, addr = servidor.accept()

    # Crear hilo
    client_handler = threading.Thread(target=handle_client,args=(client, addr))

    # Iniciar hilo
    client_handler.start()
