from django.urls import path
from .views import homePageView, createView,addView,deleteView

urlpatterns = [
    path('', homePageView, name='home'),
    path('create/', createView, name='create'),
    path('add/', addView, name='add'),
    path('delete/', deleteView, name='delete'),
]
