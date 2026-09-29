
#Problema 6: Chat con Salas - Servidor
#Comandos:
# CREATE  -> Crear una sala
# JOIN    -> Entrar a una sala
# LEAVE   -> Salir de una sala
# LIST    -> Ver salas disponibles
# USERS   -> Ver usuarios de una sala
# MSG     -> Enviar mensaje a una sala
# PRIVATE -> Enviar mensaje privado
# EXIT    -> Salir


import socket
import threading
import os

# Dirección del servidor
HOST = 'localhost'

# Puerto utilizado por el servidor
PORT = 9000

# Diccionario que guarda los clientes conectados
clients = {}

# Diccionario que guarda las salas y sus usuarios
rooms = {}

# Archivo donde se guardan las salas
ARCHIVO_SALAS = 'salas.txt'


# Lock para evitar problemas cuando varios hilos
# modifican las salas al mismo tiempo
lock = threading.Lock()

# CARGAR LAS SALAS

def cargar_salas():
    """
    Carga las salas guardadas en el archivo salas.txt.
    """

    # Comprobar si existe el archivo
    if not os.path.exists(ARCHIVO_SALAS):
        return

    # Abrir el archivo en modo lectura
    with open(ARCHIVO_SALAS, 'r') as archivo:

        # Leer cada línea
        for linea in archivo:

            # Eliminar espacios y saltos de línea
            sala = linea.strip()

            # Comprobar que no esté vacía
            if sala:

                # Crear la sala
                rooms[sala] = set()


# GUARDAR LAS SALAS

def guardar_salas():
    """
    Guarda las salas en el archivo salas.txt.

    Esto permite conservar las salas aunque
    se cierre el servidor.
    """

    # Abrir archivo en modo escritura
    with open(ARCHIVO_SALAS, 'w') as archivo:

        # Recorrer las salas
        for sala in rooms:

            # Guardar el nombre de la sala
            archivo.write(sala + '\n')


# ENVIAR MENSAJE

def enviar(client, mensaje):
    """
    Envía un mensaje a un cliente.
    """

    # Convertir el mensaje a bytes y enviarlo
    client.send(mensaje.encode())


# CREAR SALA

def crear_sala(nombre_sala):
    """
    Crea una nueva sala.
    """

    # Lock para proteger el diccionario
    with lock:

        # Comprobar si la sala ya existe
        if nombre_sala in rooms:

            return "La sala ya existe."

        # Crear la sala vacía
        rooms[nombre_sala] = set()

        # Guardar las salas
        guardar_salas()

    return f"Sala '{nombre_sala}' creada correctamente."

# UNIRSE A UNA SALA

def unirse_sala(nombre_usuario, nombre_sala):
    """
    Agrega un usuario a una sala.
    """

    with lock:

        # Comprobar que la sala exista
        if nombre_sala not in rooms:

            return "La sala no existe."

        # Agregar usuario a la sala
        rooms[nombre_sala].add(nombre_usuario)

    return f"Te has unido a la sala '{nombre_sala}'."


# SALIR DE UNA SALA

def salir_sala(nombre_usuario, nombre_sala):
    """
    Elimina un usuario de una sala.
    """

    with lock:

        # Comprobar que la sala exista
        if nombre_sala not in rooms:

            return "La sala no existe."

        # Comprobar que el usuario esté dentro
        if nombre_usuario not in rooms[nombre_sala]:

            return "No estás en esta sala."

        # Eliminar usuario
        rooms[nombre_sala].remove(nombre_usuario)

    return f"Has salido de la sala '{nombre_sala}'."


# LISTAR SALAS

def listar_salas():
    """
    Muestra las salas disponibles.
    """

    with lock:

        # Comprobar si no existen salas
        if not rooms:

            return "No hay salas disponibles."

        # Crear mensaje
        mensaje = "Salas disponibles:\n"

        # Recorrer las salas
        for sala in rooms:

            # Cantidad de usuarios
            cantidad = len(rooms[sala])

            mensaje += f"- {sala} ({cantidad} usuarios)\n"

    return mensaje

# LISTAR USUARIOS

def listar_usuarios(nombre_sala):
    """
    Muestra los usuarios que están dentro de una sala.
    """

    with lock:

        # Comprobar que exista la sala
        if nombre_sala not in rooms:

            return "La sala no existe."

        # Obtener usuarios
        usuarios = rooms[nombre_sala]

        # Comprobar si está vacía
        if not usuarios:

            return "No hay usuarios en esta sala."

        # Crear mensaje
        mensaje = "Usuarios de la sala:\n"

        # Mostrar cada usuario
        for usuario in usuarios:

            mensaje += f"- {usuario}\n"

    return mensaje


# ENVIAR MENSAJE A UNA SALA

def enviar_sala(nombre_sala, mensaje, remitente):
    """
    Envía un mensaje a todos los usuarios de una sala
    excepto al usuario que envió el mensaje.
    """

    # Recorrer usuarios de la sala
    for usuario in rooms[nombre_sala]:

        # Obtener socket del usuario
        client = clients.get(usuario)

        # No enviar al remitente
        if usuario != remitente:

            try:

                # Enviar mensaje
                client.send(mensaje.encode())

            except:

                pass


# MENSAJE PRIVADO

def mensaje_privado(remitente, destinatario, mensaje):
    """
    Envía un mensaje privado a otro usuario.
    """

    # Buscar el socket del destinatario
    client = clients.get(destinatario)

    # Comprobar si existe
    if client is None:

        return "El usuario no está conectado."

    try:

        # Enviar mensaje
        client.send(
            f"[Privado de {remitente}]: {mensaje}".encode()
        )

        return "Mensaje privado enviado."

    except:

        return "No se pudo enviar el mensaje."


# MANEJAR CLIENTE

def handle_client(client, client_name):
    """
    Atiende las solicitudes de un cliente.
    """

    print(
        f"{client_name} se ha conectado."
    )

    while True:

        try:

            # Recibir información
            data = client.recv(1024)

            # Si no hay datos, el cliente se desconectó
            if not data:

                break

            # Convertir bytes a texto
            mensaje = data.decode()

            # Separar el comando
            partes = mensaje.split()

            # Comprobar que exista un comando
            if not partes:

                continue

            # Obtener comando principal
            comando = partes[0].upper()

            # CREATE
            

            if comando == 'CREATE':

                if len(partes) < 2:
                    enviar(client,"Uso: CREATE nombre_sala")

                else:

                    sala = partes[1]

                    respuesta = crear_sala(sala) 
                    enviar(client, respuesta)


            # JOIN
            

            elif comando == 'JOIN':

                if len(partes) < 2:

                    enviar(client, "Uso: JOIN nombre_sala")

                else:

                    sala = partes[1]

                    respuesta = unirse_sala(client_name,sala)

                    enviar(client, respuesta)
            
            # LEAVE
            
            elif comando == 'LEAVE':

                if len(partes) < 2:

                    enviar(client,"Uso: LEAVE nombre_sala")

                else:

                    sala = partes[1]

                    respuesta = salir_sala(client_name, sala)

                    enviar(client, respuesta)

            # LIST

            elif comando == 'LIST':

                respuesta = listar_salas()

                enviar(client, respuesta)

            # USERS

            elif comando == 'USERS':

                if len(partes) < 2:

                    enviar(client, "Uso: USERS nombre_sala")

                else:

                    sala = partes[1]

                    respuesta = listar_usuarios(sala)

                    enviar(client, respuesta)


            # MSG

            elif comando == 'MSG':

                if len(partes) < 3:

                    enviar(client,"Uso: MSG sala mensaje")

                else:

                    sala = partes[1]

                    # Unir todas las palabras del mensaje
                    texto = ' '.join(partes[2:])

                    with lock:

                        # Comprobar que la sala exista
                        if sala not in rooms:

                            enviar(client,"La sala no existe.")

                        # Comprobar que el usuario pertenezca
                        elif client_name not in rooms[sala]:

                            enviar(client, "No perteneces a esta sala.")

                        else:

                            # Enviar mensaje a la sala
                            enviar_sala(sala, f"{client_name}: {texto}",client_name )

            # PRIVATE

            elif comando == 'PRIVATE':

                if len(partes) < 3:

                    enviar(client, "Uso: PRIVATE usuario mensaje")

                else:

                    # Obtener destinatario
                    destinatario = partes[1]

                    # Obtener mensaje
                    texto = ' '.join(partes[2:])

                    # Enviar mensaje privado
                    respuesta = mensaje_privado(client_name, destinatario, texto)

                    # Informar al remitente
                    enviar(client, respuesta)


            # EXIT

            elif comando == 'EXIT':

                enviar(client, "Desconectando...")

                break

            # COMANDO DESCONOCIDO

            else:

                enviar(client, "Comando no reconocido.")


        except ConnectionResetError:

            print(f"{client_name} se desconectó.")
            break

        except Exception as error:

            print(f"Error con {client_name}: {error}")
            break

    # ELIMINAR CLIENTE

    with lock:

        # Eliminar al usuario de todas las salas
        for sala in rooms:

            rooms[sala].discard(client_name)

        # Eliminar cliente
        if client_name in clients:

            del clients[client_name]


    # Cerrar conexión
    client.close()

    print(f"{client_name} se desconectó.")

# CARGAR SALAS

cargar_salas()

# CREAR SOCKET

# AF_INET = IPv4
# SOCK_STREAM = TCP

servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# ENLAZAR SOCKET

servidor.bind((HOST, PORT))

# ESCUCHAR CONEXIONES

servidor.listen()

print("Servidor de chat a la espera de conexiones...")

# ACEPTAR CLIENTES

while True:

    # Aceptar conexión
    client, addr = servidor.accept()

    print(f"Conexión realizada desde la IP {addr}")

    # Recibir nombre del usuario
    client_name = client.recv(1024).decode()

    # Comprobar si el nombre ya está utilizado
    with lock:

        if client_name in clients:

            client.send("El nombre de usuario ya está ocupado.".encode())

            client.close()

            continue

        # Guardar cliente
        clients[client_name] = client


    # Confirmar conexión
    client.send("Ya estás conectado al servidor.".encode())

    # Crear hilo para el cliente
    client_handler = threading.Thread( target=handle_client, args=(client, client_name))

    # Iniciar hilo
    client_handler.start()
