import os
import socket
from _thread import start_new_thread
import math
import time
import pandas as pd
import threading

# Definiciones iniciales
IP_ADDRESS = '192.168.20.22'
PORT = 8081
MAX_CLIENTS = 100000
LIST_OF_CLIENTS = []

# Carga de contraseñas desde archivo
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "rockyou.txt")

with open(file_path, 'r', encoding='latin-1') as archivo:
    lines = archivo.readlines()

# Crear un DataFrame a partir de las líneas
df = pd.DataFrame(lines, columns=['passwords'])

# Eliminar los caracteres de nueva línea de cada elemento
df['passwords'] = df['passwords'].str.strip()

# Convertir la columna del DataFrame en una lista
passwords = df['passwords'].tolist()

password_found = False  # Variable global para indicar si la contraseña ha sido encontrada
password_lock = threading.Lock()  # Lock para sincronizar el acceso a la variable


# Datos del usuario
username = "jborreroa"
salt = "06924b2c47968b211471080bd125e04c"
passw = "b305059c687b80704512cdc66dcb4966bb1d6ba75476a6c298dce7945d45cabc37a6fcc677ae3fee16457ef30d0bfedb995bdfda02e2e295f901af7ac8e2e743"

# Configuración del socket del servidor
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER_SOCKET.bind((IP_ADDRESS, PORT))
SERVER_SOCKET.listen(MAX_CLIENTS)
print(f'Server started at {IP_ADDRESS}:{PORT} and listening...')

def client_thread(client_socket, client_address, possible_pwd, user, pwd, salt):
    global password_found
    try:
        # Send the user, salt, and pwd first
        client_socket.sendall(bytes(f"{user},{salt},{pwd}", 'utf-8'))
        
        for password in possible_pwd:
            with password_lock:
                if password_found:
                    break
            # Send each password to the client
            client_socket.sendall(bytes(password, 'utf-8'))
            # Wait for the client's response
            data = client_socket.recv(1024)
            try:
                response = data.decode('utf-8')
            except UnicodeDecodeError:
                print("Received data is not valid UTF-8, trying Latin-1 decoding as fallback.")
                response = data.decode('latin-1')  # Fallback if necessary or log the error

            if response.strip() == "FOUND":
                with password_lock:
                    password_found = True
                print(f"Password found: {password}")
                broadcast()
                break

        remove(client_socket)

    except Exception as ex:
        print(f"Error in client_thread: {ex}")
        print("fue en esta: "+password)
        remove(client_socket)


def broadcast():
    
    for client in LIST_OF_CLIENTS:
        try:
            client.close()
        except Exception as ex:
            print(f"Error al cerrar la conexión del cliente: {ex}")
        finally:
            print("desconectado")
            




def remove(client_socket):
    if client_socket in LIST_OF_CLIENTS:
        LIST_OF_CLIENTS.remove(client_socket)
i=0
# Aceptación y manejo de clientes
while True:
    client_socket, client_address = SERVER_SOCKET.accept()
    LIST_OF_CLIENTS.append(client_socket)
    print(f"{client_address[0]} connected")
    
    # Distribución de contraseñas por cliente
    num_passwords = len(passwords)
    passwords_per_client = math.ceil(num_passwords / 190)
    start_index = i * passwords_per_client
    end_index = min(start_index + passwords_per_client, num_passwords)
    print(start_index)
    print(end_index)
    assigned_passwords = passwords[start_index:end_index]
    
    start_new_thread(client_thread, (client_socket, client_address, assigned_passwords, username, passw, salt))
    i+=1
# Cierre de sockets
for client in LIST_OF_CLIENTS:
    client.close()
SERVER_SOCKET.close()
