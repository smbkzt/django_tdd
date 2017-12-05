from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from lists import views as lists_views
from lists import urls as lists_urls

urlpatterns = [
    path('', lists_views.home_page),
    path('admin/', admin.site.urls),
    path('lists/', include(lists_urls)),
]
