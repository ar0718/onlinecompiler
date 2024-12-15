from django.db import models
import bcrypt
from typing import Tuple, Optional
import os
from dotenv import load_dotenv
import jwt
import datetime
import subprocess
import time

from .errors import *
from .utils.chore import is_valid_email
from .utils.hash import hash_password, verify_password


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_MAX_TIMEDELTA = datetime.timedelta(minutes=30)

if not JWT_SECRET_KEY:
    raise("Please create an Environment Variable named JWT_SECRET_KEY")


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


class CodeHandler():
    def __init__(self, code :str, language :str) -> None:
        if not all([code, language]):
            return
        if language not in ['cpp','java','python']:
            return

        self.__code = code
        self.__language = language
        self.__output = None
        self.__error = None
        self.__runtime = None
        self.__suggestion = None
        self.__user_input = None

    def getCode(self) -> str:
        return self.__code

    def updateCode(self, code :str) -> bool:
        if code:
            self.__code = code
            return True
        return False

    def getCode(self) -> str:
        return self.__code

    def updateCode(self, code :str) -> bool:
        if code:
            self.__code = code
            return True
        return False

    def getLanguage(self) -> str:
        return self.__language

    def updateLanguage(self, language :str) -> bool:
        if language in ['cpp','java','python']:
            self.__language = language
            return True
        return False

    def getOutput(self) -> str:
        return self.__output

    def getError(self) -> str:
        return self.__error

    def getRuntime(self) -> str:
        return self.__runtime

    def getSuggestion(self) -> str:
        return self.__suggestion

    def setUserInput(self, input :str):
        self.__user_input = input

    def execute(self) -> None:
        try:
            if self.__language == 'python':
                filename = 'script.py'
                with open(filename, 'w') as file:
                    file.write(self.__code)
                command = ['python', filename]

            elif self.__language == 'cpp':
                filename = 'program.cpp'
                executable = 'program.out'
                with open(filename, 'w') as file:
                    file.write(self.__code)
                compile_result = subprocess.run(['g++', filename, '-o', executable], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    self.__error = compile_result.stderr
                    return
                command = ['./' + executable]

            elif self.__language == 'java':
                filename = 'Program.java'
                with open(filename, 'w') as file:
                    file.write(self.__code)
                compile_result = subprocess.run(['javac', filename], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    self.__error = compile_result.stderr
                    return
                command = ['java', 'Program']

            else:
                self.__error = "Unsupported language"
                return

            start_time = time.time()
            
            result = subprocess.run(
                command,
                input=self.__user_input,
                capture_output=True,
                text=True,
                timeout=3  # We are giving the program to run in max 3 seconds
            )
            end_time = time.time()

            self.__runtime = f"{end_time - start_time:.3f} seconds"
            self.__output = result.stdout
            self.__error = result.stderr
        except subprocess.TimeoutExpired:
            self.__error = "Time Limit Exceeded"
        except Exception as e:
            self.__error = str(e)    

class TestCase(models.Model):
    problem = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

    def getInput(self) -> str:
        return self.input_data

    def setInput(self, test_input :str) -> None:
        if not test_input:
            return
        self.input_data = test_input

    def getExcpectedOutput(self) -> str:
        return self.expected_output

    def setExcpectedOutput(self, output :str) -> None:
        if not output:
            return
        self.expected_output = output

    def testCode(code :CodeHandler) -> Tuple[bool, str]:
        code.setUserInput(self.input_data)
        try:
            code.execute()
        except Exception as e:
            return (False, str(e))
        if code.getOutput() == self.getExcpectedOutput():
            return (True, "success")
        else:
            result = f"Input:\n{self.getInput()};\n\nOutput:\n{code.getOutput()}\n\nExpected Output:\n{self.getExcpectedOutput()}"
            return (False, result)

class Problem(models.Model):
    title = models.CharField(max_length=255)
    statement = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    testcases = models.JSONField()
    solve_percentage = models.FloatField(default=0.0)
    solve_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 

    def solve(code :CodeHandler) -> Tuple[bool, int, str]:
        passed_tests = 0
        all_test_cases = self.test_cases.all()
        isSucceed = True
        message = NoOperation
        for test in all_test_cases:
            isSucceed, message = test.testCode(code)
            if not isSucceed:
                return (isSucceed, passed_tests, message)
            passed_tests += 1
        return (isSucceed, passed_tests, message)