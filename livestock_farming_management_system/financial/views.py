from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q, Sum
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from financial.models import Expense, Income, SaleTicket, SoldCattle, SoldSheep
import datetime
from django.utils import timezone
from user.models import User
from animal.models import Cattle,Sheep

from io import BytesIO
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.views.generic import View

# Represents the homapage or root URL of Financial module. It will redirect system to the mainFinancial view function.
def financialIndex(request):
    return redirect('financial:mainFinancial')


# Render dashboard page with latest financial data regarding to business sales and animal inventory
def dashboard(request):
    user = User.objects.get(email = request.session['EMAIL'])
    today=datetime.datetime.now()
    salesYtd = SaleTicket.objects.filter(saleDate__year=today.year, saleTicketInvoiceStatus="VALID")

    janSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='1',saleTicketInvoiceStatus="VALID")
    totalJanSalesYtd = sum(total.saleTotalAmount for total in janSalesYtd )

    febSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='2',saleTicketInvoiceStatus="VALID")
    totalFebSalesYtd = sum(total.saleTotalAmount for total in febSalesYtd )
    
    macSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='3',saleTicketInvoiceStatus="VALID")
    totalMacSalesYtd = sum(total.saleTotalAmount for total in macSalesYtd )
    
    aprSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='4',saleTicketInvoiceStatus="VALID")
    totalAprSalesYtd = sum(total.saleTotalAmount for total in aprSalesYtd )
    
    maySalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='5',saleTicketInvoiceStatus="VALID")
    totalMaySalesYtd = sum(total.saleTotalAmount for total in maySalesYtd )
    
    junSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='6',saleTicketInvoiceStatus="VALID")
    totalJunSalesYtd = sum(total.saleTotalAmount for total in junSalesYtd )
    
    julSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='7',saleTicketInvoiceStatus="VALID")
    totalJulSalesYtd = sum(total.saleTotalAmount for total in julSalesYtd )
    
    augSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='8',saleTicketInvoiceStatus="VALID")
    totalAugSalesYtd = sum(total.saleTotalAmount for total in augSalesYtd )
    
    sepSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='9',saleTicketInvoiceStatus="VALID")
    totalSepSalesYtd = sum(total.saleTotalAmount for total in sepSalesYtd )
    
    octSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='10',saleTicketInvoiceStatus="VALID")
    totalOctSalesYtd = sum(total.saleTotalAmount for total in octSalesYtd )
    
    novSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='11',saleTicketInvoiceStatus="VALID")
    totalNovSalesYtd = sum(total.saleTotalAmount for total in novSalesYtd )
    
    decSalesYtd = SaleTicket.objects.filter(saleDate__year=today.year,saleDate__month='12',saleTicketInvoiceStatus="VALID")
    totalDecSalesYtd = sum(total.saleTotalAmount for total in decSalesYtd )

    salesYtdArray = [totalJanSalesYtd,totalFebSalesYtd,totalMacSalesYtd,totalAprSalesYtd,totalMaySalesYtd,totalJunSalesYtd,totalJulSalesYtd,totalAugSalesYtd,totalSepSalesYtd,totalOctSalesYtd,totalNovSalesYtd,totalDecSalesYtd]

    soldCattleArray=[]
    for x in range(1, 13):
        soldCattle=countSoldCattle(x)
        soldCattleArray.append(soldCattle)

    soldSheepArray=[]
    for x in range(1, 13):
        soldSheep=countSoldSheep(x)
        soldSheepArray.append(soldSheep)


    sumSoldCattleArray=[]
    for x in range(1, 13):
        sumSoldCattle=aggSumSoldCattle(x)
        sumSoldCattleArray.append(sumSoldCattle)

    sumSoldSheepArray=[]
    for x in range(1, 13):
        sumSoldSheep=aggSumSoldSheep(x)
        sumSoldSheepArray.append(sumSoldSheep)


    cattleInfo=[]
    sheepInfo=[]
    calvingCow=Cattle.objects.filter(cattleType="COW",cattleStatus="ACTIVE").count()
    calvingEwe=Sheep.objects.filter(sheepType="EWE",sheepStatus="ACTIVE").count()
    breedingBull=Cattle.objects.filter(cattleType="BULL",cattleStatus="ACTIVE").count()
    breedingRam=Sheep.objects.filter(sheepType="RAM",sheepStatus="ACTIVE").count()
    weaningCattle=Cattle.objects.filter(cattleWeaningStatus="YES",cattleStatus="ACTIVE").count()
    weaningSheep=Sheep.objects.filter(sheepWeaningStatus="YES",sheepStatus="ACTIVE").count()
    today=datetime.datetime.now()
    yearlingCattle=Cattle.objects.filter(cattleBirthDate__gte=timezone.now()-timezone.timedelta(weeks=72)).count()
    yearlingSheep=Sheep.objects.filter(sheepBirthDate__gte=today-datetime.timedelta(weeks=72)).count()
    cattleInfo=[calvingCow,breedingBull,weaningCattle,yearlingCattle]
    sheepInfo=[calvingEwe,breedingRam,weaningSheep,yearlingSheep]

    cattleType=[]
    activeBulls=Cattle.objects.all().filter(cattleType='BULL',cattleStatus='ACTIVE').count
    activeCows=Cattle.objects.all().filter(cattleType='COW',cattleStatus='ACTIVE').count
    activeCalves=Cattle.objects.all().filter(cattleType='CALF',cattleStatus='ACTIVE').count
    sheepType=[]
    activeRam=Sheep.objects.all().filter(sheepType='RAM',sheepStatus='ACTIVE').count
    activeEwe=Sheep.objects.all().filter(sheepType='EWE',sheepStatus='ACTIVE').count
    activeLamb=Sheep.objects.all().filter(sheepType='LAMB',sheepStatus='ACTIVE').count
    cattleType=[activeBulls,activeCows,activeCalves]
    sheepType=[activeRam,activeEwe,activeLamb]

    return render(request,'dashboard.html', {'user':user,'salesYtd':salesYtd, 'yearNow':today.year,'rangeMonth':range(12),'salesYtdArray':salesYtdArray,'soldCattleArray':soldCattleArray,'soldSheepArray':soldSheepArray,'cattleInfo':cattleInfo,'sheepInfo':sheepInfo,'cattleType':cattleType,'sheepType':sheepType, 'sumSoldSheepArray':sumSoldSheepArray,'sumSoldCattleArray':sumSoldCattleArray})


# filter and count number of sold cattle and return the result
def countSoldCattle(month):
    soldCattle=SoldCattle.objects.all().filter(sc_saleTicket__saleDate__month=month, sc_saleTicket__saleTicketInvoiceStatus='VALID').count()
    return soldCattle


# filter and count number of sold sheep and return the result
def countSoldSheep(month):
    soldSheep=SoldSheep.objects.all().filter(ss_saleTicket__saleDate__month=month, ss_saleTicket__saleTicketInvoiceStatus='VALID').count()
    return soldSheep


# filter and count number of sold cattle and return the result
def aggSumSoldCattle(month):
    sumSoldCattle=SoldCattle.objects.all().filter(sc_saleTicket__saleDate__month=month, sc_saleTicket__saleTicketInvoiceStatus='VALID').aggregate(Sum('sc_salePrice'))
    return sumSoldCattle


# filter and count number of sold sheep and return the result
def aggSumSoldSheep(month):
    sumSoldSheep=SoldSheep.objects.all().filter(ss_saleTicket__saleDate__month=month, ss_saleTicket__saleTicketInvoiceStatus='VALID').aggregate(Sum('ss_salePrice'))
    return sumSoldSheep


# Renders main financial page with latest yearly financial information
def mainFinancial(request):
    today=datetime.datetime.now()
    user = User.objects.get(email = request.session['EMAIL'])
    salesYtd = SaleTicket.objects.filter(saleDate__year=today.year, saleTicketInvoiceStatus="VALID")
    marketingYtd = sum(marketingCost.saleMarketingCost for marketingCost in salesYtd)
    
    cattleSold = SoldCattle.objects.filter(sc_saleTicket__in=salesYtd)
    totalCattleSalesYtd=sum(soldCattle.sc_salePrice for soldCattle in cattleSold)
    sheepSold = SoldSheep.objects.filter(ss_saleTicket__in=salesYtd)
    totalSheepSalesYtd=sum(soldSheep.ss_salePrice for soldSheep in sheepSold)
    totalSalesYtd = totalCattleSalesYtd+totalSheepSalesYtd

    incomesYtd = Income.objects.filter(incomeMadeDate__year=today.year)
    totalIncomesYtd = sum(income.incomeAmount for income in incomesYtd)
    expensesYtd = Expense.objects.filter(expenseMadeDate__year=today.year)
    totalExpensesYtd = sum(expense.expenseAmount for expense in expensesYtd)

    grossProfitYtd = totalCattleSalesYtd+totalSheepSalesYtd+totalIncomesYtd-marketingYtd
    netIncomeYtd=grossProfitYtd-totalExpensesYtd

    return render(request, 'mainFinancial.html', {'user':user,'totalSalesYtd':totalSalesYtd,'totalIncomesYtd':totalIncomesYtd,'totalExpensesYtd':totalExpensesYtd,'totalCattleSalesYtd':totalCattleSalesYtd,'totalSheepSalesYtd':totalSheepSalesYtd,'marketingYtd':marketingYtd,'grossProfitYtd':grossProfitYtd,'netIncomeYtd':netIncomeYtd})


# Renders main income page with latest income records
def mainIncome(request):
    user = User.objects.get(email = request.session['EMAIL'])
    incomes = Income.objects.all()
    return render(request, 'mainIncome.html', {'user':user,'incomes':incomes})


# Renders main income page with latest expense records
def mainExpense(request):
    user = User.objects.get(email = request.session['EMAIL'])
    expenses=Expense.objects.all()
    return render(request, 'mainExpense.html', {'user':user,'expenses':expenses})


# Renders main sale ticket page with latest sale ticket records
def mainSaleTicket(request):
    user = User.objects.get(email = request.session['EMAIL'])
    saleTickets=SaleTicket.objects.all()
    return render(request, 'mainSaleTicket.html', {'user':user,'saleTickets':saleTickets})


# Handles addition of new income or renders the add income page
def addIncome(request):
    user = User.objects.get(email = request.session['EMAIL'])
    try:

        if request.method=='POST':
            item=request.POST.get('item')
            amount=request.POST.get('amount')
            invoice=request.POST.get('invoice')
            customer=request.POST.get('customer')
            category=request.POST.get('category')
            madeDate=request.POST.get('madeDate') or None
            # lastUpdatedBy=user
            # recordedBy=user
            attachment = request.FILES.get('fileupload', None)
            fss =FileSystemStorage()
            Income(incomeItem=item,incomeAmount=amount,incomeCategory=category,incomeCustomer=customer,incomeInvoice=invoice,incomeMadeDate=madeDate,incomeAttachment=attachment,incomeLastUpdatedBy=user,incomeRecordedBy=user).save()
            messages.success(request,'Income is successfully created.', extra_tags='addIncome')
            return redirect('financial:mainIncome')
        else:
            return render(request, 'addIncome.html', {'user':user})

    except Exception as e:
        raise e

    except IntegrityError:
        messages.error(request,'Error Income')
        return render(request, 'addIncome.html', {'user':user})


# Renders income view page with specific income record
def viewIncome(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    income = Income.objects.get(id=id)
    return render(request, 'viewIncome.html', {'user':user,'income':income})


# Handles update operation of a current existing record of income or renders the update income page
def updateIncome(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    income = Income.objects.get(id=id)
    if request.method=='POST':
        income.incomeItem=request.POST.get('item')
        income.incomeAmount=request.POST.get('amount')
        income.incomeInvoice=request.POST.get('invoice')
        income.incomeCustomer=request.POST.get('customer')
        income.incomeCategory=request.POST.get('category')
        income.incomeMadeDate=request.POST.get('madeDate')
        income.LastUpdatedBy = user
        if len(request.FILES) != 0:
            if income.incomeAttachment!=None or income.incomeAttachment!='':
                income.incomeAttachment.delete()
            income.incomeAttachment = request.FILES['fileupload']
            fss =FileSystemStorage()
        
        income.save()
        messages.success(request,"Income is successfully updated")
        return redirect('financial:mainIncome')
    
    return render(request, 'updateIncome.html', {'user':user,'income':income})


# Handles deletion of current existing record of income or renders the delete income page
def deleteIncome(request,id):
    try:
        user = User.objects.get(email = request.session['EMAIL'])
        income = Income.objects.get(id=id)
        if request.method=='POST':
            if income.incomeAttachment!=None or income.incomeAttachment!='':
                income.incomeAttachment.delete()
            income.delete()
            messages.success(request,"Income is deleted succesfully..!")
            return redirect('financial:mainIncome')
        else:
            return render(request, 'deleteIncome.html', {'user':user,'income':income})

    except Income.DoesNotExist:
        messages.success(request,'No record of the income!' + id)
        return redirect('financial:mainIncome')


# expense-related views


# Handles addition of new expense or renders the add expense page
def addExpense(request):
    user = User.objects.get(email = request.session['EMAIL'])
    staff=User.objects.all()
    try:

        if request.method=='POST':
            name=request.POST.get('name')
            amount=request.POST.get('amount')
            category=request.POST.get('category')
            note=request.POST.get('note')
            madeDate=request.POST.get('madeDate') or None
            selectedUserID=request.POST.get('madeBy')
            selectedUser = User.objects.get(id = selectedUserID)
            attachment = request.FILES.get('fileupload', None)
            fss =FileSystemStorage()
            Expense(expenseName=name,expenseAmount=amount,expenseCategory=category,expenseNote=note,expenseMadeDate=madeDate,expenseAttachment=attachment,expenseLastUpdatedBy=user,expenseMadeBy=selectedUser).save()
            messages.success(request,'Expense is successfully created.', extra_tags='addIncome')
            return redirect('financial:mainExpense')
        else:
            return render(request, 'addExpense.html', {'user':user,'staff':staff})

    except Exception as e:
        raise e

    except IntegrityError:
        messages.error(request,'Error Expense')
        return render(request, 'addExpense.html', {'user':user,'staff':staff})


# Renders expense view page with specific expense record
def viewExpense(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    expense = Expense.objects.get(id=id)
    return render(request, 'viewExpense.html', {'user':user,'expense':expense})


# Handles update operation of a current existing record of expense or renders the expense income page
def updateExpense(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    expense = Expense.objects.get(id=id)
    staff=User.objects.all()
    if request.method=='POST':
        expense.expenseName =request.POST.get('name')
        expense.expenseAmount=request.POST.get('amount')
        expense.expenseNote=request.POST.get('note')
        expense.expenseCustomer=request.POST.get('customer')
        expense.expenseCategory=request.POST.get('category')
        expense.expenseMadeDate=request.POST.get('madeDate')
        selectedUserID=request.POST.get('madeBy')
        expense.expenseMadeBy = User.objects.get(id = selectedUserID)
        expense.expenseLastUpdatedBy = user
        if len(request.FILES) != 0:
            if expense.expenseAttachment!=None or expense.expenseAttachment!='':
                expense.expenseAttachment.delete()
            expense.expenseAttachment = request.FILES['fileupload']
            fss =FileSystemStorage()
        
        expense.save()
        messages.success(request,"Expense is successfully updated")
        return redirect('financial:mainExpense')
    
    return render(request, 'updateExpense.html', {'user':user,'expense':expense,'staff':staff})


# Handles deletion of current existing record of expense or renders the expense income page
def deleteExpense(request,id):
    try:
        user = User.objects.get(email = request.session['EMAIL'])
        expense = Expense.objects.get(id=id)
        if request.method=='POST':
            if expense.expenseAttachment!=None or expense.expenseAttachment!='':
                expense.expenseAttachment.delete()
            expense.delete()
            messages.success(request,"Expense is deleted succesfully..!")
            return redirect('financial:mainExpense')
        else:
            return render(request, 'deleteExpense.html', {'user':user,'expense':expense})

    except Expense.DoesNotExist:
        messages.success(request,'No record of the expense!' + id)
        return redirect('financial:mainExpense')


# saleTicket-related views

# Handles addition of new sale ticket or renders the add sale ticket page
def addSaleTicket(request):
    user = User.objects.get(email = request.session['EMAIL'])
    staff=User.objects.all()
    activeCattle=Cattle.objects.all().filter(cattleStatus='ACTIVE')
    activeSheep=Sheep.objects.all().filter(sheepStatus='ACTIVE')
    try:

        if request.method=='POST':
            invoice=request.POST.get('invoice')
            customer=request.POST.get('customer')
            saleDate=request.POST.get('saleDate') or None
            remarks=request.POST.get('remarks')
            attachment = request.FILES.get('fileupload', None)

            # saleTicketID=SaleTicket(saleTicketInvoice=invoice,soldToCustomer=customer,saleComment=remarks,saleDate=saleDate,saleAttachment=attachment,saleLastUpdatedBy=user,saleRecordedBy=user).save()
            saleTicketID=SaleTicket(saleTicketInvoice=invoice,soldToCustomer=customer,saleComment=remarks,saleDate=saleDate,saleAttachment=attachment,saleLastUpdatedBy=user,saleRecordedBy=user,saleTicketInvoiceStatus="VALID").save()
            saleTicket=SaleTicket.objects.get(id=saleTicketID)

            selectedCattle=request.POST.getlist('SelectedCattle')
            for cattleID in selectedCattle:
                cattle=Cattle.objects.get(id=cattleID)
                cattle.cattleStatus = "SOLD"
                cattle.save()
                SoldCattle(sc_cattle=cattle,sc_saleTicket=saleTicket).save()

            selectedSheep=request.POST.getlist('SelectedSheep')
            for sheepID in selectedSheep:
                sheep=Sheep.objects.get(id=sheepID)
                sheep.sheepStatus = "SOLD"
                sheep.save()
                SoldSheep(ss_sheep=sheep,ss_saleTicket=saleTicket).save()

            fss =FileSystemStorage()
            messages.success(request,'Sale Ticket is successfully created.', extra_tags='addIncome')
            return redirect('financial:updateSoldAnimals', saleTicket.id)
        else:
            return render(request, 'addSaleTicket.html', {'user':user,'staff':staff,'activeCattle':activeCattle,'activeSheep':activeSheep})

    except Exception as e:
        raise e

    except IntegrityError:
        messages.error(request,'Error Expense')
        return render(request, 'addExpense.html', {'user':user,'staff':staff})


# Renders sale ticket view page with specific sale ticket record
def viewSaleTicket(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    saleTicket = SaleTicket.objects.get(id=id)
    cattleSold = SoldCattle.objects.filter(sc_saleTicket=id)
    totalPriceCattle=sum(soldCattle.sc_salePrice for soldCattle in cattleSold)
    sheepSold = SoldSheep.objects.filter(ss_saleTicket=id)
    totalPriceSheep=sum(soldSheep.ss_salePrice for soldSheep in sheepSold)
    netWorth = totalPriceCattle+totalPriceSheep-saleTicket.saleMarketingCost
    return render(request, 'viewSaleTicket.html', {'user':user,'saleTicket':saleTicket,'totalPriceCattle':totalPriceCattle,'totalPriceSheep':totalPriceSheep,'netWorth':netWorth})


# Handles update operation of a current existing record of sold animals or renders the update sold animals page
def updateSoldAnimals(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    saleTicket = SaleTicket.objects.get(id=id)
    soldCattles = SoldCattle.objects.all().filter(sc_saleTicket=saleTicket)
    soldSheeps = SoldSheep.objects.all().filter(ss_saleTicket=saleTicket)
    if request.method=='POST':
        
        saleTicket.saleMarketingCost=request.POST.get('marketingCost')
        saleTicket.save()

        for cattleSoldObjectID in request.POST.getlist('soldCattleObjects'):
            cattleSold = SoldCattle.objects.get(id=cattleSoldObjectID)
            cattlesalePrice = request.POST.get('cattlePrice_%s'%cattleSoldObjectID)
            cattlesaleWeight = request.POST.get('cattleSaleWeight_%s'%cattleSoldObjectID)
            cattlepricePerKg = request.POST.get('cattlePriceperkg_%s'%cattleSoldObjectID)

            cattleSold.sc_salePrice=cattlesalePrice
            cattleSold.sc_saleWeight=cattlesaleWeight
            cattleSold.sc_pricePerKg=cattlepricePerKg

            cattleSold.save()

            cattle = Cattle.objects.get(id=cattleSold.sc_cattle.id)
            cattle.cattleStatus = "SOLD"
            cattle.save()

        for sheepSoldObjectID in request.POST.getlist('soldSheepObjects'):
            sheepSold = SoldSheep.objects.get(id=sheepSoldObjectID)
            sheepsalePrice = request.POST.get('sheepPrice_%s'%sheepSoldObjectID)
            sheepsaleWeight = request.POST.get('sheepSaleWeight_%s'%sheepSoldObjectID)
            sheeppricePerKg = request.POST.get('sheepPriceperkg_%s'%sheepSoldObjectID)

            sheepSold.ss_salePrice=sheepsalePrice
            sheepSold.ss_saleWeight=sheepsaleWeight
            sheepSold.ss_pricePerKg=sheeppricePerKg

            sheepSold.save()

            sheep = Sheep.objects.get(id=sheepSold.ss_sheep.id)
            sheep.sheepStatus = "SOLD"
            sheep.save()

        # cattleSold = SoldCattle.objects.filter(sc_saleTicket=id)
        totalPriceCattle=sum(soldCattle.sc_salePrice for soldCattle in soldCattles)
        # sheepSold = SoldSheep.objects.filter(ss_saleTicket=id)
        totalPriceSheep=sum(soldSheep.ss_salePrice for soldSheep in soldSheeps)
        totalPriceAmount = totalPriceCattle+totalPriceSheep
        saleTicket.saleTotalAmount=totalPriceAmount
        saleTicket.save()

            
        messages.success(request,"Sale Ticket is successfully updated")
        return redirect('financial:viewSaleTicket',id)
    
    return render(request, 'updateSoldAnimals.html', {'user':user,'saleTicket':saleTicket,'soldCattles':soldCattles,'soldSheeps':soldSheeps})


# Handles update operation of a current existing record of sale ticket or renders the update sale ticket page
def updateSaleTicket(request,id):
    user = User.objects.get(email = request.session['EMAIL'])
    saleTicket = SaleTicket.objects.get(id=id)
    if request.method=='POST':
        saleTicket.saleMarketingCost=request.POST.get('saleMarketingCost')
        saleTicket.soldToCustomer=request.POST.get('customer')
        saleTicket.saleComment=request.POST.get('remarks')
        saleTicket.saleDate=request.POST.get('saleDate')
        saleTicket.saleLastUpdatedBy = user
        if len(request.FILES) != 0:
            if saleTicket.saleAttachment!=None or saleTicket.saleAttachment!='':
                saleTicket.saleAttachment.delete()
            saleTicket.saleAttachment = request.FILES['fileupload']
            fss =FileSystemStorage()
        
        saleTicket.save()
        messages.success(request,"Sale ticket is successfully updated")
        return redirect('financial:viewSaleTicket',id)
    
    return render(request, 'updateSaleTicket.html', {'user':user,'saleTicket':saleTicket})


# Handles cancelling operation of a sale ticket or renders the cancel sale ticket page
def cancelSaleTicket(request,id):
    try:
        user = User.objects.get(email = request.session['EMAIL'])
        saleTicket = SaleTicket.objects.get(id=id)
        if request.method=='POST':
            saleTicket.saleComment=request.POST.get('remarks')
            saleTicket.saleTicketInvoiceStatus='CANCELLED'
            saleTicket.save()
            cattleSold = SoldCattle.objects.filter(sc_saleTicket=id)
            # cattle = Cattle.objects.filter(id__in=cattleSold.sc_cattle.id)
            sheepSold = SoldSheep.objects.filter(ss_saleTicket=id)
            # sheep = Sheep.objects.filter(id__in=sheepSold.ss_sheep)
            for cattle in cattleSold:
                cattle.sc_cattle.cattleStatus='ACTIVE'
                cattle.sc_cattle.save()
            for sheep in sheepSold:
                sheep.ss_sheep.sheepStatus='ACTIVE'
                sheep.ss_sheep.save()
                
            messages.success(request,"Sale Ticket is cancelled succesfully..! All related animals' status is changed to ACTIVE!")
            return redirect('financial:mainSaleTicket')
        else:
            return render(request, 'cancelSaleTicket.html', {'user':user,'saleTicket':saleTicket})

    except SaleTicket.DoesNotExist:
        messages.success(request,'No record of the sale ticket!' + id)
        return redirect('financial:mainSaleTicket')


# Handles searching animals operation related to sent keyword and return related animals
def searchAnimalForSaleTicket(request,key):
    # user = User.objects.get(email = request.session['EMAIL'])
    searchKey=key
        # print(request.body)
        # searchKey='LP'
        # submitbutton= request.GET.get('submit')
    if searchKey is not None:
        lookupsCattle= Q(cattleTagID__icontains=searchKey) | Q(cattleType__icontains=searchKey)
        # resultCattle= Cattle.objects.filter(lookupsCattle).distinct()
        resultCattle= list(Cattle.objects.filter(lookupsCattle).distinct().values().filter(cattleStatus='ACTIVE'))
        lookupsSheep= Q(sheepTagID__icontains=searchKey) | Q(sheepType__icontains=searchKey)
        # resultSheep= Sheep.objects.filter(lookupsSheep).distinct()
        resultSheep= list(Sheep.objects.filter(lookupsSheep).distinct().values().filter(sheepStatus='ACTIVE'))
        # context={'results': results,'submitbutton': submitbutton, 'user':user}
        context={'resultCattle': resultCattle,'resultSheep':resultSheep}
    else:
        context={'resultCattle': '0','resultSheep':'0'}
    # return JsonResponse({'resultCattle': resultCattle,'resultSheep':resultSheep, 'user':user})
    return JsonResponse(context)


# Handles searching sale ticket according to submitted keywords and renders the result of related records
def searchSaleTicket(request):
    user = User.objects.get(email = request.session['EMAIL'])
    if request.method == 'GET':
        query= request.GET.get('keyword')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(saleTicketInvoice__icontains=query) | Q(soldToCustomer__icontains=query)
            results= SaleTicket.objects.filter(lookups).distinct()
            context={'results': results,'submitbutton': submitbutton, 'user':user}
            return render(request, 'searchSaleTicket.html', context)
        else:
            return render(request, 'searchSaleTicket.html')
    
    else:
        return render(request, 'searchSaleTicket.html', {'user':user}) 
    

#  Handles searching income according to submitted keywords and renders the result of related records
def searchIncome(request):
    user = User.objects.get(email = request.session['EMAIL'])
    if request.method == 'GET':
        query= request.GET.get('keyword')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(incomeItem__icontains=query) | Q(incomeInvoice__icontains=query)
            results= Income.objects.filter(lookups).distinct()
            context={'results': results,'submitbutton': submitbutton, 'user':user}
            return render(request, 'searchIncome.html', context)
        else:
            return render(request, 'searchIncome.html')
    
    else:
        return render(request, 'searchIncome.html', {'user':user}) 


#  Handles searching expense according to submitted keywords and renders the result of related records
def searchExpense(request):
    user = User.objects.get(email = request.session['EMAIL'])
    if request.method == 'GET':
        query= request.GET.get('keyword')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(expenseName__icontains=query) | Q(expenseCategory__icontains=query)
            results= Expense.objects.filter(lookups).distinct()
            context={'results': results,'submitbutton': submitbutton, 'user':user}
            return render(request, 'searchExpense.html', context)
        else:
            return render(request, 'searchExpense.html')
    
    else:
        return render(request, 'searchExpense.html', {'user':user}) 
    

#  Handles converting html context to pdf view
def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


# class GeneratePdf(View):
    #  def get(self, request, *args, **kwargs):
         
    #     # getting the template
    #     pdf = html_to_pdf('result.html')
         
    #      # rendering the template
    #     return HttpResponse(pdf, content_type='application/pdf')


# Handles generating pdf type of application according to related view
def generatedPdf(request, id):
    saleTicket = SaleTicket.objects.get(id=id)
    cattleSold = SoldCattle.objects.filter(sc_saleTicket=id)
    totalPriceCattle=sum(soldCattle.sc_salePrice for soldCattle in cattleSold)
    sheepSold = SoldSheep.objects.filter(ss_saleTicket=id)
    totalPriceSheep=sum(soldSheep.ss_salePrice for soldSheep in sheepSold)
    pdf=html_to_pdf('result.html',{'saleTicket':saleTicket,'totalPriceCattle':totalPriceCattle,'totalPriceSheep':totalPriceSheep})
    return HttpResponse(pdf, content_type='application/pdf')