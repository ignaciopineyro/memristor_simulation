from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SimulationView(APIView):
    def post(self, request):
        print("\nSimulationView POST\n")
        return Response(
            {"message": "Simulación iniciada"}, status=status.HTTP_202_ACCEPTED
        )
