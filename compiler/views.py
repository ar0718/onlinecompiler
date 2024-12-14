from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User

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
    user = UserSerializer(data=request.data)
    message = {"status": 404, "message": "nothing was performed."}

    username = request.data.get("username")
    if User.objects.filter(username=username).exists():
        message["status"] = 403
        message["message"] = "User already exists."

    if user.is_valid():
        user.save()
        message["status"] = 200
        message["message"] = f"account for {username} is created!"
    else:
        message["status"] = 400
        message["message"] = "Please provide valid data."

    return Response(message)

@api_view(['POST'])
def login(request):
    message = {"status_code": 200, "status_message": "login is up", "message": "logic is yet to be implemented"}
    return Response(message)