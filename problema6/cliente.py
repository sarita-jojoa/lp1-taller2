#Problema 6: Chat con Salas - Cliente

import socket
import threading

# DATOS DEL SERVIDOR

# Dirección del servidor
HOST = 'localhost'

# Puerto del servidor
PORT = 9000

# FUNCIÓN PARA RECIBIR MENSAJES

def recibir_mensajes(client):
    """
    Recibe mensajes del servidor.

    Esta función se ejecuta en un hilo separado para poder
    recibir mensajes mientras el usuario escribe.
    """

    while True:

        try:

            # Recibir mensaje
            data = client.recv(1024)

            # Si no hay datos, terminar
            if not data:

                break

            # Mostrar mensaje
            print("\n" + data.decode())

        except:

            break

# CREAR SOCKET

# Crear socket IPv4 y TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# CONECTARSE AL SERVIDOR

cliente.connect((HOST, PORT))

# Pedir nombre del usuario
nombre = input("Ingrese su nombre: ")

# Enviar nombre al servidor
cliente.send(nombre.encode())

# Recibir confirmación
respuesta = cliente.recv(1024).decode()

print(respuesta)

# CREAR HILO PARA RECIBIR MENSAJES

# Crear hilo que estará escuchando al servidor
receptor = threading.Thread(target=recibir_mensajes, args=(cliente,))

# El hilo se cierra cuando termina el programa
receptor.daemon = True

# Iniciar hilo
receptor.start()

# MENÚ

while True:

    print("\n1. CREATE")
    print("2. JOIN")
    print("3. LEAVE")
    print("4. LIST")
    print("5. USERS")
    print("6. MSG")
    print("7. PRIVATE")
    print("8. EXIT")

    # Pedir opción
    opcion = input("Seleccione una opcion: ")

    # CREATE

    if opcion == '1':

        # Pedir nombre de sala
        sala = input("Nombre de la sala: ")

        # Crear comando
        comando = f"CREATE {sala}"

        # Enviar comando
        cliente.send(comando.encode())

    # JOIN

    elif opcion == '2':

        # Pedir nombre de sala
        sala = input("Nombre de la sala: ")

        # Crear comando
        comando = f"JOIN {sala}"

        # Enviar comando
        cliente.send(comando.encode())

    # LEAVE

    elif opcion == '3':

        # Pedir nombre de sala
        sala = input("Nombre de la sala: ")

        # Crear comando
        comando = f"LEAVE {sala}"

        # Enviar comando
        cliente.send(comando.encode())

    # LIST

    elif opcion == '4':

        # Enviar comando LIST
        cliente.send("LIST".encode())

    # USERS

    elif opcion == '5':

        # Pedir nombre de sala
        sala = input("Nombre de la sala: ")

        # Crear comando
        comando = f"USERS {sala}"

        # Enviar comandocliente.send(comando.encode())

    # MSG

    elif opcion == '6':

        # Pedir sala
        sala = input("Nombre de la sala: ")

        # Pedir mensaje
        mensaje = input("Mensaje: ")

        # Crear comando
        comando = f"MSG {sala} {mensaje}"

        # Enviar mensaje
        cliente.send(comando.encode())

    # PRIVATE

    elif opcion == '7':

        # Pedir destinatario
        destinatario = input("Usuario destinatario: ")

        # Pedir mensaje
        mensaje = input("Mensaje: ")

        # Crear comando
        comando = (f"PRIVATE {destinatario} {mensaje}")

        # Enviar mensaje
        cliente.send(comando.encode())

    # EXIT

    elif opcion == '8':

        # Informar al servidor que queremos salir
        cliente.send("EXIT".encode())

        print("Desconectando del servidor...")

        break

    # OPCIÓN INCORRECTA


    else:

        print("Opción no válida.")

# CERRAR CONEXIÓN

# Cerrar socket
cliente.close()

print ("Conexión cerrada.")
