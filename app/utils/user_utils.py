import random
import string
from passlib.context import CryptContext
from app.utils.jwt_utils import decodeToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def getRandomString(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)

def verifyPassword(plain_password, hashedPassword):
    return pwd_context.verify(plain_password, hashedPassword)

def getPasswordHash(password):
    return pwd_context.hash(password)

def checkaccsess(token: str):
    return decodeToken(token)['userrole']

def getMyId(token: str):
    return decodeToken(token)['userid']