from django.contrib import admin
from django.urls import path
# from django.urls import include
from django.urls import include

urlpatterns = [
    path('', include('logins.urls')),
    path('admin/', admin.site.urls),
]
