from django.contrib import admin
from django.urls import path

from memristorsimulation_app.views import (
    SimulationView,
    form_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", SimulationView.as_view(), name="form"),
]
