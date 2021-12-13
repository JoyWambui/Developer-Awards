from django.urls import path
from . import views as award_views


urlpatterns= [
    path('signup/',award_views.signup, name='signup'),
    path('', award_views.homepage, name='homepage'),
    path('profiles/', award_views.ProfileList.as_view(), name='profiles'),
    path('profiles/profile/<int:pk>', award_views.ProfileView.as_view(), name='profile'),

]