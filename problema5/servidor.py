# Problema 5: Transferencia de Archivos (Upload/Download)

import socket
import os          # archivos y carpetas
import hashlib     #checksum
import threading   #varios clientes 

HOST = 'localhost'     # dirección IP del servidor
PORT = 9000            # puerto del servidor
BUFFER = 1024          # Tamaño del buffer utilizado para enviar y recibir datos
CARPETA = 'archivos'   # Carpeta donde se guardarán los archivos

# CREAR CARPETA 
# Si la carpeta no existe, se crea automáticamente
if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)

#CALCULAR CHECKSUM
def checksum_archivo (nombre_archivo):

    """Calcula el checksum MD5 de un archivo.
    Sirve para comprobar que el archivo recibido
    sea igual al archivo original.
    """
    md5 = hashlib.md5() # Crear oobjeto MD5

    # Abrir el archivo en modo binario y leerlo en bloques
    with open(nombre_archivo, 'rb') as archivo:
        
        while True:
             
            datos = archivo.read(BUFFER) # Leer el archivo en bloques de tamaño 

            if not datos: # Si no hay más datos, salir del bucle
                break
        
            md5.update(datos) # Actualizar el objeto MD5 con los datos leídos
        
    return md5.hexdigest() # Devolver el checksum en formato hexadecimal

#CREAR RUTA SEGURA

def ruta_segura(nombre):           
    """Crea una ruta segura para guardar un archivo.
    Evita que se pueda acceder a archivos fuera de la carpeta
    especificada.
    """
    # Obtener solamente el nombre del archivo
    nombre = os.path.basename(nombre)

    # Crear la ruta dentro de la carpeta
    ruta = os.path.join(CARPETA, nombre)

    return ruta

# RECIBIR ARCHIVO
def recibir_archivo(client, nombre_archivo, tamaño):
    """
    Recibe un archivo desde el cliente.

    El archivo se recibe por partes utilizando BUFFER.
    """

    # Crear una ruta segura
    ruta = ruta_segura(nombre_archivo)

    # Contador de bytes recibidos
    recibidos = 0

    # Abrir el archivo en modo escritura binaria
    with open(ruta, 'wb') as archivo:

        while recibidos < tamaño:

            # Calcular cuántos bytes faltan
            cantidad = min(BUFFER, tamaño - recibidos)

            # Recibir datos
            datos = client.recv(cantidad)

            # Si no llegan datos, terminar
            if not datos:
                break

            # Guardar los datos recibidos
            archivo.write(datos)

            # Actualizar contador
            recibidos += len(datos)

    return ruta

# ENVIAR ARCHIVO 
def enviar_archivo(client, nombre_archivo):
    """
    Envía un archivo desde el servidor al cliente.
    """

    # Crear una ruta segura
    ruta = ruta_segura(nombre_archivo)

    # Comprobar si el archivo existe
    if not os.path.isfile(ruta):

        # Informar al cliente
        client.send("ERROR".encode())

        return

    # Obtener tamaño del archivo
    tamaño = os.path.getsize(ruta)

    # Calcular checksum
    checksum = checksum_archivo(ruta)

    # Enviar tamaño y checksum
    informacion = f"{tamaño} {checksum}"

    client.send(informacion.encode())

    # Esperar confirmación del cliente
    client.recv(BUFFER)

    # Abrir archivo en modo lectura binaria
    with open(ruta, 'rb') as archivo:

        while True:

            # Leer una parte del archivo
            datos = archivo.read(BUFFER)

            # Si no quedan datos, terminar
            if not datos:
                break

            # Enviar los datos
            client.send(datos)

#LISTAR ARCHIVOS

def listar_archivos():
    """
    Devuelve los archivos disponibles en el servidor.
    """

    # Obtener todos los elementos de la carpeta
    archivos = os.listdir(CARPETA)

    # Variable para guardar los nombres
    mensaje = ""

    # Recorrer los elementos
    for archivo in archivos:

        # Crear ruta completa
        ruta = os.path.join(CARPETA, archivo)

        # Comprobar que sea un archivo
        if os.path.isfile(ruta):

            # Agregar el nombre
            mensaje += archivo + "\n"

    # Si no se encontró ningún archivo
    if mensaje == "":
        return "No hay archivos en el servidor."

    return mensaje

# ATENDER CLIENTE 

def handle_client(client):
    """
    Atiende las solicitudes realizadas por un cliente.
    """

    while True:

        try:

            # Recibir comando
            comando = client.recv(BUFFER).decode()

            # Si no se recibe nada, el cliente se desconectó
            if not comando:
                break

            # Separar el comando
            partes = comando.split()

            # Obtener la acción
            accion = partes[0]

