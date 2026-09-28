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
