from django.db import models

class RainwaterCalculation(models.Model):
    roof_area = models.FloatField()
    rainfall = models.FloatField()
    efficiency = models.FloatField()
    collected_water = models.FloatField()
    created_at = models.DateTimeField(
        auto_now_add=True
)

def __str__(self):
    return f"Rainwater #{self.id}"

