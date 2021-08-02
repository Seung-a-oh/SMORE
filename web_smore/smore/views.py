from django.shortcuts import render, redirect, get_object_or_404
from account.models import User
from django.utils import timezone
from smore.models import Item, ItemImage
from smore.models import ExperRec
from collections import OrderedDict
from .fusioncharts import FusionCharts
from django.http import HttpResponse
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

def com_chart(request):
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "[2021] 기업 매출 현황"
    chartConfig["subCaption"] = "2021년도 매출"
    chartConfig["xAxisName"] = "월별"
    chartConfig["yAxisName"] = "상품 판매 개수"
    chartConfig["numberSuffix"] = "개"
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["1월"] = 120
    chartData["2월"] = 90
    chartData["3월"] = 129
    chartData["4월"] = 134
    chartData["5월"] = 157
    chartData["6월"] = 93
    chartData["7월"] = 113
    chartData["8월"] = 153
    chartData["9월"] = 135
    chartData["10월"] = 89
    chartData["11월"] = 142
    chartData["12월"] = 133


    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1" , "600", "400", "chart-1", "json", dataSource)

    return  render(request, 'com_chart.html', {'output' : column2D.render(), 'chartTitle': '기업 매출 그래프'})