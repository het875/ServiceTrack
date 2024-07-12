from django.db import models
from django.core import validators
from django.core.validators import RegexValidator


class By(models.Model):
    created_by =[
        ("ORG" , "organations"),
        ("AD" , "admins"),
        ("EMP" , "employees"),
        ("CUST", "customers"),
    ]
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True,editable=False)
    created_by = models.CharField(max_length=10,choices=created_by)
    updated = models.DateTimeField(auto_now=True,editable=True)
    updated_by = models.CharField(max_length=10,choices=created_by)
    deleted = models.DateTimeField(null=True, blank=True,default=False)
    is_blocked = models.BooleanField(default=False)

    #Define the validaters
pan_card_validator = RegexValidator(
    regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
    message='PAN number must be 10 characters long and in the format: "ABCDE1234F".'
)

gst_number_validator = RegexValidator(
    regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$',
    message='GST number must be 15 characters long and in the format: "22AAAAA0000A1Z5".'
)

class Organization(BaseModel):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=180,unique=True)
    org_address =models.models.TextField()
    org_mobile_no = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r"^\+?91?\d{9,10}$",
                message='Mobile number must be entered in the format: "+999999999". Up to 15 digits allowed.',
            )
        ],
    )
    org_email = models.EmailField(unique=True,null=False,max_length=55)
    gst_number = models.CharField(
        max_length=15,
        validators=[gst_number_validator]
    )
    pan_number = models.CharField(
        max_length=10,
        validators=[pan_card_validator]
    )
    services_provided = models.TextField(max_length=250)
    block_expiration = models.DateTimeField(null=True, blank=True)
    is_mobile_verification = models.BooleanField(default=False)
    is_verified_by_admin = models.BooleanField(default=False)
    is_email_verification = models.BooleanField(default=False)
    # profile_picture = models.ImageField(
    #     upload_to="profile_pictures/", null=True, blank=True
    # )
    # logo = models.ImageField( blank=True, null=True)


    def __str__(self):
        return self.org_name
