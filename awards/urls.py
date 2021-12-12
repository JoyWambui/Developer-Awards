from django.urls import path
from . import views as award_views


urlpatterns= [
    path('signup/',award_views.signup, name='signup'),
]