import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from memristorsimulation_app.serializers.simulation import ModelParametersSerializer
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ModelParametersForm


class SimulationView(APIView):
    def post(self, request):
        serializer = ModelParametersSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        form = ModelParametersForm()
        return render(request, "form.html", {"form": form})


def form_view(request):
    if request.method == "POST":
        form = ModelParametersForm(request.POST)
        if form.is_valid():
            data = json.dumps(form.cleaned_data, indent=4)
            response = HttpResponse(data, content_type="text/plain")
            response["Content-Length"] = len(data)
            response["Content-Disposition"] = 'attachment; filename="result.txt"'

            print(f"\n\n{response.__str__()=}\n\n")
            return response

    else:
        form = ModelParametersForm()

    return render(request, "form.html", {"form": form})
