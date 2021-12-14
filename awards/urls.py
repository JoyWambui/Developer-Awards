from django.urls import path, include
from . import views as award_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profiles', award_views.ProfileViewSet)
router.register(r'projects', award_views.ProjectViewSet)

urlpatterns= [
    path('signup/',award_views.signup, name='signup'),
    path('', award_views.homepage, name='homepage'),
    path('api/', include(router.urls)),
    path('profiles/', award_views.ProfileListView.as_view(), name='profiles'),
    path('profiles/<int:pk>/', award_views.ProfileDetailView.as_view(), name='profile'),
    # path('projects/', award_views.ProjectList.as_view(), name='projects'),

]
