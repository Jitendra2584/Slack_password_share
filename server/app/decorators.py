from django.http import HttpResponseBadRequest
import os
from dotenv import load_dotenv
load_dotenv()

def validate_secret(view_func):
    def wrapper(request, *args, **kwargs):
        expected_secret = os.getenv('shared_token')
        received_secret = request.META.get("HTTP_X_BOT_SECRET")  # Assuming the secret is included as a custom header

        if received_secret != expected_secret:
            return HttpResponseBadRequest("Invalid or missing secret")

        return view_func(request, *args, **kwargs)

    return wrapper