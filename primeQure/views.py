from django.shortcuts import render
from .models import Job


def index(request):
    all_jobs = Job.objects.all()[:10]
    return render(request, 'primeQure/index.html', {'jobs': all_jobs} )

