from .models import IncidentType, ReportedIncidentChallan, ReportedIncident, RTOCenter
from .inference import predict_incident_type, read_vin
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import threading

load_dotenv()
PENAULTY_PER_INCIDENT = {
    IncidentType.REFLECTOR_WITHOUT_RED_CLOTH: 500,
    IncidentType.RED_CLOTH_WITHOUT_REFLECTOR: 500,
    IncidentType.REFLECTOR_WITH_RED_CLOTH: 0,
    IncidentType.NO_REFLECTOR_NO_RED_CLOTH: 1000,
} # In INR

PENUALTY_PER_PREVIOUS_CHALLAN = 1000 # In INR
EMAIL_TEMPLATE = """
Hello RTO Officer,

A new incident has been reported.

Vehicle Number: {incident_vin}
Incident Type: {incident_type}
Challan Amount: {challan.challan_amount} INR

Please take the necessary actions.

Regards,
Traffic Monitoring System
"""
RADIUS_KM=100

class CheckIncidentResponse:
    def __init__(self, incident_type:IncidentType, predicted=False, predictions_metadata=None):
        self.incident_type = incident_type
        self.predicted = predicted
        self.predictions_metadata = predictions_metadata

    def to_dict(self):
        return {
            "incident_type": self.incident_type.name,
            "predicted": self.predicted,
            "predictions_metadata": self.predictions_metadata,
        }

def check_incident(image_data) -> CheckIncidentResponse:
    prediction_data = predict_incident_type(image_data)
    if prediction_data:
        return CheckIncidentResponse(
            incident_type=prediction_data.incident_type,
            predicted=prediction_data.predicted,
            predictions_metadata=prediction_data.predictions_metadata
        )
    
    # else: no need to record the incident
    return CheckIncidentResponse(
        incident_type=IncidentType.REFLECTOR_WITH_RED_CLOTH,
        predicted=False,
        predictions_metadata=None
    )
    
def identify_vin(img_data) -> str:
    vin = read_vin(img_data)
    if not vin: vin = "MH 12 AB1234"
    return vin

def calculate_challan_amount(incident_type, previous_challans_count=0):
    incident_type_penalty = PENAULTY_PER_INCIDENT[incident_type]
    previous_challan_penalty = previous_challans_count * PENUALTY_PER_PREVIOUS_CHALLAN
    challan_amount = incident_type_penalty + previous_challan_penalty
    return incident_type_penalty, previous_challan_penalty, challan_amount

def generate_challan(main, incident_id, incident_type:IncidentType, previous_challans_count=0):
    incident_type_penalty, previous_challan_penalty, challan_amount = calculate_challan_amount(incident_type, previous_challans_count)
    print(f"Generating challan for incident {incident_id} with amount {challan_amount} INR")
    challan = ReportedIncidentChallan.objects.create(
        incident_id=main.incident_id,
        vehicle_id=main.incident_vehicle_id,
        challan_amount=challan_amount,
        challan_calculation_metadata={
            "incident_type": incident_type.name,
            "previous_challans_count": previous_challans_count,
            "incident_type_penalty": incident_type_penalty,
            "previous_challan_penalty": previous_challan_penalty
        }
    )
    challan.save()
    return challan

def _send_email(subject, body, to_mail):
    sender_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")  # Use App Password if 2FA is enabled

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_mail
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.send_message(message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")



def send_email_to_rto(incident_vin, incident_type, challan, rto_emails:list):
    rto_emails = rto_emails[:min(len(rto_emails), 2)]
    email_subject = f"New Incident Reported: {incident_vin}"
    email_body = EMAIL_TEMPLATE.format(incident_vin=incident_vin, incident_type=incident_type, challan=challan)
    rto_emails.append(os.getenv("EMAIL")) # For testing
    def send_email_thread():
        for email in rto_emails:    
            print(f"Sending email to {email}...")
            try:
                _send_email(subject=email_subject, body=email_body, to_mail=email)
            except Exception as e:
                print("Error while sending email", e)

    thread = threading.Thread(target=send_email_thread)
    thread.start()
    # for thread in threads:
    #     thread.join()

class OwnerInfoResponse:
    def __init__(self, owner_info, error=False):
        self.owner_info = owner_info
        self.error = error

    def to_dict(self):
        return {
            "owner_info": self.owner_info,
            "error": self.error
        }
    
def identify_vehicle_owner(vin) -> OwnerInfoResponse:
    # Fetch Owner Info using the VIN
    
    # Use NIC API to fetch owner info using the VIN
    # owner_info = fetch_owner_info(data['incident_vin'])
    owner_info = {
        "owner_name": "Owner Name",
        "owner_email": "test_truck_owner@gmail.com",
        "owner_address": "110 Main St, City 1",
        "owner_contact": "+91 9876543210"
    }
    if not owner_info:
        return OwnerInfoResponse(owner_info=None, error=True)

    return OwnerInfoResponse(owner_info=owner_info, error=False)

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the distance between two latitude-longitude points
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # Distance in kilometers

def find_nearby_rto_centers(lat, long) -> list:
    rto_centers = []
    all_rto_centers = RTOCenter.objects.all().only('rto_lat', 'rto_long', 'rto_id')
    for rto in all_rto_centers:
        if rto.rto_lat == lat and rto.rto_long == long:
            rto_centers.append(rto)
            continue
        
        distance = haversine(lat, long, rto.rto_lat, rto.rto_long)
        rto_centers.append({
            "rto_id": rto.rto_id,
            "lat": rto.rto_lat,
            "long": rto.rto_long,
            "distance": distance,
            "mails": [rto.rto_main_email] + rto.rto_report_to_mails
        })
        if len(rto_centers) >= 5: # Max 5 nearby RTO centers
            break

    rto_centers.sort(key=lambda x: x['distance'])
    return rto_centers[:min(5, len(rto_centers))]

# _send_email("Hello Test", "Test email from DJANGO", os.getenv("EMAIL"))