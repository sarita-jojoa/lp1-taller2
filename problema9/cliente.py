"""
Problema 9: Sistema Distribuido - Cliente

Objetivo:
Conectarse al balanceador y enviar comandos.

El balanceador decidirá a qué servidor backend
enviar la petición.
"""

import socket


# TODO: Definir la dirección del balanceador

HOST = 'localhost'
PORT = 9000

# Tamaño del buffer
BUFFER = 1024


# CONECTAR AL BALANCEADOR

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el balanceador
cliente.connect((HOST, PORT))

# Recibir mensaje del balanceador
respuesta = cliente.recv(BUFFER).decode()

print(respuesta)

# MENÚ

while True:

    print("\n1. GUARDAR DATO")
    print("2. CONSULTAR DATO")
    print("3. LISTAR DATOS")
    print("4. ESTADO")
    print("5. SALIR")

    # Pedir opción
    opcion = input("Seleccione una opcion: ")

    # GUARDAR DATO

    if opcion == '1':

        # Pedir clave
        clave = input("Ingrese la clave: ")

        # Pedir valor
        valor = input("Ingrese el valor: ")

        # Crear comando
        comando = (f"SET {clave} {valor}")

        # Enviar comando
        cliente.send(comando.encode())

        # Recibir respuesta
        respuesta = cliente.recv(BUFFER).decode()

        print(respuesta)

    # CONSULTAR DATO

    elif opcion == '2':

        # Pedir clave
        clave = input("Ingrese la clave: ")

        # Crear comando
        comando = (f"GET {clave}")

        # Enviar comando
        cliente.send(comando.encode())

        # Recibir respuesta
        respuesta = cliente.recv(BUFFER).decode()

        print( respuesta)

    # LISTAR DATOS

    elif opcion == '3':

        # Enviar comando
        cliente.send("LIST".encode())

        # Recibir datos
        respuesta = cliente.recv(BUFFER).decode()

        print(respuesta)

    # ESTADO

    elif opcion == '4':

        # Enviar comando
        cliente.send("STATUS".encode())

        # Recibir respuesta
        respuesta = cliente.recv(BUFFER).decode()

        print(respuesta)

    # SALIR

    elif opcion == '5':

        # Informar al servidor
        cliente.send("EXIT".encode())

        print("Desconectando del servidor...")

        break

    # OPCIÓN INCORRECTA

    else:

        print("Opción no válida.")

# CERRAR CONEXIÓN

cliente.close()

print("Conexión cerrada.")