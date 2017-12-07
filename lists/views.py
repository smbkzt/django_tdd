from django.shortcuts import render, redirect

from .models import Items, Lists


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = Lists.objects.get(id=list_id)
    return render(request, 'list.html', {"list": list_})


def add_item(request, list_id):
    list_ = Lists.objects.get(id=list_id)
    items = Items.objects.create(
        text=request.POST.get("item_text", ""),
        list=list_
    )
    return redirect('/lists/%d/' % (list_id,))


def new_list(request):
    if request.method == "POST":
        list_ = Lists.objects.create()
        data = request.POST.get("item_text", "")
        Items.objects.create(text=data, list=list_).save()
    return redirect('/lists/%d/' % (list_.id))
