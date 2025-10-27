import json

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from memristorsimulation_app.serializers.simulation import SimulationInputsSerializer
from django.shortcuts import render
from memristorsimulation_app.services.simulationservice import SimulationService


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

        try:
            simulation_service = SimulationService(request_parameters=validated_data)
            zip_buffer = simulation_service.simulate_and_create_results_zip()

            folder_name = (
                simulation_service.simulation_inputs.export_parameters.folder_name
            )
            zip_filename = f"simulation_{folder_name}.zip"

            response = HttpResponse(
                zip_buffer.getvalue(), content_type="application/zip"
            )
            response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
            response["Content-Length"] = len(zip_buffer.getvalue())

            return response

        except Exception as e:
            return JsonResponse(
                {"ERROR": f"Simulation and export failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        return render(request, "form.html", {})
