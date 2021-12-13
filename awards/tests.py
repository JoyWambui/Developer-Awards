from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

class ProfileTestCase(TestCase):
    '''Tests the Profile Model and its methods'''
    
    def setUp(self):
        '''Creates an instance of the PRofile Model'''
        user1 = User.objects.create_user(first_name='ty', last_name='me',username='un', email='123@gmail.com', password='mo')
        self.profile = Profile(user=user1,profile_photo='profilephoto',bio='mimi',phone_number='0712345678')
    
    def tearDown(self):   
        '''Clears the database after every test'''
        Profile.objects.all().delete()
        
    def test_save_profile(self):
        '''Tests if a profile is saved'''
        self.profile.update_user_profile(self.profile,self.profile.user)
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)==1)

    def test_get_profiles(self):
        '''Tests that all profile instances are returned'''
        self.profile.save()
        profiles = Profile.get_profiles()
        self.assertTrue(len(profiles)==1)
        
    
    def test_get_single_profile(self):
        '''Retrieves a single profile instance from the database by id'''
        self.profile.save()
        print('my id=',self.profile.id)
        got_profile= Profile.get_single_profile(1)
        self.assertEquals(self.profile,got_profile)

    

