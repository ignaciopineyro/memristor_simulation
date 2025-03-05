from rest_framework import serializers
from memristorsimulation_app.serializers.baseserializers import CamelCaseSerializer


class ModelParametersSerializer(CamelCaseSerializer):
    alpha = serializers.FloatField()
    beta = serializers.FloatField()
    rinit = serializers.FloatField()
    roff = serializers.FloatField()
    ron = serializers.FloatField()
    vt = serializers.FloatField()


class ModelSerializer(CamelCaseSerializer):
    model = serializers.CharField()


class InputParametersSerializer(CamelCaseSerializer):
    model_parameters = ModelParametersSerializer()
    model = ModelSerializer()
