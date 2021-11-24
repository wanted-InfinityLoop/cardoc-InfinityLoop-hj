from django.db import models


class Car(models.Model):
    name      = models.CharField(max_length=32)
    brand     = models.CharField(max_length=32)
    year_type = models.PositiveIntegerField()


class FrontTire(models.Model):
    name         = models.CharField(max_length=16)
    width        = models.PositiveIntegerField()
    aspect_ratio = models.PositiveIntegerField()
    wheel_size   = models.PositiveIntegerField()


class RearTire(models.Model):
    name         = models.CharField(max_length=16)
    width        = models.PositiveIntegerField()
    aspect_ratio = models.PositiveIntegerField()
    wheel_size   = models.PositiveIntegerField()


class Spec(models.Model):
    car        = models.OneToOneField(Car, on_delete=models.CASCADE)
    front_tire = models.ForeignKey(FrontTire, null=True, on_delete=models.SET_NULL)
    back_tire  = models.ForeignKey(RearTire, null=True, on_delete=models.SET_NULL)

