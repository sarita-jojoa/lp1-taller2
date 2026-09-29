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