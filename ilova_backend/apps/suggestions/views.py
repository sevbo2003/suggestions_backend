from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.suggestions.models import ProblemType, Problem, Status, Location
from apps.suggestions.serializers import ProblemTypeSerializer, ProblemSerializer, CreateProblemSerializer, LocationSerializer
from apps.suggestions.filters import ProblemFilter
from core.geo_finder import get_location
from core.last_day_of_month import last_day_of_month
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


class ProblemTypeViewSets(viewsets.ModelViewSet):
    queryset = ProblemType.objects.all()
    serializer_class = ProblemTypeSerializer
    http_method_names = ['get', 'head', 'options']
    permission_classes = [IsAuthenticated]



class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ['get', 'post', 'head', 'options']
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        lon = serializer.data['lon']
        lat = serializer.data['lat']
        city, district = get_location(str(lon), str(lat))
        return Response({
            "id": serializer.data['id'],
            "lon": lon,
            "lat": lat,
            "city": city,
            "district": district
        }, status=status.HTTP_201_CREATED)


class ProblemViewSets(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filterset_class = ProblemFilter
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        return Response({
            "all": self.get_queryset().count(),
            "solved": self.get_queryset().filter(status=Status.SOLVED).count(),
            "pending": self.get_queryset().filter(status=Status.PENDING).count(),
            "fake": self.get_queryset().filter(status=Status.FAKE).count()
        })
    
    @action(detail=False, methods=['get'])
    def count_problems_by_city(self, request):
        city = request.query_params.get('city')
        if city:
            return Response({
                "all": self.get_queryset().filter(city=city).count(),
                "solved": self.get_queryset().filter(city=city, status=Status.SOLVED).count(),
                "pending": self.get_queryset().filter(city=city, status=Status.PENDING).count(),
                "fake": self.get_queryset().filter(city=city, status=Status.FAKE).count()
            })
        return Response({"detail": "City is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def pending_problems(self, request):
        uzb_cities = ['Toshkent', 'Andijon', 'Buxoro', 'Farg\'ona', 'Jizzax', 'Namangan', 'Navoiy', 'Qashqadaryo', 'Qoraqalpog\'iston Respublikasi', 'Samarqand', 'Sirdaryo', 'Surxondaryo', 'Xorazm']
        # [{i: self.get_queryset().filter(city=i, status=Status.PENDING).count()} for i in uzb_cities]
        result = []
        for i in uzb_cities:
            count = self.get_queryset().filter(city=i, status=Status.PENDING).count()
            if count != 0:
                result.append({i: count})
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def solved_problems(self, request):
        uzb_cities = ['Toshkent', 'Andijon', 'Buxoro', 'Farg\'ona', 'Jizzax', 'Namangan', 'Navoiy', 'Qashqadaryo', 'Qoraqalpog\'iston Respublikasi', 'Samarqand', 'Sirdaryo', 'Surxondaryo', 'Xorazm']
        result = []
        for i in uzb_cities:
            count = self.get_queryset().filter(city=i, status=Status.SOLVED).count()
            if count != 0:
                result.append({i: count})
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def graph(self, request):
        if request.query_params.get('monthly'):
            if request.query_params.get('monthly') == 'true':
                month_list = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr']
                result = []
                for i in month_list:
                    count = self.get_queryset().filter(date__month=month_list.index(i)+1).count()
                    result.append({i: {
                        "all": count,
                        "solved": self.get_queryset().filter(date__month=month_list.index(i)+1, status=Status.SOLVED).count(),
                        "pending": self.get_queryset().filter(date__month=month_list.index(i)+1, status=Status.PENDING).count(),
                        "fake": self.get_queryset().filter(date__month=month_list.index(i)+1, status=Status.FAKE).count()
                    }})
                return Response(result, status=status.HTTP_200_OK)
        if request.query_params.get('daily'):
            if request.query_params.get('daily') == 'true':
                result = []
                max_day_in_month = last_day_of_month(datetime.date.today()).month
                for i in range(1, max_day_in_month + 1):
                    count = self.get_queryset().filter(date__day=i).count()
                    result.append({i: {
                        "all": count,
                        "solved": self.get_queryset().filter(date__day=i, status=Status.SOLVED).count(),
                        "pending": self.get_queryset().filter(date__day=i, status=Status.PENDING).count(),
                        "fake": self.get_queryset().filter(date__day=i, status=Status.FAKE).count()
                    }})
                return Response(result, status=status.HTTP_200_OK)
        return Response({"detail": "Filter parametr is required"}, status=status.HTTP_400_BAD_REQUEST)

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