from django.shortcuts import render,redirect
from django.contrib import messages
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from animal.models import Cattle, CattleGroup, CattleGrouping, Sheep, SheepGroup, SheepGrouping
from django.utils import timezone
from user.models import User
from django.db.models import Q
import datetime
# Create your views here.


# Represents the homepage or root URL of Animal module. It will redirect system to the mainAnimal view function.
def animalIndex(request):
    return redirect('animal:mainAnimal')


# Renders main animal page with several categories of animals
def mainAnimal(request):
    user = User.objects.get(email = request.session['EMAIL'])

    calvingCow=Cattle.objects.filter(cattleType="COW",cattleStatus="ACTIVE").count()
    calvingEwe=Sheep.objects.filter(sheepType="EWE",sheepStatus="ACTIVE").count()
    breedingBull=Cattle.objects.filter(cattleType="BULL",cattleStatus="ACTIVE").count()
    breedingRam=Sheep.objects.filter(sheepType="RAM",sheepStatus="ACTIVE").count()
    weaningCattle=Cattle.objects.filter(cattleWeaningStatus="YES",cattleStatus="ACTIVE").count()
    weaningSheep=Sheep.objects.filter(sheepWeaningStatus="YES",sheepStatus="ACTIVE").count()
    today=datetime.datetime.now()
    yearlingCattle=Cattle.objects.filter(cattleBirthDate__gte=timezone.now()-timezone.timedelta(weeks=72)).count()
    yearlingSheep=Sheep.objects.filter(sheepBirthDate__gte=today-datetime.timedelta(weeks=72)).count()
    return render(request, 'mainAnimal.html', {'user':user,'breedingBull':breedingBull,'breedingRam':breedingRam,'weaningCattle':weaningCattle,'weaningSheep':weaningSheep,'calvingCow':calvingCow,'calvingEwe':calvingEwe,'yearlingCattle':yearlingCattle,'yearlingSheep':yearlingSheep})


# Renders all animals page with animal records
def allAnimals(request):
    user = User.objects.get(email = request.session['EMAIL'])
    cattle=Cattle.objects.all()
    sheep=Sheep.objects.all()
    allAnimals=[]
    allAnimals.append(cattle)
    allAnimals.append(sheep)
    return render(request, 'allAnimals.html', {'user':user,'cattle':cattle,'sheep':sheep,'allAnimals':allAnimals})


# cattle-related views

# Renders main cattle page with latest cattles and cattle groups
def mainCattle(request):
    user = User.objects.get(email = request.session['EMAIL'])
    allCattle=Cattle.objects.all()
    activeBulls=Cattle.objects.all().filter(cattleType='BULL',cattleStatus='ACTIVE')
    activeCows=Cattle.objects.all().filter(cattleType='COW',cattleStatus='ACTIVE')
    activeCalves=Cattle.objects.all().filter(cattleType='CALF',cattleStatus='ACTIVE')
    activeCattle=Cattle.objects.all().filter(cattleStatus='ACTIVE')
    purchasedCattle=Cattle.objects.all().filter(cattleRaisedOrPurchased='PURCHASED')
    soldCattle=Cattle.objects.all().filter(cattleStatus='SOLD')
    cattleGroups=CattleGroup.objects.all()
    return render(request, 'mainCattle.html', {'user':user,'allCattle':allCattle,'activeBulls':activeBulls,'activeCows':activeCows,'activeCalves':activeCalves,'activeCattle':activeCattle,'purchasedCattle':purchasedCattle,'soldCattle':soldCattle,'cattleGroups':cattleGroups})


# Handles addition of new cattle
def addCattle(request):
    user = User.objects.get(email = request.session['EMAIL'])
    cattleGroups = CattleGroup.objects.all()
    possibleDam = Cattle.objects.all().filter(cattleType='COW')
    possibleSire = Cattle.objects.all().filter(cattleType='BULL')
    try:

        if request.method=='POST':
            tagID=request.POST.get('tagID')
            tagPosition=request.POST.get('tagPosition')
            type=request.POST.get('type')
            status=request.POST.get('status')
            breed=request.POST.get('breed')
            hornStatus=request.POST.get('hornStatus')
            weaningStatus=request.POST.get('weaningStatus')
            imgupload = request.FILES.get('fileupload', None)
            remark=request.POST.get('remark')
            purchasedOrNot=request.POST.get('purchasedOrNot')
            offerPrice=request.POST.get('offerPrice') or None
            marketingNote=request.POST.get('marketingNote')
            birthdate=request.POST.get('birthdate') or None
            birthWeight=request.POST.get('birthWeight') or None
            sire=request.POST.get('sire') or None
            if sire:
                sire = Cattle.objects.get(id=sire)
            dam=request.POST.get('dam') or None
            if dam:
                dam = Cattle.objects.get(id=dam)

            cattleID=Cattle(cattleTagID=tagID,cattleTagPosition=tagPosition,cattleType=type,cattleStatus=status,cattleHornStatus=hornStatus,cattleBreed=breed,cattleComment=remark,cattleAttachment=imgupload,cattleOfferPrice=offerPrice,cattleRaisedOrPurchased=purchasedOrNot,cattleCommercialNote=marketingNote,cattleBirthDate=birthdate,cattleBirthWeight=birthWeight,cattleWeaningStatus=weaningStatus,cattleLastUpdatedBy=user,cattleSire=sire,cattleDam=dam).save()
            cattle=Cattle.objects.get(id=cattleID)
            groups=request.POST.getlist('cattleGroup')
            for cattleGroup in groups:
                group=CattleGroup.objects.get(id=cattleGroup)
                CattleGrouping(c_cattleID=cattle,cg_cattleGroup=group).save()

            messages.success(request,'Cattle record is successfully created.', extra_tags='addCattle')
            return redirect('animal:mainCattle')
        else:
            return render(request, 'addCattle.html', {'user':user,'cattleGroups':cattleGroups,'possibleDam':possibleDam,'possibleSire':possibleSire})

    except Exception as e:
        # messages.error(request,'Error cattle'+e)
        raise e
        return render(request, 'addCattle.html', {'user':user,'cattleGroups':cattleGroups,'possibleDam':possibleDam,'possibleSire':possibleSire})


# Handles update operation of exisiting cattle
def updateCattle(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    cattle = Cattle.objects.get(id = id)
    cattleGroups = CattleGroup.objects.all()
    possibleDam = Cattle.objects.all().filter(cattleType='COW').exclude(id=cattle.id)
    possibleSire = Cattle.objects.all().filter(cattleType='BULL').exclude(id=cattle.id)
    currentGrouping=CattleGrouping.objects.filter(c_cattleID=cattle)
    if request.method=='POST':
        cattle.cattleTagID=request.POST.get('tagID')
        cattle.cattleTagPosition=request.POST.get('tagPosition')
        cattle.cattleType=request.POST.get('type')
        cattle.cattleStatus=request.POST.get('status')
        cattle.cattleBreed=request.POST.get('breed')
        cattle.cattleHornStatus=request.POST.get('hornStatus')
        cattle.cattleWeaningStatus=request.POST.get('weaningStatus')
        if len(request.FILES) != 0:
            if cattle.cattleAttachment!=None or cattle.cattleAttachment!='':
                cattle.cattleAttachment.delete()
            cattle.cattleAttachment = request.FILES['fileupload']
            fss =FileSystemStorage()
        cattle.cattleComment=request.POST.get('remark')
        cattle.cattleRaisedOrPurchased=request.POST.get('purchasedOrNot')
        cattle.cattleOfferPrice=request.POST.get('offerPrice') or None
        cattle.cattleCommercialNote=request.POST.get('marketingNote')
        cattle.cattleBirthDate=request.POST.get('birthdate') or None
        cattle.cattleBirthWeight=request.POST.get('birthWeight') or None
        sire=request.POST.get('sire') or None
        if sire:
            cattle.cattleSire = Cattle.objects.get(id=sire)
        dam=request.POST.get('dam') or None
        if dam:
            cattle.cattleDam = Cattle.objects.get(id=dam)

        cattle.save()

        currentGroup=CattleGrouping.objects.filter(c_cattleID=cattle)
        if currentGroup:
            for grouping in currentGroup:
                grouping.delete()

        groups=request.POST.getlist('cattleGroup')
        for cattleGroup in groups:
            group=CattleGroup.objects.get(id=cattleGroup)
            CattleGrouping(c_cattleID=cattle,cg_cattleGroup=group).save()

        messages.success(request,'Cattle record is successfully updated.', extra_tags='addCattle')
        return redirect('animal:mainCattle')

    return render(request, 'updateCattle.html', {'user':user,'cattle':cattle,'currentGrouping':currentGrouping,'cattleGroups':cattleGroups,'possibleDam':possibleDam,'possibleSire':possibleSire})


# Renders view cattle page with specific record of cattle
def viewCattle(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    cattle = Cattle.objects.get(id=id)
    currentGrouping=CattleGrouping.objects.filter(c_cattleID=cattle)
    return render(request, 'viewCattle.html', {'user':user,'cattle':cattle,'currentGrouping':currentGrouping})


# Handles deletion of currently exist cattle
def deleteCattle(request,id):
    try:
        user = User.objects.get(email = request.session['EMAIL'])
        cattle = Cattle.objects.get(id = id)
        currentGrouping=CattleGrouping.objects.filter(c_cattleID=cattle)
        if request.method=='POST':
            if cattle.cattleAttachment!=None or cattle.cattleAttachment!='':
                cattle.cattleAttachment.delete()
            cattle.delete()
            messages.success(request,"Cattle is deleted succesfully..!")
            return redirect('animal:mainCattle')
        else:
            return render(request, 'deleteCattle.html', {'user':user,'cattle':cattle,'currentGrouping':currentGrouping})

    except Cattle.DoesNotExist:
        messages.success(request,'No record of the cattle!' + id)
        return redirect('animal:mainCattle')


# Handles addition of new cattle group
def addCattleGroup(request):
    user = User.objects.get(email = request.session['EMAIL'])
    try:

        if request.method=='POST':
            groupName=request.POST.get('groupName')
            CattleGroup(cattleGroupName=groupName).save()
            messages.success(request,'Cattle group is successfully created.', extra_tags='addCattleGroup')
            return redirect('animal:mainCattle')
        else:
            return render(request, 'addCattleGroup.html', {'user':user})

    except IntegrityError:
        messages.error(request,'Error Cattle Group')
        return render(request, 'addCattleGroup.html', {'user':user})


# Renders view cattles related to specific cattle group
def viewRelatedCattle(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    cattleGroup=CattleGroup.objects.get(id=id)
    cattleGrouping = CattleGrouping.objects.filter(cg_cattleGroup=id)
    return render(request, 'viewRelatedCattle.html', {'user':user,'cattleGrouping':cattleGrouping,'cattleGroup':cattleGroup})


# View cattle related to keywords submitted from cattle search feature
def searchCattle(request):
    user = User.objects.get(email = request.session['EMAIL'])
    if request.method == 'GET':
        query= request.GET.get('keyword')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(cattleTagID__icontains=query)
            results= Cattle.objects.filter(lookups).distinct()
            context={'results': results,'submitbutton': submitbutton, 'user':user}
            return render(request, 'searchCattle.html', context)
        else:
            return render(request, 'searchCattle.html')
    
    else:
        return render(request, 'searchEquipment.html', {'user':user}) 
    

# sheep-related views

# Renders main sheep page with latest sheeps and sheep groups
def mainSheep(request):
    user = User.objects.get(email = request.session['EMAIL'])
    allSheep=Sheep.objects.all()
    activeRam=Sheep.objects.all().filter(sheepType='RAM',sheepStatus='ACTIVE')
    activeEwe=Sheep.objects.all().filter(sheepType='EWE',sheepStatus='ACTIVE')
    activeLamb=Sheep.objects.all().filter(sheepType='LAMB',sheepStatus='ACTIVE')
    activeSheep=Sheep.objects.all().filter(sheepStatus='ACTIVE')
    purchasedSheep=Sheep.objects.all().filter(sheepRaisedOrPurchased='PURCHASED')
    soldSheep=Sheep.objects.all().filter(sheepStatus='SOLD')
    sheepGroups=SheepGroup.objects.all()
    return render(request, 'mainSheep.html', {'user':user,'allSheep':allSheep,'activeRam':activeRam,'activeEwe':activeEwe,'activeLamb':activeLamb,'activeSheep':activeSheep,'purchasedSheep':purchasedSheep,'soldSheep':soldSheep,'sheepGroups':sheepGroups})


# Handles addition of new sheep
def addSheep(request):
    user = User.objects.get(email = request.session['EMAIL'])
    sheepGroups = SheepGroup.objects.all()
    possibleDam = Sheep.objects.all().filter(sheepType='EWE')
    possibleSire = Sheep.objects.all().filter(sheepType='RAM')
    try:

        if request.method=='POST':
            tagID=request.POST.get('tagID')
            tagPosition=request.POST.get('tagPosition')
            type=request.POST.get('type')
            status=request.POST.get('status')
            breed=request.POST.get('breed')
            hornStatus=request.POST.get('hornStatus')
            weaningStatus=request.POST.get('weaningStatus')
            imgupload = request.FILES.get('fileupload', None)
            remark=request.POST.get('remark')
            purchasedOrNot=request.POST.get('purchasedOrNot')
            offerPrice=request.POST.get('offerPrice') or None
            marketingNote=request.POST.get('marketingNote')
            birthdate=request.POST.get('birthdate') or None
            birthWeight=request.POST.get('birthWeight') or None
            sire=request.POST.get('sire') or None
            if sire:
                sire = Sheep.objects.get(id=sire)
            dam=request.POST.get('dam') or None
            if dam:
                dam = Sheep.objects.get(id=dam)

            sheepID=Sheep(sheepTagID=tagID,sheepTagPosition=tagPosition,sheepType=type,sheepStatus=status,sheepHornStatus=hornStatus,sheepBreed=breed,sheepComment=remark,sheepAttachment=imgupload,sheepOfferPrice=offerPrice,sheepRaisedOrPurchased=purchasedOrNot,sheepCommercialNote=marketingNote,sheepBirthDate=birthdate,sheepBirthWeight=birthWeight,sheepWeaningStatus=weaningStatus,sheepLastUpdatedBy=user,sheepSire=sire,sheepDam=dam).save()
            sheep=Sheep.objects.get(id=sheepID)
            groups=request.POST.getlist('sheepGroup')
            for sheepGroup in groups:
                group=SheepGroup.objects.get(id=sheepGroup)
                SheepGrouping(s_sheepID=sheep,sg_sheepGroup=group).save()

            messages.success(request,'Sheep record is successfully created.', extra_tags='addSheep')
            return redirect('animal:mainSheep')
        else:
            return render(request, 'addSheep.html', {'user':user,'sheepGroups':sheepGroups,'possibleDam':possibleDam,'possibleSire':possibleSire})

    except Exception as e:
        # messages.error(request,'Error cattle'+e)
        raise e
        return render(request, 'addCattle.html', {'user':user,'cattleGroups':cattleGroups,'possibleDam':possibleDam,'possibleSire':possibleSire})


# Handles update operation of exisiting sheep
def updateSheep(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    sheep = Sheep.objects.get(id = id)
    sheepGroups = SheepGroup.objects.all()
    possibleDam = Sheep.objects.all().filter(sheepType='EWE').exclude(id=sheep.id)
    possibleSire = Sheep.objects.all().filter(sheepType='RAM').exclude(id=sheep.id)
    currentGrouping=SheepGrouping.objects.filter(s_sheepID=sheep)
    if request.method=='POST':
        sheep.sheepTagID=request.POST.get('tagID')
        sheep.sheepTagPosition=request.POST.get('tagPosition')
        sheep.sheepType=request.POST.get('type')
        sheep.sheepStatus=request.POST.get('status')
        sheep.sheepBreed=request.POST.get('breed')
        sheep.sheepHornStatus=request.POST.get('hornStatus')
        sheep.sheepWeaningStatus=request.POST.get('weaningStatus')
        if len(request.FILES) != 0:
            if sheep.sheepAttachment!=None or sheep.sheepAttachment!='':
                sheep.sheepAttachment.delete()
            sheep.sheepAttachment = request.FILES['fileupload']
            fss =FileSystemStorage()
        sheep.sheepComment=request.POST.get('remark')
        sheep.sheepRaisedOrPurchased=request.POST.get('purchasedOrNot')
        sheep.sheepOfferPrice=request.POST.get('offerPrice') or None
        sheep.sheepCommercialNote=request.POST.get('marketingNote')
        sheep.sheepBirthDate=request.POST.get('birthdate') or None
        sheep.sheepBirthWeight=request.POST.get('birthWeight') or None
        sire=request.POST.get('sire') or None
        if sire:
            sheep.sheepSire = Sheep.objects.get(id=sire)
        dam=request.POST.get('dam') or None
        if dam:
            sheep.sheepDam = Sheep.objects.get(id=dam)

        sheep.save()

        currentGroup=SheepGrouping.objects.filter(s_sheepID=sheep)
        if currentGroup:
            for grouping in currentGroup:
                grouping.delete()

        groups=request.POST.getlist('sheepGroup')
        for sheepGroup in groups:
            group=SheepGroup.objects.get(id=sheepGroup)
            SheepGrouping(s_sheepID=sheep,sg_sheepGroup=group).save()

        messages.success(request,'Sheep record is successfully updated.', extra_tags='updateSheep')
        return redirect('animal:mainSheep')

    return render(request, 'updateSheep.html', {'user':user,'sheep':sheep,'currentGrouping':currentGrouping,'sheepGroups':sheepGroups,'possibleDam':possibleDam,'possibleSire':possibleSire})


# Renders view sheep page with specific record of sheep
def viewSheep(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    sheep = Sheep.objects.get(id=id)
    currentGrouping=SheepGrouping.objects.filter(s_sheepID=sheep)
    return render(request, 'viewSheep.html', {'user':user,'sheep':sheep,'currentGrouping':currentGrouping})


# Handles deletion of currently exist sheep
def deleteSheep(request,id):
    try:
        user = User.objects.get(email = request.session['EMAIL'])
        sheep = Sheep.objects.get(id = id)
        currentGrouping=SheepGrouping.objects.filter(s_sheepID=sheep)
        if request.method=='POST':
            if sheep.sheepAttachment!=None or sheep.sheepAttachment!='':
                sheep.sheepAttachment.delete()
            sheep.delete()
            messages.success(request,"Sheep is deleted succesfully..!")
            return redirect('animal:mainSheep')
        else:
            return render(request, 'deleteSheep.html', {'user':user,'sheep':sheep,'currentGrouping':currentGrouping})

    except Sheep.DoesNotExist:
        messages.success(request,'No record of the sheep!' + id)
        return redirect('animal:mainSheep')


# Handles addition of new sheep group
def addSheepGroup(request):
    user = User.objects.get(email = request.session['EMAIL'])
    try:

        if request.method=='POST':
            groupName=request.POST.get('groupName')
            SheepGroup(sheepGroupName=groupName).save()
            messages.success(request,'Sheep group is successfully created.', extra_tags='addSheepGroup')
            return redirect('animal:mainSheep')
        else:
            return render(request, 'addSheepGroup.html', {'user':user})

    except IntegrityError:
        messages.error(request,'Error Sheep Group')
        return render(request, 'addSheepGroup.html', {'user':user})


# Renders view sheeps related to specific sheep group
def viewRelatedSheep(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    sheepGroup=SheepGroup.objects.get(id=id)
    sheepGrouping = SheepGrouping.objects.filter(sg_sheepGroup=id)
    return render(request, 'viewRelatedSheep.html', {'user':user,'sheepGrouping':sheepGrouping,'sheepGroup':sheepGroup})


# View sheep related to keywords submitted from sheep search feature
def searchSheep(request):
    user = User.objects.get(email = request.session['EMAIL'])
    if request.method == 'GET':
        query= request.GET.get('keyword')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(sheepTagID__icontains=query)
            results= Sheep.objects.filter(lookups).distinct()
            context={'results': results,'submitbutton': submitbutton, 'user':user}
            return render(request, 'searchSheep.html', context)
        else:
            return render(request, 'searchSheep.html')
    
    else:
        return render(request, 'searchSheep.html', {'user':user}) 