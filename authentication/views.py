from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth

from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth.decorators import login_required


# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):        #submit form

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    
                else:
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)

                    user.is_active = False
                    user.save()

                    uid64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={'uid64':uid64, 'token':token_generator.make_token(user)})

                    activate_url = 'http://'+domain+link

                    email_body = "Hey "+user.username+ ', please use this link to verify your account:\n'+activate_url

                    email = EmailMessage(
                        "activate account",
                        email_body,
                        "noreply@website.com",
                        [email],
                    )
                    email.send(fail_silently=False)
                    messages.success(request, "Successful message")

        return render(request, 'authentication/register.html', context)

    

class VerificationView(View):
    def get(self, request, uid64, token):
        try:
            id = urlsafe_base64_decode(uid64).decode('utf-8')
            user = User.objects.get(pk=id)


            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            #...if active ret redirect
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully!')
            return redirect('login')
        except Exception as ex:
            print('EXCEPTION')
            


        return redirect('login')




class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:

                if user.is_active:
                    auth.login(request, user)

                    messages.success(request,'He '+username+ ', you Logged in Successfully.')
                    return redirect('expenses')

                messages.error(request, 'Account not activated, please check your email.')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Invalid credentials, try again.')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Fill username and password.')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')





class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumerics'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, username in use already.'}, status=409)
        return JsonResponse({'username_valid': True})
        


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, email in use already.'}, status=409)
        return JsonResponse({'email_valid': True})