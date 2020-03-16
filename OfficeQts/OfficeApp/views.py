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

    # Trivia: Directed episodes
    directed_episodes_total = Episode.objects.filter(
        directed_by_id=random_quote.episode.directed_by_id).order_by('air_date')

    directed_episodes_by_date = Episode.objects.filter(
        directed_by_id=random_quote.episode.directed_by_id, air_date__lte=random_quote.episode.air_date)

    episodes_sf = Episode.objects.filter(
        air_date__lt=random_quote.episode.air_date)

    running_time_sf = 0
    running_time_sf_hours = 0

    for e in episodes_sf:
        running_time_sf += e.running_time

    if running_time_sf > 0:
        running_time_sf_hours = running_time_sf / 60

    iss_around_earth = running_time_sf / 92

    return render(request, "OfficeApp/home.html", {
        'random_quote': random_quote,
        'episode_counter': len(directed_episodes_by_date),
        'directed_episodes_total': len(directed_episodes_total),
        'running_time_sf': running_time_sf,
        'running_time_sf_hours': round(running_time_sf_hours, 2),
        'running_time_avg': 27.15,
        'iss_around_earth': round(iss_around_earth, 2),
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
