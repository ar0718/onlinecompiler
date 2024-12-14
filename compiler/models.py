from django.db import models
import bcrypt
from typing import Tuple, Optional
import os
from dotenv import load_dotenv
import jwt
import datetime

from .errors import *
from .utils.chore import is_valid_email
from .utils.hash import hash_password, verify_password


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_MAX_TIMEDELTA = datetime.timedelta(minutes=30)

if not JWT_SECRET_KEY:
    raise("Please create an Environment Variable named JWT_SECRET_KEY")

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
 
    def __str__(self) -> str:
        return self.username

    
    @classmethod
    def create_user(cls :"User", name :str, username :str, email :str, password :str) -> Tuple[int, str, Optional["User"]]:
        if not all([name, username, email, password]):
            return (400, IncompleteData, None)

        if User.objects.filter(username=username).exists():
            return (403, UserExists, None)

        if not is_valid_email(email):
            return (403, InvalidEmail, None)

        hashed_password = hash_password(password)
        user = cls(name=name, username=username, email=email, password_hash=hashed_password)
        user.save()

        return(200,UserCreated, user)

    def verify_user(username :str, password :str) -> Tuple[bool, str, Optional["User"]]:
        if not all([username, password]):
            return (400, IncompleteData, None)
        
        user = User.objects.filter(username=username).first()
        if not user:
            return (404, UserNotExists, None)

        auth = verify_password(password=password, hashed_password=user.password_hash)

        if auth:
            return (200, LoggedIn, user)
        else:
            return (401, InvalidCredentials, None)

        return (400, BadResponse, None)

    def generateJWT(self) -> str:
        expiration_time = datetime.datetime.utcnow() + JWT_MAX_TIMEDELTA

        payload = {
            'username': self.username,
            'email': self.email,
            'exp': expiration_time
        }

        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

        return token


    def getUserFromJWT(token :str) -> Tuple[bool, str, Optional["User"]]:
        if not token:
            return (False, NoToken, None)
            
        try:
            decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])

            username = decoded_payload.get('username')
            email = decoded_payload.get('email')

            user = User.objects.filter(username=username).first() 
            if user and user.email == email:
                return (True, ValidToken, user)
            return (False, UserNotExists, None)

        except jwt.ExpiredSignatureError:
            return (False, ExpiredToken, None)
        except jwt.InvalidTokenError:
            return (False, InvalidToken, None)
        except Exception as e:
            return (False, str(e), None)