from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#  Uniquely identify URL name for User module
app_name = "user"

# Define URL patterns for User module
urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('mainStaff/',views.mainStaff,name='mainStaff'),
    path('addStaff/',views.addStaff,name='addStaff'),
    path('staffProfile/<str:id>',views.staffProfile,name='staffProfile'),
    path('userProfile/<str:id>',views.userProfile,name='userProfile'),
    path('deactivateUser/<str:id>',views.deactivateUser,name='deactivateUser'),
    path('activateUser/<str:id>',views.activateUser,name='activateUser'),
    path('updateStaff/<str:id>',views.updateStaff,name='updateStaff'),
    path('deleteUser/<str:id>',views.deleteUser,name='deleteUser'),
    path('searchUser/',views.searchUser,name='searchUser'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
