"""
URL configuration for basketball_project project.
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('basketball.urls')),
    # TODO: Implementar vistas adicionales
]
