import socket
from Crypto.Hash import SHA3_512

IP_ADDRESS = '192.168.20.22'
PORT = 8081

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))

def safe_decode(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        print("Received data is not valid UTF-8, attempting Latin-1 decoding as fallback.")
        return data.decode('latin-1')  

# Receive the user, salt, and pwd
data = client_socket.recv(2048)
user_salt_pwd = safe_decode(data)
user, salt, pwd = user_salt_pwd.split(',')
while True:
    data = client_socket.recv(1024)
    password = safe_decode(data).strip()
    if password==None:
        print('nothing found')
        break
    # Perform SHA3_512 hashing
    for pepper in range(256):
        hasher = SHA3_512.new()
        hasher.update(bytes(password, 'utf-8'))
        hasher.update(pepper.to_bytes(1, 'big'))
        hasher.update(bytes.fromhex(salt))
        hashed_password = hasher.hexdigest()

        # Send response to the server if a match is found
        if hashed_password == pwd:
            client_socket.sendall(b"FOUND")
            print(f"encontrada, es esta: {password} en pepper: {pepper}")
            
            break
        
            
    client_socket.sendall(b"NOT FOUND")
    print(password)
client_socket.close()
