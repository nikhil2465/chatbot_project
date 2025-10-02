# from django.urls import path
# from .views import home, chat, wix_products_api

# urlpatterns = [
#     path("", home, name="home"),
#     path("chat/", chat, name="chat"),
#     path("wix-products/", wix_products_api, name="wix_products"),  # New endpoint
# ]

# chatbot/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage with chatbot
    path('chat/', views.chat, name='chat'),
    #path('wix-products/', views.wix_products_api, name='wix-products'),
]


