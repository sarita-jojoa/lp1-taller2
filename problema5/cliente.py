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
