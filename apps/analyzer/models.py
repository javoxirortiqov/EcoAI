from django.db import models


class Analysis(models.Model):
    image = models.ImageField(
        upload_to="uploads/"
    )

    result = models.TextField(
        blank=True
    )

    recommendation = models.TextField(
        blank=True
    )

    confidence = models.FloatField(
        default=0
    )

    eco_score = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"EcoAI Analysis #{self.id}"