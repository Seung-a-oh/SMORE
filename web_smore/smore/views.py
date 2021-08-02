from django.shortcuts import render, redirect, get_object_or_404
from account.models import User
from django.utils import timezone
from smore.models import Item, ItemImage
from smore.models import ExperRec
from .models import *


# Create your views here.
def home(request):
    items = Item.objects.all()
    itemImage = ItemImage.objects.all().first()
    return render(request, 'home.html',{'items':items, 'image':itemImage})

def create(request):
    if request.method == "POST" :
        new_item = Item()
        new_item.item_name = request.POST['item_name']
        new_item.body = request.POST['body']
        new_item.pub_date = timezone.datetime.now()

        user_id = request.user.id

        user = User.objects.get(id = user_id)

        new_item.author = user

        new_item.save()
        for img in request.FILES.getlist('image'):
            image = ItemImage()
            image.itemFK = new_item
            image.image = img
            image.save()
        return redirect('home')

    else :
        return render(request,'new.html')

def detail(request, id):
    item = get_object_or_404(Item, pk = id)
    itemImage = ItemImage.objects.all().filter(itemFK = id)
    return render(request, 'detail.html', {'item':item, 'image':itemImage})

def edit(request, id):
    if request.method == "POST":
        edit_item = Item.objects.get(id = id)
        edit_item.item_name = request.POST["item_name"]
        edit_item.body = request.POST["body"]
        edit_item.save()
        delete_img = ItemImage.objects.all().filter(itemFK = id)
        delete_img.delete()
        for img in request.FILES.getlist('image'):
            image = ItemImage()
            image.itemFK = edit_item
            image.image = img
            image.save()
        
        return redirect('detail', edit_item.id)
    else:
        item = Item.objects.get(id = id)
        return render(request, 'edit.html', {'item': item})

def delete(request, id):
    delete_item = Item.objects.get(id = id)
    delete_item.delete()
    return redirect('home')

def experience(request):
    expers = ExperRec.objects.all()
    return render(request, 'experience.html',{'expers':expers})

def exper_create(request):
    if request.method == "POST" :
        new_exper = ExperRec()
        new_exper.exper_title = request.POST['exper_title']
        new_exper.exper_body = request.POST['exper_body']
        new_exper.exper_period = request.POST['exper_period']
        new_exper.exper_pub_date = timezone.datetime.now()
        new_exper.exper_image=request.FILES['exper_image']

        user_id = request.user.id

        user = User.objects.get(id = user_id)

        new_exper.exper_author = user

        new_exper.save()
        return redirect('experience')

    else :
        return render(request,'exper_create.html')
        
def exper_detail(request, id):
    exper = get_object_or_404(ExperRec, pk = id)
    return render(request, 'exper_detail.html', {'exper':exper})

def exper_edit(request, id):
    if request.method == "POST":
        edit_exper = ExperRec.objects.get(id = id)
        edit_exper.exper_title = request.POST["exper_title"]
        edit_exper.exper_body = request.POST["exper_body"]
        edit_exper.exper_image=request.FILES['exper_image']

        edit_exper.save()
        return redirect('detail', edit_exper.id)
    else:
        exper = ExperRec.objects.get(id = id)
        return render(request, 'exper_edit.html', {'exper': exper})

def exper_delete(request, id):
    delete_exper = ExperRec.objects.get(id = id)
    delete_exper.delete()
    return redirect('experience')

def dashboard(request):
    return render(request, 'dashboard.html')
