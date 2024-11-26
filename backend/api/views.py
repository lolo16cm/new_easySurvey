from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from userauths.models import User
from creator.models import Question, Survey
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated

# from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

#get token using serializer_class defined in api_serializer.MyTokenObtainPairSerializer
#log in the user
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer

#generics: generics refers to a module that provides generic views — reusable, pre-configured views for common actions like creating, retrieving, updating, and deleting resources.
#use createApiview to handle post request to create new instance
#create the new account
class RegisterView(generics.CreateAPIView):
    #required to call User model due to generic views although not directly used
    queryset = User.objects.all()
    #allow everyone to register
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


def generate_random_otp(length=7):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

#retrive single instance of a model(User)
class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        #get the url parametor key 'email' and return the value
        email = self.kwargs['email']
        user = User.objects.filter(email=email).first()
        if user:
            #base64-encoded UUID (Universally Unique Identifier) 
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            user.refresh_token =refresh_token
            user.otp= generate_random_otp()
            user.save()
            #the link to reset the password
            link = f'http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}'
            
            context = {
                'link': link,
                'username': user.username
                }
            
            subject = 'Password Reset Email'
            text_body =  render_to_string('email/password_reset.txt', context)
            html_body = render_to_string('email/password_reset.html', context)
            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
                body=text_body,
            )
            msg.attach_alternative(html_body, 'text/html')
            msg.send()


            # print("link === ", link)
        return user
        

#at the page of changing password        
class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes =[AllowAny]
    serializer_class = api_serializer.UserSerializer

    def create(self, request, *args, **kwargs):
        otp = request.data['otp']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']

        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ''
            user.save()
            return Response({'message': 'Update successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    

class SurveyCreateView(generics.CreateAPIView):
    # communicate with Survey model
    queryset = Survey.objects.all()
    serializer_class = api_serializer.SurveyCreateSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        # Save the survey with the current user as the creator
        # class-based views, you can access request as self.request, even if it’s not explicitly passed as a parameter to your method.
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Use the serializer to validate and create the survey
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)  # Call perform_create to save the survey
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
