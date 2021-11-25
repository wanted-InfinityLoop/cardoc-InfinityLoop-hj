from django.db import models


class Car(models.Model):
    name      = models.CharField(max_length=32)
    brand     = models.CharField(max_length=32)
    year_type = models.PositiveIntegerField()

    class Meta:
        db_table = "cars"


class FrontTire(models.Model):
    name         = models.CharField(max_length=16)
    width        = models.PositiveIntegerField()
    aspect_ratio = models.PositiveIntegerField()
    wheel_size   = models.PositiveIntegerField()

    class Meta:
        db_table = "front_tires"


class RearTire(models.Model):
    name         = models.CharField(max_length=16)
    width        = models.PositiveIntegerField()
    aspect_ratio = models.PositiveIntegerField()
    wheel_size   = models.PositiveIntegerField()

    class Meta:
        db_table = "rear_tires"

class Spec(models.Model):
    car        = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="spec")
    front_tire = models.ForeignKey(FrontTire, null=True, on_delete=models.SET_NULL)
    rear_tire  = models.ForeignKey(RearTire, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "specs"

