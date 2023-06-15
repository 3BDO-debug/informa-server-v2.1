import random
import string
import dateutil.parser
from datetime import datetime
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ast import literal_eval
from . import utils, models, serializers
from accounts.models import User
from nutrition_plan_algorithm.models import (
    NutritionPlan,
    NutritionPlanMeal,
)
from nutrition_plan_algorithm.serializers import NutritionPlanMealSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def clients_data_handler(request):
    subscription_id = request.data.get("id")
    weight = int(request.data.get("weight"))
    height = int(request.data.get("height"))
    age = int(request.data.get("age"))
    body_fat = int(request.data.get("fatPercentage"))
    body_fat_calc_method = request.data.get("bodyFatCalcMethod")
    training_volume = request.data.get("trainingVolume")
    activity_per_day = request.data.get("activityPerDay")
    goal = request.data.get("goal")
    excluded_food_items = literal_eval(request.data.get("excludedFoodItems"))
    can_take_protein_supplement = True

    number_of_meals = int(request.data.get("numberOfMeals"))

    activity_level_value = utils.activity_level_value_calculator(
        user_training_volume=training_volume, user_activity_per_day=activity_per_day
    )

    total_calories = utils.total_calories_calculator(
        user_weight=weight,
        user_body_fat=body_fat,
        activity_level_value=activity_level_value,
    )["total_calories"]

    bmr = utils.total_calories_calculator(
        user_weight=weight,
        user_body_fat=body_fat,
        activity_level_value=activity_level_value,
    )["bmr"]

    total_deficit_calories = utils.deficit_calories_calculator(
        total_calories=total_calories, user_goal=goal, user_body_fat=body_fat
    )

    lean_body_mass = utils.total_calories_calculator(
        user_weight=weight,
        user_body_fat=body_fat,
        activity_level_value=activity_level_value,
    )["lean_body_mass"]

    protein_grams = utils.protein_macros_calculator(
        user_lean_body_mass=lean_body_mass, user_goal=goal, user_body_fat=body_fat
    )

    fat_grams = utils.fat_macros_calculator(
        user_calories_deficit=total_deficit_calories, user_goal=goal
    )

    carb_grams = utils.carb_macros_calculator(
        user_calories_deficit=total_deficit_calories,
        protein_macros=protein_grams,
        fat_macros=fat_grams,
    )

    """ Creating client instance """

    client = models.Client.objects.get(subscription_id=subscription_id)

    """ Creating client data """
    client_data = models.ClientData.objects.filter(client=client)

    if len(client_data) > 0:
        """Find the client data that is set to active"""
        active_client_data = client_data.get(generate_using_this_data=True)
        active_client_data.generate_using_this_data = False
        active_client_data.save()

    client_data_obj = models.ClientData.objects.create(
        client=client,
        weight=weight,
        height=height,
        age=age,
        body_fat=body_fat,
        body_fat_calc_method=body_fat_calc_method,
        training_volume=training_volume,
        activity_per_day=activity_per_day,
        goal=goal,
        preferred_schema="Re-composition",
        can_take_protein_supplement=can_take_protein_supplement,
        water_in_take=weight * 0.45,
        number_of_meals=number_of_meals,
        lean_body_mass=lean_body_mass,
        bmr=bmr,
        total_calories=total_calories,
        calories_deficit=total_deficit_calories,
        protein_grams=protein_grams,
        fat_grams=fat_grams,
        carb_grams=carb_grams,
        generate_using_this_data=True,
    )

    if len(excluded_food_items) > 0:
        for food_item in excluded_food_items:
            client_data_obj.excluded_food_items.add(food_item)

    client.save()
    client_data_obj.save()

    return Response(status=status.HTTP_201_CREATED)


class ClientsDataHandler(APIView):
    def get(self, request, format=None):
        clients_data = models.Client.objects.all()
        clients_data_serializer = serializers.ClientSerializer(clients_data, many=True)

        return Response(data=clients_data_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        subscription_id = request.data.get("subscriptionId")
        first_name = request.data.get("firstName")
        last_name = request.data.get("lastName")
        email = request.data.get("email")
        username = request.data.get("userName")
        password = request.data.get("password")
        phone_number = request.data.get("phoneNumber")
        plan_type = request.data.get("planType")
        plan_duration = request.data.get("planDuration")
        follow_up_package = request.data.get("followUpPackage")

        """ Create user instance """

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            role="client",
        )

        models.Client.objects.create(
            user=user,
            subscription_id=subscription_id,
            phone_number=phone_number,
            follow_up_package=follow_up_package,
            plan_type=plan_type,
            plan_duration=plan_duration,
        ).save()

        user.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        client_id = request.query_params.get("clientId")

        """ Delete client """
        client = models.Client.objects.get(id=int(client_id))

        client.user.delete()

        return Response(status=status.HTTP_200_OK)


class ClientDataHandler(APIView):
    def get(
        self,
        request,
        client_id,
    ):
        client_data = models.Client.objects.get(id=client_id)
        client_data_serializer = serializers.ClientSerializer(client_data, many=False)
        client_macros = models.ClientData.objects.filter(client=client_data)
        if client_macros.exists():
            client_macros = client_macros.get(generate_using_this_data=True)
            client_macros_serializer = serializers.ClientDataSerializer(
                client_macros, many=False
            ).data

        else:
            client_macros_serializer = []

        return Response(
            data={
                "client_data": client_data_serializer.data,
                "client_computed_macros": client_macros_serializer,
            },
            status=status.HTTP_200_OK,
        )


class ClientMacrosDataHandler(APIView):
    def get(self, request):
        client = models.Client.objects.get(id=int(request.query_params.get("clientId")))
        client_macros_data = models.ClientData.objects.filter(client=client).order_by(
            "-timestamp"
        )
        client_macros_data_serializer = serializers.ClientDataSerializer(
            client_macros_data, many=True
        )

        return Response(
            data=client_macros_data_serializer.data, status=status.HTTP_200_OK
        )


@api_view(["GET"])
def generate_client_subscription_id(request):
    prefix = "INFORMA"
    clients_count = models.Client.objects.count()
    client_index = clients_count + 1
    unique_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    subscription_id = f"{prefix}-{client_index:04d}-{unique_part}"

    return Response(status=status.HTTP_200_OK, data=subscription_id)


@api_view(["GET"])
def get_client_nutrition_plan_meals_handler(request):
    nutrition_plan_id = int(request.query_params.get("nutritionPlanId"))
    meal_index = request.query_params.get("mealIndex")

    active_nutrition_plan = get_object_or_404(NutritionPlan, id=nutrition_plan_id)
    generated_at_date = active_nutrition_plan.generated_at
    today = datetime.today()
    days_difference = (today - generated_at_date.replace(tzinfo=None)).days
    day_index = days_difference % 7 + 1
    week_index = (days_difference // 7) + 1

    nutrition_plan_meals = active_nutrition_plan.nutritionplanmeal_set.all()

    if active_nutrition_plan.schema in ["PSMF", "Carb cycle"]:
        meal_category = "refeed_meals" if day_index == 7 else "high_carb_days_meals"
        nutrition_plan_meals = nutrition_plan_meals.filter(meal_category=meal_category)
    elif active_nutrition_plan.schema == "Refeed":
        if (week_index == 1 and day_index == 7) or (
            week_index == 3 and day_index in [6, 7]
        ):
            nutrition_plan_meals = nutrition_plan_meals.filter(
                Q(meal_category="refeed_meals") | Q(meal_index="refeed_snack")
            )
        else:
            nutrition_plan_meals = nutrition_plan_meals.filter(
                Q(meal_category="main_meals") | Q(meal_index="snack")
            )
    elif active_nutrition_plan.schema == "Balanced":
        nutrition_plan_meals = nutrition_plan_meals.filter(meal_category="main_meals")

    if meal_index == "snack":
        nutrition_plan_meals = NutritionPlanMeal.objects.filter(
            nutrition_plan=active_nutrition_plan, meal_index="snack"
        )
    else:
        nutrition_plan_meals = nutrition_plan_meals.filter(meal_index=meal_index)

    nutrition_plan_meals_serializer = NutritionPlanMealSerializer(
        nutrition_plan_meals, many=True
    )

    return Response(
        status=status.HTTP_200_OK, data=nutrition_plan_meals_serializer.data
    )


class MealInTakeTracking(APIView):
    def get(self, request):
        client = models.Client.objects.get(user=request.user)
        client_data = models.ClientData.objects.filter(
            client=client, generate_using_this_data=True
        ).first()

        daily_calories = client_data.calories_deficit
        meals_taken = models.MealIntake.objects.filter(
            client=client,
            timestamp__date=datetime.today().date(),
        )

        for meal in meals_taken:
            meal_macros = NutritionPlanMealSerializer(meal.meal, many=False).data
            daily_calories -= meal_macros["total_macros"].get("total_calories")

        return Response(
            status=status.HTTP_200_OK,
            data={
                "remaining_meals": client_data.number_of_meals
                - meals_taken.exclude(meal__meal_category="snacks").count(),
                "remaining_calories": int(daily_calories),
            },
        )

    def post(self, request):
        client = models.Client.objects.get(user=request.user)
        meal = NutritionPlanMeal.objects.get(id=int(request.data.get("mealId")))

        models.MealIntake.objects.create(
            client=client, meal=meal, meal_image=request.data.get("mealImage")
        ).save()

        return Response(status=status.HTTP_200_OK)


class WaterInTakeTracking(APIView):
    def get(self, request):
        client = models.Client.objects.get(user=request.user)
        client_data = models.ClientData.objects.get(
            client=client, generate_using_this_data=True
        )

        daily_water_in_take = client_data.water_in_take
        water_in_take_records = models.WaterInTake.objects.filter(
            client=client, timestamp__date=datetime.today().date()
        )

        water_in_take = 0

        for water_in_take_record in water_in_take_records:
            water_in_take += water_in_take_record.in_take

        return Response(
            status=status.HTTP_200_OK, data={"water_in_take": water_in_take}
        )

    def post(self, request):
        client = models.Client.objects.get(user=request.user)
        water_in_take = request.data

        models.WaterInTake.objects.create(
            client=client, in_take=float(water_in_take)
        ).save()

        return Response(status=status.HTTP_200_OK)


class ClientsFollowUpHandler(APIView):
    def get(self, request):
        user = request.user

        if user.role != "coach":
            clients_follow_ups = models.ClientFollowUp.objects.filter(is_active=True)
        elif user.role == "coach":
            clients_follow_ups = models.ClientFollowUp.objects.filter(
                is_active=True, coach=user
            )

        clients_follow_ups_serializer = serializers.ClientFollowUpSerializer(
            clients_follow_ups, many=True
        )

        return Response(
            status=status.HTTP_200_OK, data=clients_follow_ups_serializer.data
        )

    def post(self, request):
        client = models.Client.objects.get(id=int(request.data.get("clientId")))
        note = request.data.get("note")
        scheduled_time = dateutil.parser.parse(request.data.get("followUpTime")).time()

        coach = User.objects.get(id=int(request.data.get("coach")["id"]))

        client_follow_ups = models.ClientFollowUp.objects.filter(
            client=client, is_active=True
        )

        for client_follow_up in client_follow_ups:
            client_follow_up.is_active = False
            client_follow_up.save()

        models.ClientFollowUp.objects.create(
            client=client,
            coach=coach,
            note=note,
            status="initial",
            scheduled_time=scheduled_time,
            is_active=True,
        ).save()

        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        follow_up = models.ClientFollowUp.objects.get(
            id=int(request.data.get("followUpId"))
        )

        follow_up.status = request.data.get("status")

        follow_up.save()

        return Response(status=status.HTTP_200_OK)
