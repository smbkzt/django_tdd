from django.contrib import admin
from django.urls import path

from lists import views

urlpatterns = [
    path('', views.home_page),
    path('admin/', admin.site.urls),
    path('lists/the-only-list-in-the-world/', views.view_list,
         name='view_list'),
    path('lists/new/', views.new_list, name='new_list'),
]
