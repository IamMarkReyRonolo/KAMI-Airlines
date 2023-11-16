from django.db import models


# add rules
# Create your models here.
class Airplane(models.Model):
    id = models.IntegerField(primary_key=True)
    no_of_passengers = models.IntegerField()
    fuel_tank_capacity_in_liters = models.FloatField()
    fuel_consumption_per_minute = models.FloatField()
    maximum_minutes_to_fly = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            "-updated_at",
            "-created_at",
        )

    def __str__(self):
        return self.first_name + " " + self.last_name
