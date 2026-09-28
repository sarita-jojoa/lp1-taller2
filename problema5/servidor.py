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
def calcular_checksum(archivo):
    """Calcula el checksum MD5 de un archivo.
    Sirve para comprobar que el archivo recibido
    sea igual al archivo original.
    """
    md5 = hashlib.md5() # Crear oobjeto MD5

    # Abrir el archivo en modo binario y leerlo en bloques
    with open(nombre_archivo, 'rb') as archivo:
        
        while True:
             
        datos = archivo.read(BUFFER): # Leer el archivo en bloques de tamaño 

        if not datos: # Si no hay más datos, salir del bucle
                break
        
            md5.update(datos) # Actualizar el objeto MD5 con los datos leídos
        
    return md5.hexdigest() # Devolver el checksum en formato hexadecimal

            
