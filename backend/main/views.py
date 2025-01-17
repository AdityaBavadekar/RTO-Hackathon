from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from datetime import datetime
from django.utils.timezone import now

from .models import ReportedIncident, RTOCenter, IncidentType, ReportedIncidentChallan, Vehicle
from .serializers import ReportedIncidentSerializer, RTOCenterSerializer, ReportedIncidentChallanSerializer
from . import utils
from . import inference

@api_view(['GET'])
def status(request):
    return Response({"message": "Server is running!"})

@api_view(['POST'])
def check_image(request):
    image = request.data.get("image")
    if not image:
        return Response({"message": "Image is required"}, status=400)
    
    predictions = inference.predict_incident_type(image)
    return Response(predictions)

@api_view(['POST'])
def record_incident(request):
    data = {
        "incident_location": request.data.get("incident_location", "Unknown"),
        "incident_lat": float(request.data.get("incident_lat")),
        "incident_long": float(request.data.get("incident_long")),
        "incident_timestamp": request.data.get("incident_timestamp", datetime.now()),
        "incident_image": request.data.get("incident_image"), # base64 encoded image
        "incident_camera_metadata": request.data.get("incident_camera_metadata", {}),
    }
    incident_check = utils.check_incident(data["incident_image"])
    
    if not incident_check.predicted:
        return Response({"message": "There was an error in predicting the incident type"}, status=400)
    
    if incident_check.incident_type == IncidentType.REFLECTOR_WITH_RED_CLOTH:
        return Response({"message": "Incident not recorded as truck has reflector and red cloth"})
    
    nearby_rto_centers = utils.find_nearby_rto_centers(data["incident_lat"], data["incident_long"])
    nearest_rto_center = nearby_rto_centers[0] if nearby_rto_centers else None
    # Fetch Owner Info using the VIN, Generate challan according to the incident type (penalty amount), Notify RTO via email
    vin = utils.identify_vin(data["incident_image"])
    owner_info = {}
    vehicle = None
    # if vin:
    owner_info = utils.identify_vehicle_owner(vin=vin).to_dict()
    vehicle_exists = Vehicle.objects.filter(vehicle_vin=vin).exists()
    if vehicle_exists:
        vehicle = Vehicle.objects.filter(vehicle_vin=vin).first()
        owner_info['owner_info'] = vehicle.vehicle_metadata
    else:
        vehicle = Vehicle.objects.create(
        vehicle_vin=vin,
        vehicle_owner_name=owner_info['owner_info'].get('owner_name', None),
        vehicle_owner_address=owner_info['owner_info'].get('owner_address', None),
        vehicle_owner_contact=owner_info['owner_info'].get('owner_contact', None),
        vehicle_metadata=owner_info['owner_info']
    )
        
    # Save the incident in the database
    incident = ReportedIncident.objects.create(
        incident_type=incident_check.incident_type.name,
        rto_id=nearest_rto_center['rto_id'] if nearest_rto_center else 0,
        incident_location=data['incident_location'],
        incident_lat=data['incident_lat'],
        incident_long=data['incident_long'],
        incident_timestamp=data['incident_timestamp'],
        incident_image=data['incident_image'],
        incident_vin=vin,
        incident_vehicle_id=vehicle.vehicle_id,
        incident_camera_metadata=data['incident_camera_metadata'],
        incident_prediction_metadata=incident_check.to_dict(),
        incident_owner_metadata=owner_info
    )
    # incident.save()
    
    # Generate challan for the incident
    previous_challans_count = ReportedIncidentChallan.objects.filter(vehicle_id=vehicle.vehicle_id).count()
    
    challan = utils.generate_challan(main=incident, incident_id=incident.incident_id, incident_type=incident_check.incident_type, previous_challans_count=previous_challans_count)
    
    # Find nearby rto centers and send email to them
    if nearest_rto_center and nearest_rto_center['mails']:
        utils.send_email_to_rto(incident_vin=vehicle.vehicle_vin, incident_type=incident_check.incident_type, challan=challan,rto_emails=nearest_rto_center['mails'])

    print("Incident recorded and challan generated successfully")
    return Response({
        "message": "Incident recorded and challan generated successfully",
        "incident": {
            "incident_id": incident.incident_id,
            "incident_type": incident.incident_type,
            "incident_vin": incident.incident_vin,
        },
        "challan": {
            "challan_id": challan.challan_id,
            "challan_amount": challan.challan_amount,
        }
    })

@api_view(['POST'])
def get_vehicles(request):
    try:
        vehicles = Vehicle.objects.all()
        vehicles = [vehicle.to_dict() for vehicle in vehicles]
        return Response({
            "vehicles": vehicles,
            "message": "Vehicles fetched successfully!"
        })
    except Exception as e:
        return Response({
            "message": "There was an error fetching vehicles",
            "error": str(e)
        })

@api_view(['POST'])
def get_incidents(request):
    try:
        rto_id = request.data.get('rto_id')
        if not rto_id:
            return Response({
                "message": "RTO id is required!",
                "error": "RTO id is required!",
            })

        incidents = ReportedIncident.objects.filter(rto_id=rto_id)
        incidents = ReportedIncidentSerializer(incidents, many=True).data
        for incident in incidents:
            challans = ReportedIncidentChallan.objects.filter(incident_id=incident['incident_id'])
            incident['challans'] = ReportedIncidentChallanSerializer(challans, many=True).data
        return Response({
            "incidents": incidents,
            "message": "Incidents fetched successfully!"
        })
    except Exception as e:
        return Response({
            "message": "There was an error fetching incidents",
            "error": str(e)
        })

@api_view(['POST'])
def register_rto(request):
    try:
        rto_username = request.data.get('username')
        rto_password = request.data.get('password')
        rto_name = request.data.get('rto_name')
        rto_address = request.data.get('rto_address')
        rto_lat = request.data.get('rto_lat')
        rto_long = request.data.get('rto_long')
        rto_website = request.data.get('rto_website', None)
        rto_main_email = request.data.get('rto_main_email', None)
        rto_contact_number = request.data.get('rto_contact_number', None)
        rto_office_hours = request.data.get('rto_office_hours', None)
        rto_report_to_mails = request.data.get('rto_report_to_mails', [])
        rto_metadata = request.data.get('rto_metadata', {})
        
        if any([field==None for field in [rto_username, rto_password, rto_name, rto_address, rto_lat, rto_long]]):
            return Response({"message": "All fields are required"}, status=400)

        if RTOCenter.objects.filter(rto_username=rto_username).exists():
            return Response({"message": "RTO username already exists"}, status=400)
        
        new_rto_id = RTOCenter.objects.count()
        rto_name = rto_name.replace("@[id]@", f"{new_rto_id}")
        
        user: RTOCenter = RTOCenter.objects.create_user(
            rto_username=rto_username,
            rto_password=rto_password,
            rto_name=rto_name,
            rto_address=rto_address,
            rto_lat=rto_lat,
            rto_long=rto_long,
            rto_website=rto_website,
            rto_main_email=rto_main_email,
            rto_contact_number=rto_contact_number,
            rto_office_hours=rto_office_hours,
            rto_report_to_mails=rto_report_to_mails,
            rto_metadata=rto_metadata
        )
        return Response({"message": "RTO Center registered successfully!", "rto_username": user.rto_username, "rto_id": user.rto_id, "rto_center": user.to_dict()})
    except Exception as e:
        return Response({"message": "There was an error registering the RTO", "error": str(e)}, status=400)

@api_view(['POST'])
def get_rto_info(request):
    try:
        rto_username = request.data.get('username')
        if not rto_username:
            return Response({"message": "RTO username is required"}, status=400)
        
        rto = RTOCenter.objects.filter(rto_username=rto_username).first()
        if not rto:
            return Response({"message": "RTO username does not exist"}, status=400)
        
        # Update last login time
        rto.last_login = now()
        rto.save()
        
        rto = RTOCenterSerializer(rto).data
        rto.pop('password', None)
        return Response({
            "rto_info": rto,
            "message": "RTO info fetched successfully!"
        })
    except Exception as e:
        return Response({"message": "There was an error fetching RTO info", "error": str(e)}, status=400)

@api_view(['POST'])
def login_rto(request):
    try:
        rto_username = request.data.get('username')
        rto_password = request.data.get('password')
        
        print(rto_username, rto_password)

        if not rto_username or not rto_password:
            print(rto_username, "Required")
            return Response({"message": "RTO username and password are required"}, status=400)
        
        rto_username_exists = RTOCenter.objects.filter(rto_username=rto_username).exists()
        
        if not rto_username_exists:
            return Response({"message": "RTO username does not exist"}, status=400)

        user = authenticate(request, username=rto_username, password=rto_password)
        if user is not None:
            return Response({"message": "Login successful!", "rto_username": user.rto_username, "rto_id": user.rto_id, "rto_center": user.to_dict()})
        else:
            return Response({"message": "Invalid credentials"}, status=400)
    except Exception as e:
        return Response({"message": "There was an error logging in", "error": str(e)}, status=400)

@api_view(['GET'])
def get_rto_usernames(request):
    rtos = RTOCenter.objects.all().values('rto_username')
    # rtos = RTOCenterSerializer(rtos, many=True).data
    return Response({
        "count": len(rtos),
        "last_added": rtos.last().get('rto_username') if rtos else None,
        "rtos_registered": [k['rto_username'] for k in list(rtos)],
        "message": "RTOs fetched successfully!"
    })