from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
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
    path('profiles/<int:pk>/update/', award_views.ProfileUpdateView.as_view(), name='profileUpdate'),
    path('projects/', award_views.ProjectListView.as_view(), name='projects'),
    path('projects/new/', award_views.ProjectCreateView.as_view(), name='projectNew'),
    path('projects/<int:pk>/', award_views.ProjectDetailView.as_view(), name='project'),
    path('projects/<int:pk>/update/', award_views.ProjectUpdateView.as_view(), name='projectUpdate'),
    path('projects/<int:pk>/delete/', award_views.ProjectDeleteView.as_view(), name='projectDelete'),
    path('projects/<int:pk>/rate/new/', award_views.RateCreateView.as_view(), name='rateNew'),
    path('rate/<int:pk>/update/', award_views.RateUpdateView.as_view(), name='rateUpdate'),
    path('rate/<int:pk>/delete/', award_views.RateDeleteView.as_view(), name='rateDelete'),
    path('search-results/',award_views.search_results,name='searchProject')
]
