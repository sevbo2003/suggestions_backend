from rest_framework import serializers
from apps.suggestions.models import ProblemType, Problem, Location, ProblemImages
from apps.notification.serializers import MahallaSerializer
from core.geo_finder import get_location
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class ProblemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemType
        fields = ("id", "name")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'lon', 'lat']
    

class ProblemImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemImages
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    problem_types = serializers.SerializerMethodField()
    location = LocationSerializer()
    images = serializers.SerializerMethodField()
    mahalla = MahallaSerializer()

    class Meta:
        model = Problem
        fields = ['id', 'user', 'city', 'district', 'date', 'problem_types', 'images', 'description', 'status', 'location', 'mahalla']
        read_only_fields = ['id','user', 'city', 'district', 'date']
    
    def get_problem_types(self, obj):
        return ProblemTypeSerializer(obj.problem_types.all(), many=True).data
    
    def get_images(self, obj):
        return [settings.SITE_URL + obj.image.url for obj in obj.images.all()]
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class CreateProblemSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(write_only=True, child=serializers.ImageField(allow_empty_file = False, use_url = False))

    class Meta:
        model = Problem
        fields = ['id', 'user', 'city', 'district', 'date', 'problem_types', 'images','uploaded_images', 'description', 'status', 'location', 'mahalla']
        read_only_fields = ['id','user', 'city', 'district', 'date', 'status']
    
    def get_images(self, obj):
        return [settings.SITE_URL + obj.image.url for obj in obj.images.all()]

    def create(self, validated_data):
        problem_types = validated_data.pop('problem_types')
        uploaded_data = validated_data.pop('uploaded_images')
        validated_data['city'], validated_data['district'] = get_location(str(validated_data['location'].lon), str(validated_data['location'].lat))
        mahalla = validated_data['mahalla']
        if mahalla is not None:
            user = self.context['request'].user
            user.mahallalar.add(mahalla)
            user.save()
        problem = Problem.objects.create(**validated_data)
        for problem_type in problem_types:
            problem.problem_types.add(problem_type)
        for image in uploaded_data:
            ProblemImages.objects.create(problem=problem, image=image)
        return problem
