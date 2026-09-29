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

# ENVIAR MENSAJE

def enviar(client, mensaje):
    """
    Envía un mensaje a un cliente.
    """

    try:

        client.send(mensaje.encode())

    except:

        pass

# NOTIFICAR A TODOS

def notificar_todos(mensaje):
    """
    Envía un mensaje a los dos jugadores
    y a los espectadores.
    """

    # Enviar a jugador 1
    if jugador1 is not None:

        enviar(jugador1, mensaje)

    # Enviar a jugador 2
    if jugador2 is not None:

        enviar(jugador2, mensaje)

    # Enviar a espectadores
    for espectador in espectadores:

        enviar(espectador, mensaje)

# REALIZAR MOVIMIENTO

def realizar_movimiento(simbolo, posicion):
    """
    Realiza un movimiento en el tablero.

    Recibe:
    - símbolo del jugador
    - posición seleccionada
    """

    global turno

    # Comprobar que sea el turno correcto
    if simbolo != turno:

        return "No es tu turno."

    # Comprobar que la posición sea válida
    if posicion < 0 or posicion > 8:

        return "Posición no válida."

    # Comprobar que la posición esté vacía
    if tablero[posicion] != "-":

        return "Esa posición ya está ocupada."

    # Colocar símbolo
    tablero[posicion] = simbolo

    # Comprobar ganador
    ganador = comprobar_ganador()

    if ganador is not None:

        return f"GANADOR:{ganador}"

    # Comprobar empate
    if comprobar_empate():

        return "EMPATE"

    # Cambiar turno
    if turno == "X":

        turno = "O"

    else:

        turno = "X"

    return "Movimiento correcto."

# MANEJAR JUGADOR

def manejar_jugador(client, simbolo, nombre):
    """
    Maneja las acciones de un jugador.
    """

    global jugador1
    global jugador2

    # Informar al jugador de su símbolo
    enviar(client, f"Tu símbolo es {simbolo}\n")

    # Enviar tablero
    enviar(client,mostrar_tablero())

    while True:

        try:

            # Recibir movimiento
            data = client.recv(BUFFER)

            # Si no hay datos
            if not data:

                break

            # Convertir datos a texto
            mensaje = data.decode().strip()

            # Comprobar salida
            if mensaje.upper() == "SALIR":

                break

            # Convertir posición a número
            try:

                posicion = int(mensaje)

            except:

                enviar(client, "Debes introducir una posición del 1 al 9.")

                continue

            # Convertir posición 1-9 a índice 0-8
            posicion = posicion - 1

            # Proteger el estado compartido
            with lock:

                # Realizar movimiento
                resultado = realizar_movimiento(simbolo, posicion)

                # Enviar resultado
                enviar(client, resultado)

                # Si el movimiento fue correcto
                if resultado == "Movimiento correcto.":

                    # Mostrar tablero actualizado
                    notificar_todos(mostrar_tablero())

                    # Informar turno
                    notificar_todos(f"Turno de: {turno}")

                # Si hay ganador
                elif resultado.startswith("GANADOR"):

                    ganador = resultado.split(":")[1]

                    notificar_todos(mostrar_tablero())

                    notificar_todos(f"El jugador {ganador} ha ganado.")

                    # Reiniciar tablero
                    reiniciar_juego()

                # Si hay empate
                elif resultado == "EMPATE":

                    notificar_todos(mostrar_tablero())

                    notificar_todos("El juego terminó en empate.")

                    # Reiniciar tablero
                    reiniciar_juego()

        except:

            break

    # DESCONEXIÓN DEL JUGADOR

    with lock:

        if jugador1 == client:

            jugador1 = None

        if jugador2 == client:

            jugador2 = None

    # Cerrar conexión
    client.close()

    print(f"{nombre} se desconectó.")