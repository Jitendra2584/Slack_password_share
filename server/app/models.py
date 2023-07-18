from django.db import models
from cryptography.fernet import Fernet
import os 
from dotenv import load_dotenv
load_dotenv()

class SecretLink(models.Model):
    link_id = models.CharField(max_length=50, unique=True)
    encoded_secret_key = models.BinaryField(max_length=255)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return self.link_id

    def get_secret_key(self):
        return self.encode()

# Create your models here. 
