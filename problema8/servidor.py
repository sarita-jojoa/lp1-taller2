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

# MOSTRAR TABLERO

def mostrar_tablero():
    """
    Convierte el tablero en un texto
    para poder enviarlo a los clientes.
    """

    tablero_texto = (
        f"\n"
        f" {tablero[0]} | {tablero[1]} | {tablero[2]}\n"
        f"---+---+---\n"
        f" {tablero[3]} | {tablero[4]} | {tablero[5]}\n"
        f"---+---+---\n"
        f" {tablero[6]} | {tablero[7]} | {tablero[8]}\n"
    )

    return tablero_texto

# COMPROBAR GANADOR

def comprobar_ganador():
    """
    Comprueba si existe un ganador.
    """

    # Posibles combinaciones ganadoras
    combinaciones = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    # Recorrer combinaciones
    for a, b, c in combinaciones:

        # Comprobar que las posiciones no estén vacías
        if tablero[a] != "-":

            # Comprobar si los tres símbolos son iguales
            if tablero[a] == tablero[b] == tablero[c]:

                return tablero[a]

    # No hay ganador
    return None

# COMPROBAR EMPATE

def comprobar_empate():
    """
    Comprueba si el tablero está lleno.
    """

    # Si no existe ningún espacio vacío
    if "-" not in tablero:

        return True

    return False

# REINICIAR JUEGO

def reiniciar_juego():
    """
    Reinicia el tablero y el turno.
    """

    global tablero
    global turno

    # Crear tablero vacío
    tablero = [
        "-", "-", "-",
        "-", "-", "-",
        "-", "-", "-"
    ]

    # El primer turno será para X
    turno = "X"