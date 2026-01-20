from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Client, Project, Task
from django.db.models import Count

@login_required
def dashboard(request):
    user = request.user

    clients = Client.objects.filter(user=user)
    projects = Project.objects.filter(client__user=user)
    tasks = Task.objects.filter(project__client__user=user)

    context = {
        'clients_count': clients.count(),
        'projects_count': projects.count(),
        'tasks_count': tasks.count(),
        'completed_tasks': tasks.filter(status=True).count(),
        'pending_tasks': tasks.filter(status=False).count(),
        'project_status': projects.values('status').annotate(count=Count('id')),
    }

    return render(request, 'core/dashboard.html', context)



@login_required
def client_list(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, 'core/client_list.html', {
        'clients': clients
    })


@login_required
def add_client(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        company = request.POST['company']

        Client.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            company=company
        )
        return redirect('client_list')

    return render(request, 'core/add_client.html')

@login_required
def project_list(request, client_id):
    client = Client.objects.get(id=client_id, user=request.user)
    projects = Project.objects.filter(client=client)

    return render(request, 'core/project_list.html', {
        'client': client,
        'projects': projects
    })


@login_required
def add_project(request, client_id):
    client = Client.objects.get(id=client_id, user=request.user)

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        status = request.POST['status']

        Project.objects.create(
            client=client,
            title=title,
            description=description,
            deadline=deadline,
            status=status
        )
        return redirect('project_list', client_id=client.id)

    return render(request, 'core/add_project.html', {
        'client': client
    })
    
@login_required
def task_list(request, project_id):
    project = Project.objects.get(
        id=project_id,
        client__user=request.user
    )
    tasks = Task.objects.filter(project=project)

    return render(request, 'core/task_list.html', {
        'project': project,
        'tasks': tasks
    })


@login_required
def add_task(request, project_id):
    project = Project.objects.get(
        id=project_id,
        client__user=request.user
    )

    if request.method == 'POST':
        title = request.POST['title']
        priority = request.POST['priority']

        Task.objects.create(
            project=project,
            title=title,
            priority=priority
        )
        return redirect('task_list', project_id=project.id)

    return render(request, 'core/add_task.html', {
        'project': project
    })
    
@login_required
def update_task(request, task_id):
    task = Task.objects.get(
        id=task_id,
        project__client__user=request.user
    )

    if request.method == 'POST':
        task.title = request.POST['title']
        task.priority = request.POST['priority']
        task.status = True if request.POST.get('status') == 'on' else False
        task.save()

        return redirect('task_list', project_id=task.project.id)

    return render(request, 'core/update_task.html', {
        'task': task
    })
    
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(
        id=task_id,
        project__client__user=request.user
    )

    if request.method == 'POST':
        project_id = task.project.id
        task.delete()
        return redirect('task_list', project_id=project_id)

    return render(request, 'core/confirm_delete.html', {
        'task': task
    })
