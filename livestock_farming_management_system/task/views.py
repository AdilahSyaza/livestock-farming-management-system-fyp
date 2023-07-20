from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from task.models import Task

from user.models import User

# Represents the homepage or root URL of Task module. It will redirect system to the mainTask view function.
def taskIndex(request):
    return redirect('task:mainTask')


# Renders main task page with all records of task
def mainTask(request):
    user = User.objects.get(email = request.session['EMAIL'])
    tasks=Task.objects.all()
    openedTasks=Task.objects.exclude(taskCompletionStatus='COMPLETED')
    completedTasks=Task.objects.filter(taskCompletionStatus='COMPLETED')
    return render(request, 'mainTask.html', {'user':user,'tasks':tasks,'openedTasks':openedTasks,'completedTasks':completedTasks})


# Handles addition of new task or renders add task form
def addTask(request):
    user = User.objects.get(email = request.session['EMAIL'])
    staff=User.objects.all()
    try:

        if request.method=='POST':
            taskName=request.POST.get('taskName')
            taskPriority=request.POST.get('priority')
            taskCategory=request.POST.get('taskCategory')
            taskDetails=request.POST.get('details')
            taskDueDate=request.POST.get('dueDate')
            taskCompletionStatus=request.POST.get('completionStatus')
            taskAssigner=user
            selectedUserID=request.POST.get('taskAssignee')
            assignee = User.objects.get(id = selectedUserID)
            taskAttachment = request.FILES.get('fileupload', None)
            fss =FileSystemStorage()
            Task(taskName=taskName,taskPriority=taskPriority,taskCategory=taskCategory,taskDetails=taskDetails,taskDueDate=taskDueDate,taskCompletionStatus=taskCompletionStatus,taskAssigner=taskAssigner,taskAssignee=assignee,taskAttachment=taskAttachment).save()
            messages.success(request,'Task is successfully created.', extra_tags='addTask')
            return redirect('task:mainTask')
        else:
            return render(request, 'addTask.html', {'user':user,'staff':staff})

    except IntegrityError:
        messages.error(request,'Error Task')
        return render(request, 'addTask.html', {'user':user,'staff':staff})


# Renders view task page with information of a specific task
def viewTask(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    task = Task.objects.get(id=id)
    return render(request, 'viewTask.html', {'user':user,'task':task})


# Handles update operation of a specific task
def updateTask(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    task = Task.objects.get(id=id)
    staff=User.objects.all()
    if request.method=='POST':
        task.taskName=request.POST.get('taskName')
        task.taskPriority=request.POST.get('priority')
        task.taskCategory=request.POST.get('taskCategory')
        task.taskDetails=request.POST.get('details')
        task.taskDueDate=request.POST.get('dueDate')
        selectedUserID=request.POST.get('taskAssignee')
        task.assignee = User.objects.get(id = selectedUserID)
        # task.taskAttachment = request.FILES['fileupload']
        if len(request.FILES) != 0:
            if task.taskAttachment!=None or task.taskAttachment!='':
                task.taskAttachment.delete()
            task.taskAttachment = request.FILES['fileupload']
            fss =FileSystemStorage()
        
        task.save()
        messages.success(request,"Task is successfully updated")
        return redirect('task:mainTask')
    
    return render(request, 'updateTask.html', {'user':user,'task':task,'staff':staff})


# Handles deletion operation of a specific task
def deleteTask(request,id):
    try:
        user = User.objects.get(email = request.session['EMAIL'])
        task = Task.objects.get(id=id)
        if request.method=='POST':
            if task.taskAttachment!=None or task.taskAttachment!='':
                task.taskAttachment.delete()
            task.delete()
            messages.success(request,"Task is deleted succesfully..!")
            return redirect('task:mainTask')
        else:
            return render(request, 'deleteTask.html', {'user':user,'task':task})

    except Task.DoesNotExist:
        messages.success(request,'No record of the task!' + id)
        return redirect('task:mainTask')


# Renders task page with all task records related to a user
def myTask(request):
    user = User.objects.get(email = request.session['EMAIL'])
    userOpenedTasks=Task.objects.filter(taskAssignee = user.id).exclude(taskCompletionStatus='COMPLETED')
    userCompletedTasks = Task.objects.all().filter(taskAssignee = user.id, taskCompletionStatus='COMPLETED')
    # completedTasks=Task.objects.filter(taskCompletionStatus='COMPLETED')
    return render(request, 'myTask.html', {'user':user,'userOpenedTasks':userOpenedTasks,'userCompletedTasks':userCompletedTasks})


# Handles update operation of task status by a user
def updateTaskStatus(request,id):
    user=User.objects.get(email = request.session['EMAIL'])
    taskInfo=Task.objects.get(id = id)
    if request.method=='POST':
        taskInfo.taskCompletionStatus=request.POST.get('taskCompletionStatus')
        taskInfo.save()
        messages.success(request,"Task progress status is successfully updated")
        return redirect('task:myTask')

    return render(request, 'taskStatus.html', {'user':user,'task':taskInfo})
