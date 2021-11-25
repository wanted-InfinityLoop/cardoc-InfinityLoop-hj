from django.urls import path
from cars.views import CarView

urlpatterns = [
    path('/tire', CarView.as_view()),
]
