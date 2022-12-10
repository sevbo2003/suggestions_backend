from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.suggestions.views import ProblemTypeViewSets, ProblemViewSets

router = DefaultRouter()

router.register('problems', ProblemViewSets, basename='problems')
router.register('problem_types', ProblemTypeViewSets, basename='problem-types')


urlpatterns = [
    path('', include(router.urls))
]