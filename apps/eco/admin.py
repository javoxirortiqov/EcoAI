from django.contrib import admin

from .models import RainwaterCalculation

@admin.register(RainwaterCalculation)
class RainwaterCalculationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "roof_area",
        "rainfall",
        "efficiency",
        "collected_water",
        "created_at",
)

ordering = (
    "-created_at",
)
