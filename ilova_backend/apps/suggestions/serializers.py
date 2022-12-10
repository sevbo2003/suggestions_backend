from rest_framework import serializers
from apps.suggestions.models import ProblemType, Problem, Status, Location
from core.geo_finder import get_location
from django.contrib.auth import get_user_model


User = get_user_model()


class ProblemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemType
        fields = ("id", "name")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'lon', 'lat']


class ProblemSerializer(serializers.ModelSerializer):
    problem_types = serializers.SerializerMethodField()
    location = LocationSerializer()

    class Meta:
        model = Problem
        fields = ['id', 'user', 'city', 'district', 'date', 'problem_types', 'images','description', 'status', 'location']
        read_only_fields = ['id','user', 'city', 'district', 'date']
    
    def get_problem_types(self, obj):
        return ProblemTypeSerializer(obj.problem_types.all(), many=True).data
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class CreateProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'user', 'city', 'district', 'date', 'problem_types', 'images','description', 'status', 'location']
        read_only_fields = ['id','user', 'city', 'district', 'date', 'status']
    
    def create(self, validated_data):
        problem_types = validated_data.pop('problem_types')
        validated_data['city'], validated_data['district'] = get_location(str(validated_data['location'].lon), str(validated_data['location'].lat))
        problem = Problem.objects.create(**validated_data)
        for problem_type in problem_types:
            problem.problem_types.add(problem_type)
        return problem
