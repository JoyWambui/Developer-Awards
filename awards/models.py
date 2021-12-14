from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import Http404, request
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    '''Model that defines a user profile and its methods'''
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length = 10,blank =True)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
    @receiver(post_save, sender=User)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
        
    @classmethod
    def get_profiles(cls):
        '''Retrieves all the profile instances from the database'''
        return cls.objects.all()

    @classmethod
    def get_single_profile(cls,profile_id):
        '''Retrieves a single profile instance from the database by id'''
        try:
            return cls.objects.filter(id=profile_id).get()
        except Profile.DoesNotExist:
            return Http404

        

    def __str__(self):
        return self.user.username
    
class Project(models.Model):
    '''Model that defines a project class and its methods'''
    title = models.CharField(max_length = 30)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)
    link = models.URLField(max_length=200)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    @classmethod
    def get_projects(cls):
        '''Retrieves all the project instances from the database'''
        return cls.objects.all()

    
    def __str__(self):
        return self.title
