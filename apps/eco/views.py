from django.shortcuts import render
from .models import RainwaterCalculation


def rainwater_calculator(request):
    result = None

    if request.method == "POST":
        roof_area = float(request.POST.get("roof_area", 0))
        rainfall = float(request.POST.get("rainfall", 0))
        efficiency = float(request.POST.get("efficiency", 0))

        collected_water = roof_area * rainfall * efficiency

        RainwaterCalculation.objects.create(
            roof_area=roof_area,
            rainfall=rainfall,
            efficiency=efficiency,
            collected_water=collected_water
        )

        result = {
            "liters": round(collected_water),
            "roof_area": roof_area,
            "rainfall": rainfall,
            "efficiency": efficiency * 100
        }

    return render(
        request,
        "eco/rainwater.html",
        {"result": result}
    )