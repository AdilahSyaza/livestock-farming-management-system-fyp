from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#  Uniquely identify URL name for Equipment module
app_name = "equipment"

# Define URL patterns to be mapped respective view function of Equipment module
urlpatterns = [
    path('',views.equipmentIndex,name='equipmentIndex'),
    path('mainEquipment/',views.mainEquipment,name='mainEquipment'),
    path('addEquipment/',views.addEquipment,name='addEquipment'),
    path('viewEquipment/<str:id>',views.viewEquipment,name='viewEquipment'),
    path('updateEquipment/<str:id>',views.updateEquipment,name='updateEquipment'),
    path('deleteEquipment/<str:id>',views.deleteEquipment,name='deleteEquipment'),
    path('searchEquipment/',views.searchEquipment,name='searchEquipment'),
    path('equipmentUsage/',views.equipmentUsage,name='equipmentUsage'),
    path('addEquipmentUsage/',views.addEquipmentUsage,name='addEquipmentUsage'),
    path('updateEquipmentUsage/<str:id>',views.updateEquipmentUsage,name='updateEquipmentUsage'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
