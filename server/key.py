from cryptography.fernet import Fernet

def generate_fernet_key():
    key = Fernet.generate_key()
    return key

# Generate a Fernet key
fernet_key = generate_fernet_key()
print(fernet_key.decode())

