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
    incident_lat = models.FloatField()
    incident_long = models.FloatField()
    incident_timestamp = models.DateTimeField()
    incident_vin = models.CharField(max_length=255, null=True) # Vehicle Identification Number
    incident_image = models.ImageField(upload_to='images/')
    incident_owner_metadata = models.JSONField(default=dict)
    incident_camera_metadata = models.JSONField(default=dict)


class ReportedIncidentChallan(models.Model):
    challan_id = models.AutoField(primary_key=True)
    incident_id = models.ForeignKey(ReportedIncident, on_delete=models.CASCADE)
    challan_amount = models.FloatField()
    challan_timestamp = models.DateTimeField(auto_now=True)
    challan_status_paid = models.BooleanField(default=False)
    challan_payment_timestamp = models.DateTimeField(null=True)
    challan_payment_reference_id = models.CharField(max_length=255, null=True)
    challan_payment_amount = models.FloatField()
    challan_payment_mode = models.CharField(max_length=255, null=True)
    challan_payment_receipt = models.ImageField(upload_to='images/', null=True)
    challan_payment_metadata = models.JSONField(default=dict)


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
    rto_location = models.CharField(max_length=255)
    rto_lat = models.FloatField()
    rto_long = models.FloatField()
    last_login = models.DateTimeField(default=now)
    rto_report_to_mails = models.JSONField()
    rto_metadata = models.JSONField()

    objects = RTOCenterManager()

    USERNAME_FIELD = 'rto_username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.rto_username