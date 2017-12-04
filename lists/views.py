from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Items


def home_page(request):
    if request.POST.get("item_text", "") != "":
        new_item = request.POST.get("item_text", "")
        Items.objects.create(text=new_item)
        return redirect('/')

    context = {
        "all_items": Items.objects.all(),
    }
    return render(request, 'home.html', context)
