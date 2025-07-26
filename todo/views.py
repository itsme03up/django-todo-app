from django.shortcuts import render, redirect,  get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
import traceback
import os
from django.conf import settings

# Create your views here.

@login_required
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
        
        # Try to get tasks for the logged-in user
        tasks = Task.objects.filter(user=request.user)
        debug_info.append(f"Number of tasks found: {tasks.count()}")

        if request.method == 'POST':
            title = request.POST.get('title')
            if title:
                Task.objects.create(title=title, user=request.user)
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

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('/')

@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('/')