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
