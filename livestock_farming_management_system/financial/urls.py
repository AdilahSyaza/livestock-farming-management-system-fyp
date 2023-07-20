from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#  Uniquely identify URL name for Financial module
app_name = "financial"

# Define URL patterns to be mapped respective view function of Financial module
urlpatterns = [
    path('',views.financialIndex,name='financialIndex'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('mainFinancial/',views.mainFinancial,name='mainFinancial'),
    path('mainFinancial/mainIncome/',views.mainIncome,name='mainIncome'),
    path('mainFinancial/mainExpense/',views.mainExpense,name='mainExpense'),
    path('mainFinancial/mainSaleTicket/',views.mainSaleTicket,name='mainSaleTicket'),
    path('mainFinancial/mainIncome/addIncome/',views.addIncome,name='addIncome'),
    path('mainFinancial/mainIncome/viewIncome/<str:id>',views.viewIncome,name='viewIncome'),
    path('mainFinancial/mainIncome/updateIncome/<str:id>',views.updateIncome,name='updateIncome'),
    path('mainFinancial/mainIncome/deleteIncome/<str:id>',views.deleteIncome,name='deleteIncome'),
    path('mainFinancial/mainIncome/searchIncome',views.searchIncome,name='searchIncome'),
    path('mainFinancial/mainExpense/addExpense/',views.addExpense,name='addExpense'),
    path('mainFinancial/mainExpense/viewExpense/<str:id>',views.viewExpense,name='viewExpense'),
    path('mainFinancial/mainExpense/updateExpense/<str:id>',views.updateExpense,name='updateExpense'),
    path('mainFinancial/mainExpense/deleteExpense/<str:id>',views.deleteExpense,name='deleteExpense'),
    path('mainFinancial/mainExpense/searchExpense',views.searchExpense,name='searchExpense'),
    path('mainFinancial/mainSaleTicket/addSaleTicket/',views.addSaleTicket,name='addSaleTicket'),
    path('mainFinancial/mainSaleTicket/searchSaleTicket',views.searchSaleTicket,name='searchSaleTicket'),
    path('mainFinancial/mainSaleTicket/updateSaleTicket/<str:id>',views.updateSaleTicket,name='updateSaleTicket'),
    path('mainFinancial/mainSaleTicket/cancelSaleTicket/<str:id>',views.cancelSaleTicket,name='cancelSaleTicket'),
    path('mainFinancial/mainSaleTicket/updateSoldAnimals/<str:id>',views.updateSoldAnimals,name='updateSoldAnimals'),
    path('mainFinancial/mainSaleTicket/viewSaleTicket/<str:id>',views.viewSaleTicket,name='viewSaleTicket'),
    path('mainFinancial/mainSaleTicket/viewSaleTicket/generatedPdf/<str:id>',views.generatedPdf,name='generatedPdf'),
    path('mainFinancial/mainSaleTicket/searchAnimalForSaleTicket/<str:key>',views.searchAnimalForSaleTicket,name='searchAnimalForSaleTicket'),

    
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
