from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#  Uniquely identify URL name for Task module
app_name = "task"

# Define URL patterns to be mapped respective view function of Task module
urlpatterns = [
    path('',views.taskIndex,name='taskIndex'),
    path('mainTask/',views.mainTask,name='mainTask'),
    path('addTask/',views.addTask,name='addTask'),
    path('viewTask/<str:id>',views.viewTask,name='viewTask'),
    path('updateTask/<str:id>',views.updateTask,name='updateTask'),
    path('deleteTask/<str:id>',views.deleteTask,name='deleteTask'),
    path('myTask/',views.myTask,name='myTask'),
    path('updateTaskStatus/<str:id>',views.updateTaskStatus,name='updateTaskStatus'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
