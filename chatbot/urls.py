from django.urls import path
from .views import *

urlpatterns = [
    path('upload_data', upload_data, name='upload_data'),
    path('home', home, name=''),
    path('', chatbot, name='chatbot'),
]
