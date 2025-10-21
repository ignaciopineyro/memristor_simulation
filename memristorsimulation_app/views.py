import json

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from memristorsimulation_app.serializers.simulation import SimulationInputsSerializer
from django.shortcuts import render
from memristorsimulation_app.services.simulationservice import SimulationService
from .forms import ModelParametersForm


class SimulationView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        serializer = SimulationInputsSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        SimulationService(request_parameters=validated_data).simulate()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        form = ModelParametersForm()
        return render(request, "form.html", {"form": form})
