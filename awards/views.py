from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status,viewsets
from .serializer import ProfileSerializer,ProjectSerializer
from .forms import SignUpForm
from .permissions import IsAuthenticatedOrReadOnly
from .models import  Profile,Project,Rate

def signup(request):
    '''View function that signs up a new user'''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "Congratulations! Your user account has been created.")
            return redirect(reverse('homepage'))
    else:
        form = SignUpForm()
        
    title = 'Create New Account'
    context={
        'title': title,
        'form': form,
        }
    return render(request, 'registration/signup.html', context)

def homepage(request):
    return render(request, 'homepage.html')

#PROFILE LOGIC
class ProfileListView(generic.ListView):
    model=Profile
    
class ProfileDetailView(generic.DetailView):
    model = Profile
    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(author=self.object.user).all()
        return context
    
class ProfileUpdateView(generic.UpdateView):
    model = Profile
  
    fields = [
        "profile_photo",
        "bio",
        "phone_number"
    ]
    
#PROJECT LOGIC
class ProjectCreateView(LoginRequiredMixin,generic.CreateView):
  
    model = Project
    fields = ['image','title', 'description','link']
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ProjectCreateView, self).form_valid(form)

class ProjectListView(generic.ListView):
    model=Project
    

class ProjectDetailView(generic.DetailView):
    model = Project
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['votes'] = Rate.objects.filter(rated_project=self.object.pk).all()
        return context

class ProjectUpdateView(generic.UpdateView):
    model = Project
  
    fields = [
        "title",
        "description",
        "image",
        "link"
    ]
    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.pk})
    
class ProjectDeleteView(generic.DeleteView):

    model = Project
     
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.id})


#RATE LOGIC
class RateCreateView(LoginRequiredMixin,generic.CreateView):
  
    model = Rate
    fields = ['design','usability', 'content']
    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.rated_project.pk})
    
    def form_valid(self, form):
        form.instance.rated_project = Project.objects.get(id=self.kwargs.get('pk'))
        form.instance.reviewer = self.request.user
        form.instance.score = (form.instance.design+form.instance.usability+form.instance.content)/3
        return super(RateCreateView, self).form_valid(form)
class RateUpdateView(generic.UpdateView):
    model = Rate
  
    fields = ['design','usability', 'content']
    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.rated_project.pk})

    def form_valid(self, form):
        form.instance.score = (form.instance.design+form.instance.usability+form.instance.content)/3
        return super(RateUpdateView, self).form_valid(form)


#API LOGIC
class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



# class ProfileList(APIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     # template_name = 'profiles.html'
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
    
#     def get(self, request, format=None):
#         profiles = Profile.get_profiles()
#         serializers = ProfileSerializer(profiles,many=True)
#         return Response({'serializers':serializers.data,})#'profiles':profiles})
    
#     def post(self, request, format=None):
#         serializers = ProfileSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ProfileView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'profile.html'
    
#     def get_single_profile(self,pk):
#         try:
#             return Profile.objects.filter(id=pk).get()
#         except Profile.DoesNotExist:
#             raise Http404


#     def get(self, request, pk, format=None):
#         user=request.user
#         profile = get_object_or_404(Profile, pk=pk)
#         serializers = ProfileSerializer(profile)
#         print(serializers.data)
#         return Response({'serializer':serializers.data,'profile':profile})

#     def post(self, request, pk,format=None):
#         user=request.user
#         if pk: # the update request 
#             profile = get_object_or_404(Profile, id=pk)
#             serializers = ProfileSerializer(profile, data=request.data)
#         else:  # the create request
#             serializers = ProfileSerializer(data=request.data)
#         if not serializers.is_valid():
#             return Response({'serializers': serializers,'profile':profile})
#         serializers.save()
#         return redirect('profile', pk=profile.id)

# class ProjectList(APIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     # template_name = 'projects.html'
#     def get(self, request, format=None):
#         projects = Project.get_projects()
#         serializers = ProjectSerializer(projects,many=True)
#         return Response({'serializers':serializers.data,'projects':projects})
    
#     def post(self, request, format=None):
#         serializers = ProjectSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
       