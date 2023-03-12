from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
)
from rest_framework.views import APIView
from . import models, serializers


@api_view(["POST"])
def logout_handler(request):
    refresh_token = request.data.get("refresh_token")
    token = RefreshToken(refresh_token)
    request.user.is_logged_in = False
    request.user.save()
    token.blacklist()
    return Response(status=status.HTTP_205_RESET_CONTENT)


@api_view(["GET"])
def allowed_views_handler(request):
    allowed_views = models.AllowedView.objects.all().order_by("-created_at")
    allowed_views_serializer = serializers.AllowedViewSerializer(
        allowed_views, many=True
    )

    return Response(status=status.HTTP_200_OK, data=allowed_views_serializer.data)


class AccountHandler(APIView):
    def get(self, request):
        users = models.User.objects.all().order_by("-date_joined")
        users_serializer = serializers.UserSerializer(users, many=True)

        return Response(status=status.HTTP_200_OK, data=users_serializer.data)

    def post(self, request):

        first_name = request.data.get("firstName")
        last_name = request.data.get("lastName")
        email = request.data.get("email")
        username = request.data.get("userName")
        password = request.data.get("password")
        role = request.data.get("role")

        allowed_views = request.data.get("allowedViews")

        user = models.User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            role=role,
        )

        for allowed_view in allowed_views:
            user.allowed_views.add(
                models.AllowedView.objects.get(slug=allowed_view["id"])
            )

        user.save()

        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def account_details_handler(request):
    logged_in_user = request.user
    request.user.is_logged_in = True
    request.user.save()
    user_serializer = serializers.UserSerializer(logged_in_user)

    return Response(status=status.HTTP_200_OK, data=user_serializer.data)


@api_view(["GET"])
def active_users_data(request):
    active_users = models.User.objects.filter(is_logged_in=True)
    active_users_serializer = serializers.UserSerializer(active_users, many=True)

    return Response(status=status.HTTP_200_OK, data=active_users_serializer.data)
