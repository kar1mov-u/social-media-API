from passlib.context import CryptContext
pwd_context =CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(palintext):
    return pwd_context.hash(palintext)

def check_password(plaintext, hashed):
    return pwd_context.verify(plaintext,hashed)