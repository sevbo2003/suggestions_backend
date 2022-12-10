from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.suggestions.models import ProblemType, Problem, Status
from apps.suggestions.serializers import ProblemTypeSerializer, ProblemSerializer, CreateProblemSerializer
from apps.suggestions.filters import ProblemFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model

User = get_user_model()


class ProblemTypeViewSets(viewsets.ModelViewSet):
    queryset = ProblemType.objects.all()
    serializer_class = ProblemTypeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'head', 'options']


class ProblemViewSets(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filterset_class = ProblemFilter

    @action(detail=False, methods=['get'])
    def count_problems_by_status(self, request):
        return Response({
            "all": self.get_queryset().count(),
            "solved": self.get_queryset().filter(status=Status.SOLVED).count(),
            "pending": self.get_queryset().filter(status=Status.PENDING).count(),
            "fake": self.get_queryset().filter(status=Status.FAKE).count()
        })

    def destroy(self, request, *args, **kwargs):
        problem = self.get_object()
        if problem.user == request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"detail": "You don't have permission to do this operation"}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        problem = self.get_object()
        if problem.user == request.user:
            updated_status = request.data.get('status')
            problem.status = updated_status
            problem.save()
            serializer = ProblemSerializer(problem)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You don't have permission to do this operation"}, status=status.HTTP_403_FORBIDDEN)
    
    def get_serializer_class(self):
        return super().get_serializer_class() if self.request.method == 'GET' else CreateProblemSerializer