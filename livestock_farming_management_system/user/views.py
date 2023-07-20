import email
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from random import randint

from .models import User
from animal.models import Cattle,Sheep

# Create your views here.
    
# Handles the login functionality
def loginpage(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            if user.status == 'OPEN':
                if user.password == request.POST['password']:
                    request.session['EMAIL'] = user.email
                    request.session['LOGIN'] = 'YES'
                    request.session['ROLE'] = user.userRole
                    request.session['STAFFID'] = user.staffID
                    return redirect('user:home')
                else:
                    messages.success(request,'Incorrect User Credentials')
            else:
                messages.error(request,'This account has been deactivated. You cannot longer login using this account.')
        except User.DoesNotExist:
            messages.warning(request, 'Incorrect User Credentials')
    
    return render(request, 'login.html')


# Renders the homepage with a list of latest (top 4) cattles and sheeps to be displayed
def home(request):
    user = User.objects.get(email = request.session['EMAIL'])
    cattle=Cattle.objects.filter(~Q(cattleAttachment=''))
    newestCattle=cattle.order_by('-cattleDateRecorded')[:4]
    # print(newestCattle)
    sheep=Sheep.objects.filter(~Q(sheepAttachment=''))
    newestSheep=sheep.order_by('-sheepDateRecorded')[:4]
    # for x in allAnimals:
    #     randomAnimals.insert(randint(0,len(randomAnimals)),x)
    # print("random:",randomAnimals)
    return render(request,'homepage.html', {'user':user,'newestCattle':newestCattle,'newestSheep':newestSheep})


# logout from the session and redirect user to login page
def logout(request):
    request.session.flush()
    return redirect('user:loginpage')


# Renders main staff page with a list of staff records
def mainStaff(request):
    user = User.objects.get(email = request.session['EMAIL'])
    staff = User.objects.all()
    openedUser = User.objects.all().filter(status='OPEN')
    deactivatedUser = User.objects.all().filter(status='DEACTIVATED')
    return render(request, 'mainStaff.html', {'pagination':'STAFF', 'user':user, 'staff':staff, 'openedUser':openedUser, 'deactivatedUser':deactivatedUser})


# Handles the addition of new staff
def addStaff(request):
    user = User.objects.get(email = request.session['EMAIL'])

    try:

        if request.method=='POST':
            staffID=request.POST.get('staffID')
            email=request.POST.get('email')
            password='abcd1234'
            status='OPEN'
            role=request.POST.get('role')
            firstName=request.POST.get('firstname')
            lastName=request.POST.get('lastname')
            username=request.POST.get('username')
            User(email=email, staffID=staffID, password=password,userRole=role,status=status,firstName=firstName,lastName=lastName,username=username).save()
            messages.success(request,'Staff account is successfully created.', extra_tags='addStaff')
            return redirect('user:mainStaff')
            # return render(request, 'addStaff.html', {'pagination':'STAFF', 'user':user})
        else:
            return render(request, 'addStaff.html', {'pagination':'STAFF', 'user':user})

    except IntegrityError:
        messages.error(request,'Staff ID or email has been used before; Must be unique for each account.')
        return render(request, 'addStaff.html', {'pagination':'STAFF', 'user':user})


# Renders staff profile page with the information of that specific staff
def staffProfile(request, id):
    user = User.objects.get(email = request.session['EMAIL'])
    staff = User.objects.get(id = id)
    return render(request, 'staffProfile.html',{'user':user,'staff':staff,'pagination':'STAFF'})


# Renders the user profile page or handles the data update of the user
def userProfile(request, id):
    user = User.objects.get(id = id)
    
    if request.method=='POST':
        if 'AccountInfo' in request.POST:
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.password = request.POST.get('password')
            del request.session['EMAIL']
            request.session['EMAIL'] = user.email
            user.save()
            messages.success(request,"Account is successfully updated")
            return redirect('user:userProfile', id)
        
        if 'ProfileInfo' in request.POST:
            user.firstName = request.POST.get('firstName')
            user.lastName = request.POST.get('lastName')
            user.dateOfBirth = request.POST.get('dateOfBirth')
            user.gender = request.POST.get('gender')
            user.maritalStatus = request.POST.get('maritalStatus')
            user.address = request.POST.get('address')

            user.save()
            messages.success(request,"Profile Info is successfully updated")
            return redirect('user:userProfile', id)

        if 'uploadPicture' in request.POST:
            user.media = request.FILES['imgupload']
            fss =FileSystemStorage()
            user.save()
            return redirect('user:userProfile', id)

    else:
        return render(request, 'userProfile.html',{'user':user})


# Handles deactivation of user account
@csrf_exempt
def deactivateUser(request, id):
    user = User.objects.get(id = id)
    reason=request.POST.get('reason')
    user.status="DEACTIVATED"
    user.reasonDeactivation=reason
    user.save()
    messages.success(request,"Account is deactivated")
    response = {'status': 1}
    return HttpResponse(json.dumps(response), content_type='application/json')


# Handles activation of user account
def activateUser(request, id):
    user = User.objects.get(id = id)
    # status = "DEACTIVATED"
    user.status="OPEN"
    user.reasonDeactivation="Not Applicable"
    user.save()
    messages.success(request,"Account is activated")
    return redirect('user:mainStaff')
    # return redirect('user:staffProfile', id)


# Handles the data update of staff information
def updateStaff(request, id):
    user = User.objects.get(id = id)
    if request.method=='POST':
        user.userRole = request.POST.get('role')
        user.dateJoined = request.POST.get('dateJoined')
        user.save()
        messages.success(request,"Account is successfully updated")
        return redirect('user:mainStaff')
    
    return render(request, 'updateStaff.html',{'user':user})


# Handles the deletion of user account
def deleteUser(request,id):
    try:
        user=User.objects.get(staffID=id)
        user.delete()
        messages.success(request,"User is deleted succesfully..!")
        return redirect('user:mainStaff')
    except User.DoesNotExist:
        messages.success(request,'No record of the user!' + id)
        return redirect('user:mainStaff')


# To search specific staff and render search staff page with related staff records if found.
def searchUser(request):
    user = User.objects.get(email = request.session['EMAIL'])
    if request.method == 'GET':
        query= request.GET.get('keyword')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(staffID__icontains=query) | Q(username__icontains=query)
            results= User.objects.filter(lookups).distinct()
            context={'results': results,'submitbutton': submitbutton, 'pagination':'STAFF','user':user}
            return render(request, 'searchStaff.html', context)
        else:
            return render(request, 'searchStaff.html')
    
    else:
        return render(request, 'searchStaff.html', {'pagination':'STAFF','user':user}) 