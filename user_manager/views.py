from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponse 
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.template.loader import render_to_string 
from .token import account_activation_token 
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from .tasks import *
# Create your views here.

def auth(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/main')
    context={'title':'авторизация',}
    return render(request,'user_manager/templates/auth.html', context=context)

def exit(request):
    logout(request)
    return redirect('/main')

def registration(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False) 
        user.is_active = False 
        user.save() 
        # to get the domain of the current site 
        current_site = get_current_site(request) 
        mail_subject = 'Ссылка активации была отправлена ​​на ваш адрес электронной почты' 
        message = render_to_string('user_manager/templates/mail_mess/acc_activate_email.html', { 
            'user': user, 
            'domain': current_site.domain, 
            'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
            'token':account_activation_token.make_token(user), 
        }) 
        to_email = form.cleaned_data.get('email') 
        send_verification_email(mail_subject, message, to_email)
        return HttpResponse('Пожалуйста, подтвердите свой адрес электронной почты для завершения регистрации.') 
    return render(request, 'user_manager/templates/registration.html', context = {'form': form})

def activate(request, uidb64, token): 
    User = get_user_model() 
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save()
        login(request, user)
        messages.success(request,'Спасибо за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись.')
        return redirect('/profile')
    else: 
        return HttpResponse('Ссылка активации недействительна!') 
    
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(prof=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile_obj, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Профиль успешно обновлён!')
        return redirect('/user/profile')  
    context = {
        'title':'профиль',
        'form':form,
        'object':profile_obj,
    }
    return render (request,'user_manager/templates/profile.html', context)
