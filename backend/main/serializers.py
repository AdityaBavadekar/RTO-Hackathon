from rest_framework import serializers
from .models import ReportedIncident, ReportedIncidentChallan, RTOCenter, Vehicle

class ReportedIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedIncident
        fields = '__all__'
        
class ReportedIncidentChallanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedIncidentChallan
        fields = '__all__'

class RTOCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RTOCenter
        fields = '__all__'
        
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'    