from django.urls import path,include
from app import views

urlpatterns = [
    path('secret/',views.secret,name='secret'),
    path('secret/<link_id>',views.access_secret,name='access_secret'),
]