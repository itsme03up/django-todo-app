from django.shortcuts import render, redirect
from .models import Task

# Create your views here.
from django.http import HttpResponse

def index(request):
    tasks = Task.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('/')

    return render(request, 'todo/index.html', {'tasks': tasks})