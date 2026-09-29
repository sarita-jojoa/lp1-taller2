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

# Tablero del juego

# Los espacios vacíos se representan con "-"
tablero = [
    "-", "-", "-",
    "-", "-", "-",
    "-", "-", "-"
]

# Jugador 1
jugador1 = None

# Jugador 2
jugador2 = None

# Símbolos de los jugadores
simbolo_jugador1 = "X"
simbolo_jugador2 = "O"

# Indica de quién es el turno
turno = "X"

# Lista de espectadores
espectadores = []

# Lock para proteger el estado compartido
lock = threading.Lock()

