from django.shortcuts import render, redirect,  get_object_or_404
from .models import Task
from django.db import connection
from django.http import HttpResponse
import traceback
import os
from django.conf import settings

# Create your views here.

def index(request):
    try:
        # Detailed debugging information
        debug_info = []
        debug_info.append(f"DEBUG mode: {settings.DEBUG}")
        debug_info.append(f"Database path: {settings.DATABASES['default']['NAME']}")
        debug_info.append(f"Database file exists: {os.path.exists(str(settings.DATABASES['default']['NAME']))}")
        
        # Check if database tables exist
        table_names = connection.introspection.table_names()
        debug_info.append(f"Available tables: {table_names}")
        
        if 'todo_task' not in table_names:
            debug_info.append("ERROR: todo_task table not found!")
            return HttpResponse("<br>".join(debug_info), status=500)
        
        # Try to get tasks
        tasks = Task.objects.all()
        debug_info.append(f"Number of tasks found: {tasks.count()}")

        if request.method == 'POST':
            title = request.POST.get('title')
            if title:
                Task.objects.create(title=title)
            return redirect('/')
            
        return render(request, 'todo/index.html', {'tasks': tasks})
        
    except Exception as e:
        error_info = [
            f"Error type: {type(e).__name__}",
            f"Error message: {str(e)}",
            f"Full traceback:",
            traceback.format_exc()
        ]
        return HttpResponse("<pre>" + "\n".join(error_info) + "</pre>", status=500)

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('/')

def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('/')