from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from equipment.models import Equipment, EquipmentUsage
from user.models import User


# Represents the homepage or root URL of Equipment module. It will redirect system to the mainEquipment view function.
def equipmentIndex(request):
    return redirect('equipment:mainEquipment')


# Renders main equipment page with all records of equipments
def mainEquipment(request):
    user = User.objects.get(email = request.session['EMAIL'])
    equipments = Equipment.objects.all()
    activeEquipments = Equipment.objects.all().filter(equipmentStatus='ACTIVE')
    inactiveEquipments = Equipment.objects.all().filter(equipmentStatus='INACTIVE')
    return render(request, 'mainEquipment.html', {'user':user,'equipments':equipments,'activeEquipments':activeEquipments,'inactiveEquipments':inactiveEquipments})


# Handles addition of new equipment
def addEquipment(request):
    user = User.objects.get(email = request.session['EMAIL'])
    try:

        if request.method=='POST':
            name=request.POST.get('name')
            serialID=request.POST.get('serialID') or None
            status=request.POST.get('status')
            location=request.POST.get('location')
            make=request.POST.get('make')
            model=request.POST.get('model')
            acquiredDate=request.POST.get('acquiredDate') or None
            yearMade=request.POST.get('yearMade')
            purchasedFrom=request.POST.get('purchasedFrom')
            lastMaintenance=request.POST.get('lastMaintenance') or None
            color=request.POST.get('color')
            price=request.POST.get('price') or None
            notes=request.POST.get('notes')
            imgupload = request.FILES.get('imgupload', None)
            fss =FileSystemStorage()
            Equipment(equipmentName=name,equipmentMake=make,equipmentModel=model,equipmentYear=yearMade,equipmentSerialID=serialID,equipmentAcquiredDate=acquiredDate,equipmentLastMaintenance=lastMaintenance,equipmentColor=color,equipmentLocation=location,equipmentPrice=price,equipmentPurchasedFrom=purchasedFrom,equipmentNotes=notes,equipmentStatus=status,equipmentPhoto=imgupload).save()
            messages.success(request,'Equipment record is successfully created.', extra_tags='addEquipment')
            return redirect('equipment:mainEquipment')
        else:
            return render(request, 'addEquipment.html', {'user':user})

    except IntegrityError:
        messages.error(request,'Serial ID of equipment has been recorded before; Must be unique for each equipment.')
        return render(request, 'addEquipment.html', {'user':user})


# Handles update operation of exisiting equipment record
def updateEquipment(request, id):
    user = User.objects.get(email = request.session['EMAIL'])
    equipment = Equipment.objects.get(id = id)
    if request.method=='POST':
        equipment.equipmentName=request.POST.get('name')
        equipment.equipmentSerialID=request.POST.get('serialID') or None
        equipment.equipmentStatus=request.POST.get('status')
        equipment.equipmentLocation=request.POST.get('location')
        equipment.equipmentMake=request.POST.get('make')
        equipment.equipmentModel=request.POST.get('model')
        equipment.equipmentAcquiredDate=request.POST.get('acquiredDate') or None
        equipment.equipmentYear=request.POST.get('yearMade')
        equipment.equipmentPurchasedFrom=request.POST.get('purchasedFrom')
        equipment.equipmentLastMaintenance=request.POST.get('lastMaintenance') or None
        equipment.equipmentColor=request.POST.get('color')
        equipment.equipmentPrice=request.POST.get('price') or None
        equipment.equipmentNotes=request.POST.get('notes')
        if len(request.FILES) != 0:
            equipment.equipmentPhoto = request.FILES['imgupload']
        fss =FileSystemStorage()
        equipment.save()
        messages.success(request,"Equipment is successfully updated")
        return redirect('equipment:mainEquipment')
    
    return render(request, 'updateEquipment.html',{'equipment':equipment,'user':user})


# Handles deletion of exisiting equipment record
def deleteEquipment(request, id):
    try:
        user = User.objects.get(email = request.session['EMAIL'])
        equipment = Equipment.objects.get(id = id)
        if request.method=='POST':
            
            equipment.delete()
            messages.success(request,"Equipment is deleted succesfully..!")
            return redirect('equipment:mainEquipment')
        else:
            return render(request,'deleteEquipment.html',{'equipment':equipment,'user':user})

    except Equipment.DoesNotExist:
        messages.success(request,'No record of the equipment!' + id)
        return redirect('equipment:mainEquipment')


# Handles searching of equipments related to submitted keyword
def searchEquipment(request):
    user = User.objects.get(email = request.session['EMAIL'])
    if request.method == 'GET':
        query= request.GET.get('keyword')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(equipmentName__icontains=query) | Q(equipmentSerialID__icontains=query)
            results= Equipment.objects.filter(lookups).distinct()
            context={'results': results,'submitbutton': submitbutton, 'user':user}
            return render(request, 'searchEquipment.html', context)
        else:
            return render(request, 'searchEquipment.html')
    
    else:
        return render(request, 'searchEquipment.html', {'user':user}) 


# Renders equipment usage page with equipments that have been used by user
def equipmentUsage(request):
    user = User.objects.get(email = request.session['EMAIL'])
    equipmentUsages = EquipmentUsage.objects.all()
    myEquipmentUsages = EquipmentUsage.objects.all().filter(usedBy_user=user)
    return render(request, 'equipmentUsage.html', {'user':user, 'equipmentUsages':equipmentUsages,'myEquipmentUsages':myEquipmentUsages })


# Handles addition of new equipment usage by user
def addEquipmentUsage(request):
    user = User.objects.get(email = request.session['EMAIL'])
    # equipments = Equipment.objects.all()
    activeEquipments = Equipment.objects.all().filter(equipmentStatus='ACTIVE')
    inUsedEquipmentUsages = EquipmentUsage.objects.all().filter(statusUsage='IN-USED')
    # availableEquipments = activeEquipments.exclude(id__in=inUsedEquipmentUsages)
    availableEquipments = activeEquipments.exclude(usedEquipment__statusUsage='IN-USED')
    try:

        if request.method=='POST':
            equipmentID=request.POST.get('equipmentID')
            usageInfo=request.POST.get('usageInfo')
            dateUsed=request.POST.get('dateUsed')
            statusUsage=request.POST.get('statusUsage')
            
            equipment = Equipment.objects.get(id = equipmentID)
            EquipmentUsage(dateUsed=dateUsed,statusUsage=statusUsage,usageInfo=usageInfo,equipmentID_equip=equipment,usedBy_user=user).save()
            messages.success(request,'Equipment usage is successfully recorded.', extra_tags='addEquipmentUsage')
            return redirect('equipment:equipmentUsage')
        
        else:
            return render(request, 'addEquipmentUsage.html', {'user':user,'equipments':availableEquipments})

    except IntegrityError:
        messages.error(request,'error' + equipmentID + ' ' + usageInfo + ' ' + dateUsed + ' ' + statusUsage)
        return render(request, 'addEquipmentUsage.html', {'user':user,'equipments':availableEquipments})


# Handles update operation on existing records of user's equipment usage
def updateEquipmentUsage(request, id):
    user = User.objects.get(email = request.session['EMAIL'])
    equipmentUsage = EquipmentUsage.objects.get(id=id)
    if request.method=='POST':
        equipmentUsage.statusUsage=request.POST.get('statusUsage')
        equipmentUsage.save()
        messages.success(request,"Equipment status usage is successfully updated")
        return redirect('equipment:equipmentUsage')
    
    return render(request, 'updateEquipmentUsage.html',{'equipment':equipmentUsage,'user':user})


# Renders equipment page with information of a specific equipment
def viewEquipment(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    equipment = Equipment.objects.get(id=id)
    return render(request, 'viewEquipment.html', {'user':user,'equipment':equipment})