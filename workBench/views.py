from django.shortcuts import render
from configureDataBase.models.workBench import *


# Create your views here.
def myWorkBench(request):
    result = userScheduleControler.objects.all()
    return render(request, 'workBench/myWorkBench.html', {'result': result})
