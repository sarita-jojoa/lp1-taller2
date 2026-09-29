"""
Problema 8: Servidor de juegos - Tic-Tac-Toe

Objetivo:
Crear un servidor que permita jugar Tic-Tac-Toe
entre dos jugadores y tener espectadores.

Conceptos clave:
- Estado compartido
- Coordinación de turnos
- Validación de movimientos
- Matchmaking
- Espectadores
"""
import socket
import threading

# Dirección y puerto del proxi
HOST = 'localhost'
PORT = 9000

# Tamaño del buffer
BUFFER = 1024

# RECIBIR MENSAJES

def recibir_mensajes(cliente):
    """
    Recibe mensajes del servidor.

    Esta función se ejecuta en un hilo separado
    para poder recibir mensajes mientras el jugador
    escribe.
    """

    while True:

        try:

            # Recibir datos
            data = cliente.recv(BUFFER)

            # Si no se reciben datos
            if not data:

                break

            # Mostrar mensaje
            print("\n" + data.decode())

        except:

            break

# Crear socket TCP

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# CONECTARSE AL SERVIDOR

cliente.connect((HOST, PORT))

print( "Conectado al servidor.")

# PEDIR NOMBRE

nombre = input("Ingrese su nombre: ")


# Enviar nombre
cliente.send(nombre.encode())

# ELEGIR TIPO DE CONEXIÓN

print(cliente.recv(BUFFER).decode())

# Pedir opción
opcion = input("Seleccione una opcion: ")

# Enviar opción
cliente.send(opcion.encode())

# CREAR HILO PARA RECIBIR MENSAJES

receptor = threading.Thread(target=recibir_mensajes, args=(cliente,))

# El hilo termina cuando se cierra el programa
receptor.daemon = True

# Iniciar hilo
receptor.start()
