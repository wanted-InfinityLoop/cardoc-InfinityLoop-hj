from django.urls import path, include

urlpatterns = [
    path("user", include("users.urls")),
    path("car", include("cars.urls")),
]

