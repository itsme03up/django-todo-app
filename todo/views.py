from django.shortcuts import render, redirect,  get_object_or_404
from .models import Task
from django.db import connection
from django.http import HttpResponse

# Create your views here.

def index(request):
    try:
        # Check if database tables exist
        table_names = connection.introspection.table_names()
        if 'todo_task' not in table_names:
            return HttpResponse("Database not properly migrated. Tables available: " + str(table_names), status=500)
        
        tasks = Task.objects.all()

        if request.method == 'POST':
            title = request.POST.get('title')
            if title:
                Task.objects.create(title=title)
            return redirect('/')
        return render(request, 'todo/index.html', {'tasks': tasks})
    except Exception as e:
        return HttpResponse(f"Database error: {str(e)}", status=500)

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('/')

def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('/')