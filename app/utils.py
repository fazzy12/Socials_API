from passlib.context import CryptContext
ctx =  CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return ctx.hash(password)
