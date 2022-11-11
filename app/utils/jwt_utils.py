import jwt
import json

def createToken(secret:str,pyload:json):
    return jwt.encode(pyload, secret, algorithm='HS256')

def decodeToken(token:str):
   return jwt.decode(token, options={"verify_signature": False})