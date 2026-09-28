# Problema 5: Transferencia de Archivos (Upload/Download)

import socket
import os          # archivos y carpetas
import hashlib     #cheksum
import threading   #varios clientes 

HOST = 'localhost' # dirección IP del servidor
PORT = 5000        # puerto del servidor