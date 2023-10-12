import time
import opcua
from opcua import ua

import os
import numpy as np

def inicio():
    files = open("./ip_server_opc.txt", "r")
    sw = True
    for file in files:
        client = opcua.Client(file)
        print(file)
        try:
            if client.connect() is None:
                sw = True
                break
        except:
            print("Ha ocurrido un error")
            print("")
            sw = False
    files.close()
    if sw:
        return client
    else:       
        return None

client = inicio()
if client is None:
    print("Error de conexion")
    exit()