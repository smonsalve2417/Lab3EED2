
from Crypto.Hash import SHA3_512

P_pwd="brayden16"
salt = "06924b2c47968b211471080bd125e04c"
pwd = "b305059c687b80704512cdc66dcb4966bb1d6ba75476a6c298dce7945d45cabc37a6fcc677ae3fee16457ef30d0bfedb995bdfda02e2e295f901af7ac8e2e743"

for pepper in range(256):
    H = SHA3_512. new()
    password_b = bytes(P_pwd, 'utf-8')
    H.update (password_b)

    pepper_b = pepper.to_bytes (1, 'big')
    H.update (pepper_b)

    salt_b = bytes.fromhex(salt)
    H.update(salt_b)

    pwd_h = H.hexdigest()

    if pwd_h == pwd:
        print (P_pwd)
        print(pepper)
print("termino")