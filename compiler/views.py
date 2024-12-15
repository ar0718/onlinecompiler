from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User, CodeHandler
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
    message = {"status": 500, "message": NoOperation}

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
    message = {"status": 500, "message": NoOperation}

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
    message = {"status": 500, "message": NoOperation}

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

@api_view(['POST'])
def coderunner(request):
    message = {"status": 500, "message": NoOperation}

    code_data = request.data.get("code")
    user_input = request.data.get("user_input")
    language = request.data.get("language")

    if not all([code_data, language]):
        message["status"] = 400
        message["message"] = IncompleteData
        return Response(message)

    code = CodeHandler(code=code_data, language=language)

    if user_input:
        code.setUserInput(user_input)

    try:
        code.execute()
    except Exception as e:
        message["status"] = 500
        message["message"] = str(e)
        return Response(message)

    message["status"] = 200
    message["message"] = code.getSuggestion()
    message["output"] = code.getOutput()
    message["error"] = code.getError()
    message["runtime"] = code.getRuntime()

    return Response(message)