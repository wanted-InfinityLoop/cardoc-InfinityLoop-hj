from django.db import models


class User(models.Model):
    id       = models.CharField(primary_key=True, unique=True, max_length=32)
    password = models.CharField(max_length=64)
    car      = models.ForeignKey("cars.Car", null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "users"
