from .models import IncidentType, ReportedIncidentChallan

PENAULTY_PER_INCIDENT = {
    IncidentType.REFLECTOR_WITHOUT_RED_CLOTH: 500,
    IncidentType.RED_CLOTH_WITHOUT_REFLECTOR: 500,
    IncidentType.NO_REFLECTOR_NO_RED_CLOTH: 1000,
} # In INR

PENUALTY_PER_PREVIOUS_CHALLAN = 1000 # In INR
EMAIL_TEMPLATE = """
Hello RTO Officer,

A new incident has been reported.

Vehicle Number: {incident['incident_vin']}
Incident Type: {incident['incident_type'].name}
Challan Amount: {challan.challan_amount} INR

Please take the necessary actions.

Regards,
Traffic Monitoring System
"""

def check_incident(data):
    # TODO: The main logic to check if truck in image has reflector/red cloth or not
    _ = True
    if (_):
        # Should be recorded
        return {
            "incident_vin": "vehicle_number",
            # ... all other fields
            "incident_type": IncidentType.NO_REFLECTOR_NO_RED_CLOTH,
        }

    # else: no need to record the incident
    return {
        "incident_type": IncidentType.REFLECTOR_WITH_RED_CLOTH,
    }

def generate_challan_amount(incident, previous_challans_count=0):
    challan_amount = PENAULTY_PER_INCIDENT[incident['incident_type']] + previous_challans_count * PENUALTY_PER_PREVIOUS_CHALLAN
    return challan_amount

def generate_challan(incident, previous_challans_count=0):
    challan_amount = generate_challan_amount(incident, previous_challans_count)
    challan = ReportedIncidentChallan.objects.create(
        incident_id=incident['incident_id'],
        challan_amount=challan_amount,
    )
    challan.save()
    return challan

def send_email_to_rto(incident, challan, rto_emails):
    email_title = "New Incident Reported"
    email_subject = f"New Incident Reported: {incident['vehicle_number']}"
    email_body = EMAIL_TEMPLATE.format(incident=incident, challan=challan)
    for email in rto_emails:
        # Send email
        pass