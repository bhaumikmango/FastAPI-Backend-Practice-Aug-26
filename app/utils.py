from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def hash(password : str):
    return pwd_context.hash(password)