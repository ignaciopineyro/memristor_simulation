from memristorsimulation_app.constants import (
    MemristorModels,
    ModelsSimulationFolders,
    NetworkType,
    PlotType,
    WaveForms,
)
from rest_framework import serializers
from rest_enumfield import EnumField
from memristorsimulation_app.serializers.baseserializers import CamelCaseSerializer


class ModelParametersSerializer(CamelCaseSerializer):
    alpha = serializers.FloatField()
    beta = serializers.FloatField()
    rinit = serializers.FloatField()
    roff = serializers.FloatField()
    ron = serializers.FloatField()
    vt = serializers.FloatField()


class SubcircuitSerializer(CamelCaseSerializer):
    model_parameters = ModelParametersSerializer()
    name = serializers.CharField(required=False, allow_null=True)
    nodes = serializers.ListField(
        child=serializers.CharField(), required=False, default=[]
    )


class SinWaveFormSerializer(CamelCaseSerializer):
    vo = serializers.FloatField()
    amplitude = serializers.FloatField()
    frequency = serializers.FloatField()
    td = serializers.FloatField(default=0.0)
    theta = serializers.FloatField(default=0.0)
    phase = serializers.FloatField(default=0.0)


class PulseWaveFormSerializer(CamelCaseSerializer):
    v1 = serializers.FloatField()
    v2 = serializers.FloatField()
    td = serializers.FloatField(default=0.0)
    tr = serializers.FloatField(default=0.0)
    tf = serializers.FloatField(default=0.0)
    pw = serializers.FloatField(default=0.5)
    per = serializers.FloatField(default=1)
    np = serializers.IntegerField(default=0)


class AlternatingPulseWaveFormSerializer(CamelCaseSerializer):
    v1 = serializers.FloatField()
    v2 = serializers.ListField(child=serializers.FloatField())
    td = serializers.FloatField(default=0.0)
    tr = serializers.FloatField(default=0.0)
    tf = serializers.FloatField(default=0.0)
    pw = serializers.FloatField(default=0.5)
    per = serializers.FloatField(default=1)
    np = serializers.IntegerField(default=0)


class WaveFormSerializer(CamelCaseSerializer):
    type = EnumField(choices=WaveForms)
    parameters = serializers.DictField()

    # def validate(self, data):
    #     waveform_type = data.get("type")
    #     parameters = data.get("parameters", {})

    #     serializer_map = {
    #         "sin": SinWaveFormSerializer,
    #         "pulse": PulseWaveFormSerializer,
    #         "pwl": AlternatingPulseWaveFormSerializer,
    #     }

    #     if waveform_type not in serializer_map:
    #         raise serializers.ValidationError(
    #             f"Unsupported waveform type: {waveform_type}"
    #         )

    #     param_serializer = serializer_map[waveform_type](data=parameters)
    #     if not param_serializer.is_valid():
    #         raise serializers.ValidationError({"parameters": param_serializer.errors})

    #     data["validated_parameters"] = param_serializer.validated_data
    #     return data

    # def to_internal_value(self, data):
    #     validated_data = super().to_internal_value(data)
    #     return {
    #         "type": validated_data["type"],
    #         "parameters": validated_data.get(
    #             "validated_parameters", validated_data["parameters"]
    #         ),
    #     }


class InputParametersSerializer(CamelCaseSerializer):
    source_number = serializers.IntegerField()
    n_plus = serializers.CharField()
    n_minus = serializers.CharField()
    wave_form = WaveFormSerializer()


class SimulationParametersSerializer(CamelCaseSerializer):
    analysis_type = serializers.CharField(default=".tran")
    tstep = serializers.FloatField()
    tstop = serializers.FloatField()
    tstart = serializers.FloatField(required=False, allow_null=True)
    tmax = serializers.FloatField(required=False, allow_null=True)
    uic = serializers.BooleanField(required=False, allow_null=True, default=True)


class ExportParametersSerializer(CamelCaseSerializer):
    model_simulation_folder = EnumField(choices=ModelsSimulationFolders)
    folder_name = serializers.CharField()
    file_name = serializers.CharField()
    magnitudes = serializers.ListField(child=serializers.CharField())


class NetworkParametersSerializer(CamelCaseSerializer):
    n = serializers.IntegerField(required=False, allow_null=True)
    m = serializers.IntegerField(required=False, allow_null=True)
    amount_connections = serializers.IntegerField(required=False, allow_null=True)
    amount_nodes = serializers.IntegerField(required=False, allow_null=True)
    shortcut_probability = serializers.FloatField(required=False, allow_null=True)
    seed = serializers.IntegerField(required=False, allow_null=True)


class SimulationInputsSerializer(CamelCaseSerializer):
    model = EnumField(choices=MemristorModels)
    subcircuit = SubcircuitSerializer()
    input_parameters = InputParametersSerializer()
    simulation_parameters = SimulationParametersSerializer()
    export_parameters = ExportParametersSerializer()
    network_type = EnumField(choices=NetworkType)
    network_parameters = NetworkParametersSerializer(required=False, allow_null=True)
    amount_iterations = serializers.IntegerField(default=1)
    plot_types = serializers.ListField(
        child=EnumField(choices=PlotType), required=False, default=[]
    )
