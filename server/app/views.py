from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
import json
from .decorators import validate_secret
import os
import secrets
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()
from .models import SecretLink
from cryptography.fernet import Fernet
# from .models import SecretLink

# Create your views here.

@csrf_exempt
@validate_secret
def secret(request):
    if request.method == 'POST':
        
        secret_key=json.loads(request.body)['key1'].encode()
        person=json.loads(request.body)['username']
        # secret_key = request.POST.get('text')

        # Generate a unique link with a 15-minute expiration time
        link_id = secrets.token_urlsafe()
        expiration_time = timezone.now() + timedelta(minutes=15)
        # Store the link and encoded secret key in the database
        SecretLink.objects.create(link_id=link_id, encoded_secret_key=secret_key, expiration_time=expiration_time)

        # # Store the link and associated secret key in the database
        # SecretLink.objects.create(link_id=link_id, secret_key=secret_key, expiration_time=expiration_time)
        # # Construct the link URL
        link_url = request.build_absolute_uri('/') + 'secret/' + link_id

        # # Prepare the response to Slackbot
        response = {
            'text': f"{person} shared a secret link : {link_url}\nUse within 15 minutes",
        }
        
        return JsonResponse(response)
    return JsonResponse({'message': 'Invalid request'}) 


def access_secret(request, link_id):

    secret_link = get_object_or_404(SecretLink, link_id=link_id)    

    if secret_link.expiration_time < timezone.now():
        return render(request, 'expired.html')

    # Decrypt the encoded secret key
    cipher_suite = Fernet(SecretLink.get_secret_key(os.getenv('fernet_key')))
    decrypted_secret_key = cipher_suite.decrypt(secret_link.encoded_secret_key).decode()

    # Perform desired actions with the secret key
    # For example, you can pass the decrypted_secret_key to a template or use it in your logic

    return render(request, 'secret.html', {'secret_key': decrypted_secret_key})


# @task
# def delete_expired_rows():
#     current_time = timezone.now()
#     expired_rows = SecretLink.objects.filter(expiration_time__lt=current_time)
#     expired_rows.delete()
