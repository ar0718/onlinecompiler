from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User
from .errors import *

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
def signup(request):
    message = {"status": 404, "message": "nothing was performed."}

    name = request.data.get("name")
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    
    status, user = User.create_user(name=name, username=username, email=email, password=password)

    if status == False:
        message["message"] = user
        return Response(message)
    else:
        message["status"] = 200
        message["message"] = UserSerializer(user).data

    jwt_token = user.generateJWT()
    message["jwt"] = jwt_token

    return Response(message)

@api_view(['POST'])
def login(request):
    message = {"status_code": 200, "status_message": "login is up", "message": "logic is yet to be implemented"}
    return Response(message)