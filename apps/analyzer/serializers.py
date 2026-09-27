from django.shortcuts import render, redirect
from .models import Analysis


def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')

        if image:
            analysis = Analysis.objects.create(
                image=image
            )
            return redirect('analysis_result', analysis_id=analysis.id)

    return render(request, 'analyzer/upload.html')


def analysis_result(request, analysis_id):
    analysis = Analysis.objects.get(id=analysis_id)

    return render(
        request,
        'analyzer/result.html',
        {'analysis': analysis}
    )