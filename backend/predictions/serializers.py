from rest_framework import serializers
from .models import LeafSample, SoilSample, Prediction

class LeafSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeafSample
        fields = '__all__'

class SoilSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilSample
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'