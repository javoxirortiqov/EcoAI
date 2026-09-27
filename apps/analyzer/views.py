from django.shortcuts import render, redirect, get_object_or_404

from .models import Analysis
from .ai import analyze_environment_image


def upload_image(request):

    if request.method == "POST":

        image = request.FILES.get("image")

        if image:

            analysis = Analysis.objects.create(
                image=image
            )

            try:

                data = analyze_environment_image(
                    analysis.image.path
                )

                analysis.result = (
                    f"MUAMMO:\n"
                    f"{data.get('problem', '')}\n\n"
                    f"TAFSILOT:\n"
                    f"{data.get('details', '')}"
                )

                analysis.recommendation = (
                    f"YECHIM:\n"
                    f"{data.get('solution', '')}\n\n"
                    f"TAVSIYA:\n"
                    f"{data.get('recommendation', '')}"
                )

                analysis.eco_score = int(
                    data.get("eco_score", 0)
                )

                analysis.confidence = float(
                    data.get("confidence", 0)
                )

                analysis.save()

            except Exception as error:

                analysis.result = (
                    f"AI tahlilida xatolik:\n\n"
                    f"{error}"
                )

                analysis.recommendation = (
                    "API key va OpenAI sozlamalarini tekshiring."
                )

                analysis.save()

            return redirect(
                "analysis_result",
                analysis_id=analysis.id
            )

    return render(
        request,
        "analyzer/upload.html"
    )


def analysis_result(request, analysis_id):

    analysis = get_object_or_404(
        Analysis,
        id=analysis_id
    )

    return render(
        request,
        "analyzer/result.html",
        {
            "analysis": analysis
        }
    )