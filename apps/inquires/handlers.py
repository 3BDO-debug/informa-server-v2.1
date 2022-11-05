from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models


@api_view(["POST"])
def inquires_handler(request):

    fullname = request.data.get("fullName")
    phone_number = request.data.get("phoneNumber")
    email = request.data.get("email")
    message = request.data.get("message")

    models.Inquiry.objects.create(
        fullname=fullname, phone_number=phone_number, email=email, message=message
    ).save()

    return Response(status=status.HTTP_200_OK)
