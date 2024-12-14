from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def Welcome(request):
    message = {"status_code": 200, "status_message": "api is up", "message": "Hello from AxG!"}
    return Response(message)