from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import requests
from django.db.models import Count, Sum
import datetime

def address(request, address):
    return render(request, 'address.html', {"address": address})


def main_page(request):
    return render(request, 'main_page.html')
