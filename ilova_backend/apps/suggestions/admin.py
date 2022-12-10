from django.contrib import admin
from apps.suggestions.models import ProblemType, Problem, Location


@admin.register(ProblemType)
class ProblemTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "city", "district", "date", "status")
    search_fields = ("id", "user", "city", "district", "date", "status")
    list_filter = ("status",)
    readonly_fields = ("id", "city", "district", "date")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'lon', 'lat']
