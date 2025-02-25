from rest_framework import serializers
from memristorsimulation_app.serializers.baseserializers import CamelCaseSerializer


class ModelParametersSerializer(CamelCaseSerializer):
    alpha = serializers.FloatField()
    beta = serializers.FloatField()
    rinit = serializers.FloatField()
    roff = serializers.FloatField()
    ron = serializers.FloatField()
    vt = serializers.FloatField()
