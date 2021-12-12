from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import  Profile
from .serializer import ProfileSerializer


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
            return redirect(request, 'homepage')
            messages.success(request, "Congratulations! Your user account has been created.")
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

class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profiles.html'
    def get(self, request, format=None):
        profiles = Profile.get_profiles()
        serializers = ProfileSerializer(profiles,many=True)
        return Response({'serializers':serializers.data,'profiles':profiles})
        