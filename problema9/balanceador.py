"""
Problema 9: Sistema Distribuido - Balanceador

Objetivo:
Crear un balanceador que reciba clientes y los
distribuya entre diferentes servidores backend.

Conceptos clave:
- Múltiples servidores
- Balanceo de carga
- Health checks
- Tolerancia a fallos
"""

import socket
import threading
import time


# TODO: Definir la dirección y puerto del balanceador

HOST = 'localhost'
PORT = 9000

# Tamaño del buffer
BUFFER = 1024

# SERVIDORES BACKEND

# Lista de servidores backend
# Cada servidor tiene:
# - nombre
# - dirección
# - puerto
# - estado

servidores = [
    {
        'nombre': 'BACKEND 1',
        'host': 'localhost',
        'port': 9001,
        'activo': False
    },

    {
        'nombre': 'BACKEND 2',
        'host': 'localhost',
        'port': 9002,
        'activo': False
    }
]


# Variable para saber qué servidor utilizar
servidor_actual = 0

# Lock para sincronizar los hilos
lock = threading.Lock()

# HEALTH CHECK

def health_check(servidor):
    """
    Comprueba si un servidor backend está disponible.
    """

    try:

        # Crear socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

        # Definir tiempo máximo de espera
        client.settimeout(2)

        # Intentar conectar
        client.connect((servidor['host'],servidor['port']))

        # Cerrar conexión
        client.close()

        # El servidor está activo
        return True

    except:

        # El servidor no está disponible
        return False

# COMPROBAR SERVIDORES

def comprobar_servidores():
    """
    Comprueba periódicamente el estado de los
    servidores backend.
    """

    # Guardar el estado anterior de cada servidor
    estados_anteriores = {}

    while True:

        # Recorrer servidores
        for servidor in servidores:

            # Comprobar estado
            servidor['activo'] = health_check(servidor)

            # Obtener estado anterior
            estado_anterior = estados_anteriores.get(
                servidor['nombre']
            )

            # Mostrar solamente si cambió el estado
            if servidor['activo'] != estado_anterior:

                # Mostrar estado
                if servidor['activo']:

                    print(f"{servidor['nombre']} está activo.")

                else:

                    print(f"{servidor['nombre']} está fuera de servicio.")

                # Guardar nuevo estado
                estados_anteriores[
                    servidor['nombre']
                ] = servidor['activo']

        # Esperar antes de volver a comprobar
        time.sleep(5)


# OBTENER SERVIDOR DISPONIBLE

def obtener_servidor():
    """
    Busca un servidor backend disponible.

    Utiliza una distribución sencilla tipo
    Round Robin.
    """

    global servidor_actual

    with lock:

        # Intentar encontrar un servidor
        for i in range(len(servidores)):

            # Obtener posición
            posicion = (servidor_actual + i) % len(servidores)

            # Obtener servidor
            servidor = servidores[posicion]

            # Comprobar si está activo
            if servidor['activo']:

                # Actualizar siguiente posición
                servidor_actual = ( posicion + 1) % len(servidores)

                return servidor

    # Si no existe servidor disponible
    return None

# MANEJAR CLIENTE

def handle_client(client, addr):
    """
    Atiende a un cliente y lo conecta con un
    servidor backend.
    """

    print( f"Cliente conectado desde {addr}")

    # Obtener servidor disponible
    servidor = obtener_servidor()

    # Comprobar si existe servidor
    if servidor is None:

        client.send("No hay servidores disponibles.".encode())

        client.close()

        return

    # Informar al cliente
    client.send(f"Conectado a {servidor['nombre']}".encode())

    try:

        # Crear conexión con backend
        backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar al backend
        backend.connect((servidor['host'], servidor['port']))

        # ENVIAR DATOS AL BACKEND
       

        while True:

            # Recibir datos del cliente
            data = client.recv(BUFFER)

            # Si no hay datos
            if not data:

                break

            # Enviar datos al backend
            backend.sendall(data)

            # Recibir respuesta
            respuesta = backend.recv(BUFFER)

            # Enviar respuesta al cliente
            client.sendall(respuesta)

    except Exception as error:

        print(f"Error con el backend: {error}")

        client.send("Error del servidor backend.".encode())

    finally:

        # Cerrar backend
        backend.close()

        # Cerrar cliente
        client.close()

        print(f"Cliente desconectado: {addr}")

# CREAR SOCKET

# AF_INET = IPv4
# SOCK_STREAM = TCP

servidor = socket.socket( socket.AF_INET,socket.SOCK_STREAM)

# ENLAZAR SOCKET

servidor.bind((HOST, PORT))

# ESCUCHAR CONEXIONES

servidor.listen()

print("Balanceador a la espera de conexiones...")

# INICIAR HEALTH CHECK


health_thread = threading.Thread(target=comprobar_servidores)

# El hilo continúa mientras el programa esté activo
health_thread.daemon = True

# Iniciar hilo
health_thread.start()

# ACEPTAR CLIENTES

while True:

    # Aceptar conexión
    client, addr = servidor.accept()

    # Crear hilo
    client_handler = threading.Thread(target=handle_client,args=(client, addr))

    # Iniciar hilo
    client_handler.start()
