from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#  Uniquely identify URL name for Animal module
app_name = "animal"

# Define URL patterns to be mapped respective view function of Animal module
urlpatterns = [
    path('',views.animalIndex,name='animalIndex'),
    path('mainAnimal/',views.mainAnimal,name='mainAnimal'),
    path('allAnimals/',views.allAnimals,name='allAnimals'),
    path('mainAnimal/mainCattle/',views.mainCattle,name='mainCattle'),
    path('mainAnimal/mainSheep/',views.mainSheep,name='mainSheep'),
    path('mainAnimal/mainCattle/addCattle/',views.addCattle,name='addCattle'),
    path('mainAnimal/mainCattle/updateCattle/<str:id>',views.updateCattle,name='updateCattle'),
    path('mainAnimal/mainCattle/viewCattle/<str:id>',views.viewCattle,name='viewCattle'),
    path('mainAnimal/mainCattle/deleteCattle/<str:id>',views.deleteCattle,name='deleteCattle'),
    path('mainAnimal/mainCattle/addCattleGroup/',views.addCattleGroup,name='addCattleGroup'),
    path('mainAnimal/mainCattle/viewRelatedCattle/<str:id>',views.viewRelatedCattle,name='viewRelatedCattle'),
    path('mainAnimal/mainCattle/searchCattle/',views.searchCattle,name='searchCattle'),
    path('mainAnimal/mainSheep/addSheep/',views.addSheep,name='addSheep'),
    path('mainAnimal/mainSheep/updateSheep/<str:id>',views.updateSheep,name='updateSheep'),
    path('mainAnimal/mainSheep/viewSheep/<str:id>',views.viewSheep,name='viewSheep'),
    path('mainAnimal/mainSheep/deleteSheep/<str:id>',views.deleteSheep,name='deleteSheep'),
    path('mainAnimal/mainSheep/addSheepGroup/',views.addSheepGroup,name='addSheepGroup'),
    path('mainAnimal/mainSheep/viewRelatedSheep/<str:id>',views.viewRelatedSheep,name='viewRelatedSheep'),
    path('mainAnimal/mainSheep/searchSheep/',views.searchSheep,name='searchSheep'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
