from django.contrib import admin
from django.urls import path, re_path

from MainMenu.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^(?P<path>.*)$', base_pattern, name='base_pattern'),
]