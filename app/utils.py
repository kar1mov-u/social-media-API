from passlib.context import CryptContext


def hash_password(palintext):
    pwd_context =CryptContext(schemes=["bcrypt"],deprecated="auto")
    return pwd_context.hash(palintext)