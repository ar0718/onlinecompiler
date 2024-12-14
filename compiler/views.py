from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User
from .errors import *

### Test Endpoints

@api_view(['GET'])
def Welcome(request):
    message = {"status_code": 200, "status_message": "api is up", "message": "Hello from AxG!"}
    return Response(message)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all() 
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def decodeJWT(request):
    message = {"status": 404, "message": "nothing was performed."}

    token = request.data.get("jwt")

    success, response, user = User.getUserFromJWT(token)
    message["message"] = response

    if not success:
        message["status"] = 500
        return Response(message)
    else:
        message["status"] = 200
        message["user"] = UserSerializer(user).data
        return Response(message)

    return Response(message)

### Primary Endpoints

@api_view(['POST'])
def signup(request):
    message = {"status": 404, "message": "nothing was performed."}

    name = request.data.get("name")
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    
    status, response, user = User.create_user(name=name, username=username, email=email, password=password)

    message["status"] = status
    message["message"] = response

    if status == 200:
        message["user"] = UserSerializer(user).data
    else:
        return Response(message)

    jwt_token = user.generateJWT()
    message["jwt"] = jwt_token

    return Response(message)

@api_view(['POST'])
def login(request):
    message = {"status": 404, "message": "nothing was performed."}

    username = request.data.get("username")
    password = request.data.get("password")

    status, response, user = User.verify_user(username=username, password=password)

    message["status"] = status
    message["message"] = response

    if status == 200:
        message["user"] = UserSerializer(user).data
    else:
        return Response(message)

    jwt_token = user.generateJWT()
    message["jwt"] = jwt_token

    return Response(message)