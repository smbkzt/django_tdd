from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Items


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    items = Items.objects.all()
    return render(request, 'list.html', {'all_items': items})


def new_list(request):
    if request.method == "POST":
        data = request.POST.get("item_text", "")
        Items.objects.create(text=data).save()
    return redirect('/lists/the-only-list-in-the-world/')
