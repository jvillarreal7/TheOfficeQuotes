from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from random import randint
from .models import *
import requests


def Home(request):
    count = Quote.objects.count()
    if count > 0:
        random_quote = Quote.objects.all()[randint(0, count - 1)]
    return render(request, "OfficeApp/home.html", {
        'random_quote': random_quote
    })


def LoginAdmin(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, "OfficeApp/login.html", {'site_key': settings.RECAPTCHA_SITE_KEY})
        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            secret_key = settings.RECAPTCHA_SECRET_KEY

            print(request.POST)

            data = {
                'response': request.POST.get('recaptcha'),
                'secret': secret_key
            }
            resp = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data)
            result_json = resp.json()

            print(result_json)

            if not result_json.get('success'):
                message = "Really?"
                return render(request, 'OfficeApp/login.html', {'message': message, 'is_robot': True, 'site_key': settings.RECAPTCHA_SITE_KEY})
            else:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
                else:
                    message = "Wrong username and/or password."
                    return render(request, 'OfficeApp/login.html', {'message': message, 'site_key': settings.RECAPTCHA_SITE_KEY})
        else:
            message = "Bad request! Try again."
            return render(request, '/login-dashboard/', {'message': message, 'site_key': settings.RECAPTCHA_SITE_KEY})
    else:
        return HttpResponseRedirect('/dashboard/')


def LogoutAdmin(request):
    logout(request)
    return HttpResponseRedirect('/login-dashboard/')


def Dashboard(request):
    if request.user.is_authenticated:
        return render(request, "OfficeApp/dashboard.html")
    else:
        return HttpResponseRedirect('/login-dashboard/')
