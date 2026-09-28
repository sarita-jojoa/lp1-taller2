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
