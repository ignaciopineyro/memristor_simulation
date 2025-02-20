from django.contrib import admin
from django.urls import path

from memristorsimulation_app.views import SimulationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("simulate/", SimulationView.as_view(), name="simulate"),
]
