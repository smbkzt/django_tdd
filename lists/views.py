from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Items, Lists


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = Lists.objects.get(id=list_id)
    if request.POST:
        item = Items.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/%d/' % (list_.id))
    return render(request, 'list.html', {"list": list_})


def new_list(request):
    list_ = Lists.objects.create()
    data = request.POST.get("item_text", "")
    item = Items(text=data, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list!"
        return render(request, 'home.html', {'error': error})
    return redirect('/lists/%d/' % (list_.id))
