from django.urls import path
from .views import *
from image_predict import *
urlpatterns = [
    path('upload_data', upload_data, name='upload_data'),
    path('home', home, name=''),
    path('', chatbot, name='chatbot'),
    path('train/', train_model, name='train-model'),
    path('predict/', predict_model, name='predict-model'),
]
