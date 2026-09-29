# Problema 5: Transferencia de Archivos (Upload/Download)

import socket
import os          # archivos y carpetas
import hashlib     #checksum
import threading   #varios clientes 

HOST = 'localhost'     # dirección IP del servidor
PORT = 9000            # puerto del servidor
BUFFER = 1024          # Tamaño del buffer utilizado para enviar y recibir datos

#CALCULAR CHECKSUM

def checksum_archivo(nombre_archivo):
    """
    Calcula el checksum SHA-256 de un archivo.
    """

    # Crear objeto MD5
    md5 = hashlib.md5()

    # Abrir archivo en modo lectura binaria
    with open(nombre_archivo, 'rb') as archivo:

        while True:

            # Leer una parte del archivo
            datos = archivo.read(BUFFER)

            # Si no quedan datos, terminar
            if not datos:
                break

            # Actualizar checksum
            md5.update(datos)

    return md5.hexdigest()

# SUBIR ARCHIVO

def upload(client):
    """
    Sube un archivo desde el cliente al servidor.
    """

    # Mostrar la carpeta actual
    print("\nCarpeta donde se están buscando los archivos:")
    print(os.getcwd())

    # Obtener archivos de la carpeta actual
    archivos = os.listdir()

    # Mostrar archivos disponibles
    print("\nArchivos disponibles para subir:")

    # Variable para saber si encontramos archivos
    hay_archivos = False

    for archivo in archivos:

        # Mostrar solamente archivos
        if os.path.isfile(archivo):

            print("-", archivo)

            hay_archivos = True

    # Si no hay archivos
    if not hay_archivos:

        print("No hay archivos disponibles para subir.")

        return

    # Pedir nombre del archivo
    nombre = input("\nNombre del archivo: ")

    # Comprobar si existe
    if not os.path.isfile(nombre):

        print("El archivo no existe.")

        return

    # Obtener tamaño
    tamaño = os.path.getsize(nombre)

    # Calcular checksum original
    checksum = checksum_archivo(nombre)

    # Obtener solamente el nombre
    nombre_archivo = os.path.basename(nombre)

    # Crear comando UPLOAD
    comando = f"UPLOAD {nombre_archivo} {tamaño}"

    # Enviar comando al servidor
    client.send(comando.encode())

    # Esperar confirmación
    respuesta = client.recv(BUFFER).decode()

    # Comprobar que el servidor esté listo
    if respuesta != "READY":

        print("El servidor no está listo.")

        return

    # Abrir archivo en modo lectura binaria
    with open(nombre, 'rb') as archivo:

        while True:

            # Leer una parte
            datos = archivo.read(BUFFER)

            # Si no quedan datos, terminar
            if not datos:
                break

            # Enviar datos
            client.send(datos)

    # Recibir respuesta
    respuesta = client.recv(BUFFER).decode()

    print("\n" + respuesta)

    # Mostrar checksum original
    print(f"Checksum original: {checksum}")

# DESCARGAR ARCHIVO

def download(client):
    """
    Descarga un archivo desde el servidor.
    """

    # Pedir nombre
    nombre = input("Nombre del archivo: ")

    # Crear comando
    comando = f"DOWNLOAD {nombre}"

    # Enviar comando
    client.send(comando.encode())

    # Recibir información
    informacion = client.recv(BUFFER).decode()

    # Comprobar si existe
    if informacion == "ERROR":

        print("El archivo no existe en el servidor.")

        return

    # Separar tamaño y checksum
    partes = informacion.split()

    tamaño = int(partes[0])

    checksum_servidor = partes[1]

    # Avisar al servidor que estamos listos
    client.send("READY".encode())

    # Guardar archivo descargado
    with open(nombre, 'wb') as archivo:

        # Contador de bytes
        recibidos = 0

        while recibidos < tamaño:

            # Calcular cantidad a recibir
            cantidad = min(
                BUFFER,
                tamaño - recibidos
            )

            # Recibir datos
            datos = client.recv(cantidad)

            # Si no llegan datos
            if not datos:
                break

            # Guardar datos
            archivo.write(datos)

            # Actualizar contador
            recibidos += len(datos)

    # Calcular checksum del archivo descargado
    checksum_cliente = checksum_archivo(nombre)

    print("\nArchivo descargado correctamente.")

    print(
        f"Checksum servidor: {checksum_servidor}"
    )

    print(
        f"Checksum cliente: {checksum_cliente}"
    )

    # Comparar checksum
    if checksum_servidor == checksum_cliente:

        print("La integridad del archivo es correcta.")

    else:

        print("ERROR: El archivo está dañado.")

    
