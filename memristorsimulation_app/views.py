from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from memristorsimulation_app.serializers.simulation import ModelParametersSerializer


class SimulationView(APIView):
    def post(self, request):
        serializer = ModelParametersSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
