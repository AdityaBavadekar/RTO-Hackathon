from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from datetime import datetime

from .models import ReportedIncident, ReportedIncidentChallan, RTOCenter, IncidentType
from .serializers import ReportedIncidentSerializer
from . import utils

@api_view(['GET'])
def status(request):
    return Response({"message": "Server is running!"})

@api_view(['POST'])
def record_incident(request):
    data = {
        "incident_location": request.data.get("incident_location", ""),
        "incident_lat": float(request.data.get("incident_lat")),
        "incident_long": float(request.data.get("incident_long")),
        "incident_timestamp": request.data.get("incident_timestamp", datetime.now()),
        "incident_image": request.get("incident_image_base64"), # base64 encoded image
        "incident_camera_metadata": request.data.get("incident_camera_metadata", {}),
    }
    incident_check = utils.check_incident(data)
    
    if incident_check['incident_type'] == IncidentType.REFLECTOR_WITH_RED_CLOTH:
        return Response({"message": "Incident not recorded as truck has reflector and red cloth"})
    
    # Fetch Owner Info using the VIN, Generate challan according to the incident type (penalty amount), Notify RTO via email
    # Save the incident in the database
    incident = ReportedIncident.objects.create(
        incident_type=incident_check['incident_type'],
        incident_location=data['incident_location'],
        incident_lat=data['incident_lat'],
        incident_long=data['incident_long'],
        incident_timestamp=data['incident_timestamp'],
        incident_image=data['incident_image'],
        incident_camera_metadata=data['incident_camera_metadata'],
        **incident_check
    )
    incident.save()
    
    utils.generate_challan(incident)
    
    return Response({"message": "Incident recorded and challan generated successfully"})


@api_view(['GET'])
def get_incidents(request):
    rto_id = request.GET.get('rto_id')
    if not rto_id:
        return Response({
            "message": "RTO ID is required!",
            "error": True,
        })

    incidents = ReportedIncident.objects.filter(rto_id=rto_id)
    incidents = ReportedIncidentSerializer(incidents, many=True).data
    return Response({
        "incidents": incidents,
        "message": "Incidents fetched successfully!"
    })

@api_view(['POST'])
def register_rto(request):
    rto_username = request.data.get('username')
    rto_password = request.data.get('password')
    rto_name = request.data.get('rto_name')
    rto_location = request.data.get('rto_location')
    rto_lat = request.data.get('rto_lat')
    rto_long = request.data.get('rto_long')
    rto_report_to_mails = request.data.get('rto_report_to_mails', [])
    rto_metadata = request.data.get('rto_metadata', {})
    
    if any([field==None for field in [rto_username, rto_password, rto_name, rto_location, rto_lat, rto_long]]):
        return Response({"message": "All fields are required"}, status=400)

    if RTOCenter.objects.filter(rto_username=rto_username).exists():
        return Response({"message": "RTO username already exists"}, status=400)

    user = RTOCenter.objects.create_user(
        rto_username=rto_username,
        rto_password=rto_password,
        rto_name=rto_name,
        rto_location=rto_location,
        rto_lat=rto_lat,
        rto_long=rto_long,
        rto_report_to_mails=rto_report_to_mails,
        rto_metadata=rto_metadata
    )
    return Response({"message": "RTO registered successfully!"})


@api_view(['POST'])
def login_rto(request):
    rto_username = request.data.get('username')
    rto_password = request.data.get('password')

    if not rto_username or not rto_password:
        return Response({"message": "RTO username and password are required"}, status=400)
    
    rto_username_exists = RTOCenter.objects.filter(rto_username=rto_username).exists()
    
    if not rto_username_exists:
        return Response({"message": "RTO username does not exist"}, status=400)

    user = authenticate(request, username=rto_username, password=rto_password)
    if user is not None:
        return Response({"message": "Login successful!", "rto_username": user.rto_username})
    else:
        return Response({"message": "Invalid credentials"}, status=400)


@api_view(['GET'])
def get_rto_usernames(request):
    rtos = RTOCenter.objects.all().values('rto_username')
    # rtos = RTOCenterSerializer(rtos, many=True).data
    return Response({
        "rtos_registered": [k['rto_username'] for k in list(rtos)],
        "message": "RTOs fetched successfully!"
    })