from django.contrib import admin
from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'result',
        'confidence',
        'created_at',
    ]
    list_filter = [
        'created_at',
    ]
    search_fields = [
        'result',
        'recommendation',
    ]