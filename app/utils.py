from passlib.context import CryptContext
ctx =  CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return ctx.hash(password)

def verify(plain_password, masked_password):
    return ctx.verify(plain_password, masked_password)