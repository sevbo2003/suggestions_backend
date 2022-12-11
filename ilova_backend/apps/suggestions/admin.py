from django.contrib import admin
from apps.suggestions.models import ProblemType, Problem, Location, ProblemImages


@admin.register(ProblemType)
class ProblemTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ProblemImages)
class ProblemImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "problem", "image")
    search_fields = ("id", "problem", "image")
    list_filter = ("problem",)
    readonly_fields = ("id", "problem", "image")


class ProblemImagesInline(admin.TabularInline):
    model = ProblemImages
    extra = 1


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "city", "district", "date", "status")
    search_fields = ("id", "user", "city", "district", "date", "status")
    list_filter = ("status",)
    readonly_fields = ("id", "city", "district", "date")
    inlines = [ProblemImagesInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'lon', 'lat']
