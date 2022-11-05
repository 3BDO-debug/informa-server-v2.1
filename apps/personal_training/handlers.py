from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


@api_view(["POST"])
def personal_training_requests_handler(request):
    fullname = request.data.get("fullname")
    phone_number = request.data.get("whatsappNumber")
    cor = request.data.get("cor")
    payment_currency = request.data.get("paymentCurrency")
    age = request.data.get("age")
    gender = request.data.get("gender")
    weight = int(request.data.get("weight"))
    height = float(request.data.get("height"))
    plan_program = request.data.get("planProgram")
    plan_duration = request.data.get("planDuration")
    followup_package = request.data.get("followUpPackage")
    computed_total_price = float(request.data.get("computedTotalPrice"))

    models.PersonalTrainingRequest.objects.create(
        fullname=fullname,
        phone_number=phone_number,
        cor=cor,
        payment_currency=payment_currency,
        age=age,
        gender=gender,
        weight=weight,
        height=height,
        plan_program=plan_program,
        plan_duration=plan_duration,
        followup_package=followup_package,
        computed_total_price=computed_total_price,
    ).save()

    return Response(status=status.HTTP_200_OK)
