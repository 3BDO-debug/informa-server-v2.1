"""based_on_tech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path/
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from personal_training.handlers import personal_training_requests_injector

urlpatterns = [
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # jwt auth
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # jwt auth
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("personal-training/", include("personal_training.urls")),
    path("inquires/", include("inquires.urls")),
    path("offers/", include("offers.urls")),
    path("programs-generator/", include("programs_generator.urls")),
    path("meals/", include("meals.urls")),
    path("inject-requests/", personal_training_requests_injector),
    path("system-logs/", include("system_logs.urls")),
    path("tasks/", include("tasks.urls")),
]

admin.site.site_header = "Informa administration"


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
