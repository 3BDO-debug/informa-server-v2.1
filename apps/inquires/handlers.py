from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from . import models


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def inquires_handler(request):

    fullname = request.data.get("fullName")
    phone_number = request.data.get("phoneNumber")
    email = request.data.get("email")
    message = request.data.get("message")

    models.Inquiry.objects.create(
        fullname=fullname, phone_number=phone_number, email=email, message=message
    ).save()

    return Response(status=status.HTTP_200_OK)
