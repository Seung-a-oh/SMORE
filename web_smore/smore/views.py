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
    dataSource2 = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "[2021] 기업 매출 현황"
    chartConfig["subCaption"] = "2021년도 매출"
    chartConfig["xAxisName"] = "월별"
    chartConfig["yAxisName"] = "상품 판매 개수"
    chartConfig["numberSuffix"] = "개"
    chartConfig["theme"] = "fusion"
    chartConfig2 = OrderedDict()
    chartConfig2["caption"] = "[2020] 기업 매출 현황"
    chartConfig2["subCaption"] = "2020년도 매출"
    chartConfig2["xAxisName"] = "월별"
    chartConfig2["yAxisName"] = "상품 판매 개수"
    chartConfig2["numberSuffix"] = "개"
    chartConfig2["theme"] = "fusion"

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

    chartData2 = OrderedDict()
    chartData2["1월"] = 150
    chartData2["2월"] = 149
    chartData2["3월"] = 155
    chartData2["4월"] = 89
    chartData2["5월"] = 147
    chartData2["6월"] = 192
    chartData2["7월"] = 184
    chartData2["8월"] = 92
    chartData2["9월"] = 115
    chartData2["10월"] = 123
    chartData2["11월"] = 148
    chartData2["12월"] = 129

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    dataSource2["chart"] = chartConfig2
    dataSource2["data"] = []

    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)

    for key, value in chartData2.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource2["data"].append(data)



    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1" , "650", "350", "chart-1", "json", dataSource)
    column2D2 = FusionCharts("column2d", "ex2" , "650", "350", "chart-3", "json", dataSource2)

    chartObj = FusionCharts( 'bar2d', 'ex3', '700', '350', 'chart-4', 'json', """{
  "chart": {
    "caption": "상품 판매 순위",
    "yaxisname": "판매 개수",
    "aligncaptionwithcanvas": "0",
    "plottooltext": "<b>$label</b> 은 <b>$dataValue</b> 개 판매됨",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "Travel",
      "value": "41"
    },
    {
      "label": "Adver",
      "value": "39"
    },
    {
      "label": "Other",
      "value": "38"
    },
    {
      "label": "Real",
      "value": "32"
    },
    {
      "label": "Communic",
      "value": "26"
    },
    {
      "label": "Consn",
      "value": "25"
    },
    {
      "label": "Enteent",
      "value": "25"
    },
    {
      "label": "Stam",
      "value": "24"
    },
    {
      "label": "Tra",
      "value": "23"
    },
    {
      "label": "Utes",
      "value": "22"
    },
    {
      "label": "Aee",
      "value": "18"
    },
    {
      "label": "Bng",
      "value": "16"
    },
    {
      "label": "fssssssssss",
      "value": "15"
    }
  ]
}""")
    chartObj2 = FusionCharts( 'doughnut2d', 'ex5', '650', '350', 'chart-5', 'json', """{
  "chart": {
    "caption": "구매자 연령대",
    "subcaption": "2021년 구매자 통계",
    "showpercentvalues": "1",
    "defaultcenterlabel": "연령대 통계  ",
    "aligncaptionwithcanvas": "0",
    "captionpadding": "0",
    "decimals": "1",
    "plottooltext": "사용자의 <b>$percentValue</b>는 <b>$label</b>입니다",
    "centerlabel": "<b>$label</b>: $value",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "20대 여자",
      "value": "10000"
    },
    {
      "label": "20대 남자",
      "value": "5300"
    },
    {
      "label": "30대 여자",
      "value": "10500"
    },
    {
      "label": "30대 남자",
      "value": "18900"
    },
    {
      "label": "그 외",
      "value": "4000"
    }
  ]
}""")
    chartObj3 = FusionCharts( 'doughnut2d', 'ex6', '650', '350', 'chart-6', 'json', """{
  "chart": {
    "caption": "구매자 성별",
    "subcaption": "2021년 구매자 통계",
    "showpercentvalues": "1",
    "defaultcenterlabel": "성별",
    "aligncaptionwithcanvas": "0",
    "captionpadding": "0",
    "decimals": "1",
    "plottooltext": " 사용자의 <b>$percentValue</b>는 <b>$label</b>입니다.",
    "centerlabel": "<b>$label</b>: $value",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "남성",
      "value": "2100"
    },
    {
      "label": "여성",
      "value": "3200"
    }
  ]
}""")
    chartObj4 = FusionCharts( 'line', 'ex7', '700', '350', 'chart-7', 'json', """{
  "chart": {
    "caption": "구독자 수",
    "yaxisname": "명",
    "subcaption": "[2016-2021]",
    "numbersuffix": " 명",
    "rotatelabels": "1",
    "setadaptiveymin": "1",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "2016",
      "value": "89"
    },
    {
      "label": "2017",
      "value": "1452"
    },
    {
      "label": "2018",
      "value": "6740"
    },
    {
      "label": "2019",
      "value": "20453"
    },
    {
      "label": "2020",
      "value": "64201"
    },
    {
      "label": "2021",
      "value": "80132"
    }
  ]
}""")
    return  render(request, 'com_chart.html', {'output' : column2D.render(), 'output2':column2D2.render(), 'output3': chartObj.render(), 'output4': chartObj2.render(),'output5': chartObj3.render(),'output6': chartObj4.render(),'chartTitle': '기업 매출 그래프', 'chartTitle2': '기업 매출 그래프2'})

def product_chart(request):
  # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
   dataSource = OrderedDict() 
   # The `chartConfig` dict contains key-value pairs data for chart attribute
   chartConfig = OrderedDict()
   chartConfig["caption"] = "월별 매출 현황"
   chartConfig["subCaption"] = ""
   chartConfig["xAxisName"] = "month"
   chartConfig["yAxisName"] = "상품 매출(만원)"
   chartConfig["numberSuffix"] = ""
   chartConfig["theme"] = "fusion"  
   # The `chartData` dict contains key-value pairs data
   chartData = OrderedDict()
   chartData["Jan"] = 290
   chartData["Feb"] = 260
   chartData["Mar"] = 180
   chartData["Apr"] = 140
   chartData["May"] = 115
   chartData["Jun"] = 100
   chartData["Jul"] = 30
   chartData["Aug"] = 30
   chartData["Sep"] = 30
   chartData["Oct"] = 300
   chartData["Nov"] = 450
   chartData["Dec"] = 30  
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

   column2D = FusionCharts("column2d", "ex1" , "610", "350", "chart-1", "json", dataSource) 
   return  render(request, 'product_chart.html', {'output' : column2D.render(), 'chartTitle': ''}) 
   
def main_chart(request):
  dataSource = OrderedDict()

  chartConfig = OrderedDict()
  chartConfig["caption"] = "[2021] 기업 매출 현황"
  chartConfig["subCaption"] = "2021년도 매출"
  chartConfig["xAxisName"] = "월별"
  chartConfig["yAxisName"] = "상품 판매 개수"
  chartConfig["numberSuffix"] = "개"
  chartConfig["theme"] = "fusion"

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

  for key, value in chartData.items():
      data = {}
      data["label"] = key
      data["value"] = value
      dataSource["data"].append(data)
  column2D = FusionCharts("column2d", "ex1" , "600", "400", "chart-1", "json", dataSource)
  chartObj = FusionCharts( 'line', 'ex2', '600', '400', 'chart-2', 'json', """{
  "chart": {
    "caption": "최근 10년간 매출 추이",
    "yaxisname": "만원",
    "subcaption": "[2011-2021]",
    "numbersuffix": " 만원",
    "rotatelabels": "1",
    "setadaptiveymin": "1",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "2011",
      "value": "12229"
    },
    {
      "label": "2012",
      "value": "8249"
    },
    {
      "label": "2013",
      "value": "9245"
    },
    {
      "label": "2014",
      "value": "15584"
    },
    {
      "label": "2015",
      "value": "18529"
    },
    {
      "label": "2016",
      "value": "14289"
    },
    {
      "label": "2017",
      "value": "19562"
    },
    {
      "label": "2018",
      "value": "16240"
    },
    {
      "label": "2019",
      "value": "24153"
    },
    {
      "label": "2020",
      "value": "24091"
    },
    {
      "label": "2021",
      "value": "31032"
    }
  ]
}""")
  chartObj2 = FusionCharts( 'doughnut2d', 'ex3', '600', '400', 'chart-3', 'json', """{
    "chart": {
      "caption": "구매율이 높은 해시태그",
      "subcaption": "2021년 구매율",
      "showpercentvalues": "1",
      "defaultcenterlabel": "구매자 통계",
      "aligncaptionwithcanvas": "0",
      "captionpadding": "0",
      "decimals": "1",
      "plottooltext": "판매된 상품의 <b>$percentValue</b>는 <b>$label</b>입니다",
      "centerlabel": "<b>$label</b>: $value",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "#재활용",
        "value": "10000"
      },
      {
        "label": "#리사이클링",
        "value": "5300"
      },
      {
        "label": "#친환경",
        "value": "10500"
      },
      {
        "label": "#재활용기",
        "value": "8900"
      },
      {
        "label": "그 외",
        "value": "4000"
      }
    ]
  }""")
  chartObj3 = FusionCharts( 'bar2d', 'ex4', '600', '400', 'chart-4', 'json', """{
    "chart": {
      "caption": "우리 회사 별점",
      "yaxisname": "평가한 사용자 수",
      "aligncaptionwithcanvas": "0",
      "plottooltext": "<b>$dataValue</b>명은 우리 회사를 <b>$label</b>점으로 평가함",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "5",
        "value": "4311"
      },
      {
        "label": "4",
        "value": "3149"
      },
      {
        "label": "3",
        "value": "138"
      },
      {
        "label": "2",
        "value": "32"
      },
      {
        "label": "1",
        "value": "6"
      }
    ]
  }""")
  return render(request, 'main_chart.html', {'output' : column2D.render(), 'output2': chartObj.render(), 'output3': chartObj2.render(),'output4': chartObj3.render()})

def research_chart(request):
    chartObj = FusionCharts( 'bar2d', 'ex1', '700', '350', 'chart-1', 'json', """{
    "chart": {
      "caption": "우리 기업을 구독한 이유",
      "yaxisname": "응답 비율",
      "aligncaptionwithcanvas": "0",
      "plottooltext": "<b>$dataValue</b> %",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "제품을 사용해본 경험이 있어서",
        "value": (31/100)*100
      },
      {
        "label": "가치관에 맞는 스타트업이라서",
        "value": "12"
      },
      {
        "label": "디자인이 마음에 들어서",
        "value": "41"
      },
      {
        "label": "SNS 홍보를 통해서",
        "value": "31"
      },
      {
        "label": "그 외",
        "value": "31"
      }
    ]
  }""")
    chartObj2 = FusionCharts( 'bar2d', 'ex2', '700', '350', 'chart-2', 'json', """{
    "chart": {
      "caption": "우리 기업의 강점",
      "yaxisname": "응답 비율",
      "aligncaptionwithcanvas": "0",
      "plottooltext": "<b>$dataValue</b> %",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "기업의 가치관(친환경)",
        "value": (31/100)*100
      },
      {
        "label": "제품 디자인",
        "value": "12"
      },
      {
        "label": "제품 품질",
        "value": "41"
      },
      {
        "label": "홍보 방식",
        "value": "31"
      },
      {
        "label": "그 외",
        "value": "31"
      }
    ]
  }""")
    return render(request, 'research_chart.html',{'output' : chartObj.render(),'output2' : chartObj2.render()})

