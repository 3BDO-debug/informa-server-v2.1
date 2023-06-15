import json
from datetime import datetime
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import HttpResponse
from . import models, serializers
from accounts.models import User
from tasks.handlers import user_got_turn


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def personal_training_requests_handler(request):
    fullname = request.data.get("fullname")
    phone_number = request.data.get("whatsappNumber")
    cor = request.data.get("cor")
    paying_region = request.data.get("payingRegion")
    age = request.data.get("age")
    gender = request.data.get("gender")
    weight = int(request.data.get("weight"))
    height = float(request.data.get("height"))
    plan_program = request.data.get("planProgram")
    plan_duration = request.data.get("planDuration")
    followup_package = request.data.get("followUpPackage")
    computed_total_price = float(request.data.get("computedTotalPrice"))
    computed_price_after_sale = (
        float(request.data.get("computedPriceAfterSale"))
        if request.data.get("computedPriceAfterSale")
        else None
    )
    has_sale = bool(computed_price_after_sale)

    staff_member = user_got_turn()

    if models.PersonalTrainingRequest.objects.filter(phone_number=phone_number):
        client_request = models.PersonalTrainingRequest.objects.filter(
            phone_number=phone_number
        ).order_by("-timestamp")[0]

        days_diff = abs((datetime.now().date() - client_request.timestamp.date()).days)

        if days_diff > 3:
            models.PersonalTrainingRequest.objects.create(
                fullname=fullname,
                phone_number=phone_number,
                cor=cor,
                paying_region=paying_region,
                age=age,
                gender=gender,
                weight=weight,
                height=height,
                plan_program=plan_program,
                plan_duration=plan_duration,
                followup_package=followup_package,
                computed_total_price=computed_total_price,
                computed_price_after_sale=computed_price_after_sale,
                has_sale=has_sale,
                assigned_to=staff_member,
            ).save()
        else:
            return Response(status=status.HTTP_200_OK, data={"spamming": True})
    else:
        models.PersonalTrainingRequest.objects.create(
            fullname=fullname,
            phone_number=phone_number,
            cor=cor,
            paying_region=paying_region,
            age=age,
            gender=gender,
            weight=weight,
            height=height,
            plan_program=plan_program,
            plan_duration=plan_duration,
            followup_package=followup_package,
            computed_total_price=computed_total_price,
            computed_price_after_sale=computed_price_after_sale,
            has_sale=has_sale,
            assigned_to=staff_member,
        ).save()
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def personal_training_requests_data(request):
    user = request.user

    if user.role == "manager" or user.is_superuser:
        personal_training_requests = (
            models.PersonalTrainingRequest.objects.all().order_by("-timestamp")
        )
        personal_training_requests_serializer = (
            serializers.PersonalTrainingRequestSerializer(
                personal_training_requests, many=True
            )
        )
    else:
        personal_training_requests = models.PersonalTrainingRequest.objects.filter(
            assigned_to=user
        ).order_by("-timestamp")
        personal_training_requests_serializer = (
            serializers.PersonalTrainingRequestSerializer(
                personal_training_requests, many=True
            )
        )

    return Response(
        status=status.HTTP_200_OK, data=personal_training_requests_serializer.data
    )


def personal_training_requests_injector(request):
    main_db = requests.get(
        "https://informa-server.herokuapp.com/personal-training/personal-training-requests-data"
    )
    data = json.loads(main_db.content)

    for request in data:
        models.PersonalTrainingRequest.objects.create(
            fullname=request["fullname"],
            phone_number=request["phone_number"],
            cor=request["cor"],
            paying_region=request["paying_region"],
            age=request["age"],
            gender=request["gender"],
            weight=request["weight"],
            height=request["height"],
            plan_program=request["plan_program"],
            plan_duration=request["plan_duration"],
            followup_package=request["followup_package"],
            computed_total_price=request["computed_total_price"],
            computed_price_after_sale=request["computed_price_after_sale"],
            has_sale=request["has_sale"],
            timestamp=request["timestamp"],
            proceeded=request["proceeded"],
        ).save()

    return HttpResponse("done")


@api_view(["POST"])
def assign_personal_training_request_handler(request):
    number_of_tasks_to_be_assigned = int(request.data.get("numberOfTasksToBeAssigned"))
    staff_account_id = request.data.get("staffAccountId")

    related_staff_account = User.objects.get(id=int(staff_account_id))

    unassigned_tasks = models.PersonalTrainingRequest.objects.filter(
        proceeded=False
    ).filter(assigned_to=None)[0:number_of_tasks_to_be_assigned]

    for task in unassigned_tasks:
        task.assigned_to = related_staff_account
        task.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def proceed_personal_training_request(request):
    request_id = request.data.get("requestId")

    personal_training_request = models.PersonalTrainingRequest.objects.get(
        id=int(request_id)
    )

    personal_training_request.proceeded = True
    personal_training_request.proceeded_at = datetime.now()
    personal_training_request.save()

    return Response(status=status.HTTP_200_OK)
