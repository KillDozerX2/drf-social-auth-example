from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def secret_message(request):
    return Response({
        "message": "Hi! This is a secret view"
    })
