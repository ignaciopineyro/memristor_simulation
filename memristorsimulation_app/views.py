import json

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from memristorsimulation_app.serializers.simulation import SimulationInputsSerializer
from django.shortcuts import render

from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.services.simulationservice import SimulationService
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService
from .constants import MemristorModels, ModelsSimulationFolders
from .forms import ModelParametersForm
from .representations import Subcircuit


class SimulationView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        serializer = SimulationInputsSerializer(data=data)

        if not serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        SimulationService(request_parameters=validated_data).simulate()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        form = ModelParametersForm()
        return render(request, "form.html", {"form": form})


# def form_view(request):
#     if request.method == "POST":
#         form = ModelParametersForm(request.POST)
#         if form.is_valid():
#             data = json.dumps(form.cleaned_data, indent=4)
#             response = HttpResponse(data, content_type="text/plain")
#             response["Content-Length"] = len(data)
#             response["Content-Disposition"] = 'attachment; filename="result.txt"'
#
#             print(f"\n\n{response.__str__()=}\n\n")
#             return response
#
#     else:
#         form = ModelParametersForm()
#
#     return render(request, "form.html", {"form": form})
