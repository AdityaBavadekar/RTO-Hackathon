from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
import enum

# Create your models here.

class IncidentType(enum.Enum):
    REFLECTOR_WITHOUT_RED_CLOTH = "reflector_without_red_cloth"
    REFLECTOR_WITH_RED_CLOTH = "reflector_with_red_cloth"
    RED_CLOTH_WITHOUT_REFLECTOR = "red_cloth_without_reflector"
    NO_REFLECTOR_NO_RED_CLOTH = "no_reflector_no_red_cloth"


class ReportedIncident(models.Model):
    incident_id = models.AutoField(primary_key=True)
    incident_type = models.CharField(max_length=255)
    incident_location = models.CharField(max_length=255)
    rto_id = models.IntegerField()
    incident_lat = models.FloatField()
    incident_long = models.FloatField()
    incident_timestamp = models.DateTimeField()
    incident_vin = models.CharField(max_length=255, null=True) # Vehicle Identification Number
    incident_vehicle_id = models.IntegerField(default=0)
    incident_image = models.ImageField(upload_to='images/')
    incident_prediction_metadata = models.JSONField(default=dict)
    incident_owner_metadata = models.JSONField(default=dict)
    incident_camera_metadata = models.JSONField(default=dict)
    
    def to_dict(self):
        return {
            "incident_id": self.incident_id,
            "incident_type": self.incident_type,
            "incident_location": self.incident_location,
            "rto_id": self.rto_id,
            "incident_lat": self.incident_lat,
            "incident_long": self.incident_long,
            "incident_timestamp": self.incident_timestamp,
            "incident_vin": self.incident_vin,
            "incident_vehicle_id": self.incident_vehicle_id,
            "incident_image": self.incident_image,
            "incident_prediction_metadata": self.incident_prediction_metadata,
            "incident_owner_metadata": self.incident_owner_metadata,
            "incident_camera_metadata": self.incident_camera_metadata,
        }


class ReportedIncidentChallan(models.Model):
    challan_id = models.AutoField(primary_key=True)
    incident_id = models.IntegerField()
    challan_amount = models.FloatField()
    vehicle_id = models.IntegerField(default=0)
    challan_timestamp = models.DateTimeField(auto_now=True)
    challan_calculation_metadata = models.JSONField(default=dict)
    challan_status_paid = models.BooleanField(default=False)
    challan_payment_timestamp = models.DateTimeField(null=True)
    challan_payment_reference_id = models.CharField(max_length=255, null=True)
    challan_payment_mode = models.CharField(max_length=255, null=True)
    challan_payment_receipt = models.ImageField(upload_to='images/', null=True)
    challan_payment_metadata = models.JSONField(default=dict)
    
    def to_dict(self):
        return {
            "challan_id": self.challan_id,
            "incident_id": self.incident_id,
            "challan_amount": self.challan_amount,
            "vehicle_id": self.vehicle_id,
            "challan_timestamp": self.challan_timestamp,
            "challan_calculation_metadata": self.challan_calculation_metadata,
            "challan_status_paid": self.challan_status_paid,
            "challan_payment_timestamp": self.challan_payment_timestamp,
            "challan_payment_reference_id": self.challan_payment_reference_id,
            "challan_payment_mode": self.challan_payment_mode,
            "challan_payment_receipt": self.challan_payment_receipt,
            "challan_payment_metadata": self.challan_payment_metadata,
        }

class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, unique=True)
    vehicle_vin = models.CharField(max_length=255, unique=True)
    vehicle_owner_name = models.CharField(max_length=255, null=True)
    vehicle_owner_address = models.CharField(max_length=255, null=True)
    vehicle_owner_contact = models.CharField(max_length=15, null=True)
    # vehicle_make = models.CharField(max_length=255)
    # vehicle_model = models.CharField(max_length=255)
    # vehicle_year = models.IntegerField()
    # vehicle_registration_number = models.CharField(max_length=255)
    # vehicle_registration_state = models.CharField(max_length=255)
    # vehicle_registration_date = models.DateTimeField()
    # vehicle_insurance_provider = models.CharField(max_length=255)
    # vehicle_insurance_validity = models.DateTimeField()
    vehicle_metadata = models.JSONField(default=dict)
    
    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "vehicle_vin": self.vehicle_vin,
            "vehicle_owner_name": self.vehicle_owner_name,
            "vehicle_owner_address": self.vehicle_owner_address,
            "vehicle_owner_contact": self.vehicle_owner_contact,
            "vehicle_metadata": self.vehicle_metadata,
        }

class RTOCenterManager(BaseUserManager):
    def create_user(self, rto_username, rto_password, **extra_fields):
        if not rto_username:
            raise ValueError("The RTO username must be set")
        user = self.model(rto_username=rto_username, **extra_fields)
        user.set_password(rto_password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rto_username, rto_password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(rto_username, rto_password, **extra_fields)

class RTOCenter(AbstractBaseUser, PermissionsMixin):
    rto_id = models.AutoField(primary_key=True)
    rto_username = models.CharField(max_length=255, unique=True)
    rto_password = models.CharField(max_length=255)
    rto_name = models.CharField(max_length=255)
    rto_address = models.CharField(max_length=255)
    rto_lat = models.FloatField()
    rto_long = models.FloatField()
    rto_website = models.URLField(null=True)
    rto_main_email = models.EmailField(null=True)
    rto_contact_number = models.CharField(max_length=15, null=True)
    rto_created_at = models.DateTimeField(default=now)
    rto_office_hours = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(default=now)
    rto_report_to_mails = models.JSONField()
    rto_metadata = models.JSONField()

    objects = RTOCenterManager()

    USERNAME_FIELD = 'rto_username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.rto_username
    
    def to_dict(self):
        return {
            "rto_id": self.rto_id,
            "rto_username": self.rto_username,
            "rto_name": self.rto_name,
            "rto_address": self.rto_address,
            "rto_lat": self.rto_lat,
            "rto_long": self.rto_long,
            "rto_website": self.rto_website,
            "rto_main_email": self.rto_main_email,
            "rto_contact_number": self.rto_contact_number,
            "rto_created_at": self.rto_created_at,
            "rto_office_hours": self.rto_office_hours,
            "last_login": self.last_login,
            "rto_report_to_mails": self.rto_report_to_mails,
            "rto_metadata": self.rto_metadata,
        }