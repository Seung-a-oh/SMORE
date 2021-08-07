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

def com_chart(request):
    dataSource = OrderedDict()
    dataSource2 = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "[2021] 기업 매출 현황"
    chartConfig["subCaption"] = "2021년도 매출"
    chartConfig["xAxisName"] = "월별"
    chartConfig["yAxisName"] = "상품 판매액"
    chartConfig["numberSuffix"] = "만원"
    chartConfig["theme"] = "fusion"
    chartConfig["palettecolors"] = "e4dbb2"
    chartConfig2 = OrderedDict()
    chartConfig2["caption"] = "[2020] 기업 매출 현황"
    chartConfig2["subCaption"] = "2020년도 매출"
    chartConfig2["xAxisName"] = "월별"
    chartConfig2["yAxisName"] = "상품 판매액"
    chartConfig2["numberSuffix"] = "만원"
    chartConfig2["theme"] = "fusion"
    chartConfig2["palettecolors"] = "e4dbb2"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["1월"] = 1205
    chartData["2월"] = 936
    chartData["3월"] = 1249
    chartData["4월"] = 1347
    chartData["5월"] = 1572
    chartData["6월"] = 932
    chartData["7월"] = 1134
    chartData["8월"] = 1536
    chartData["9월"] = 1357
    chartData["10월"] = 898
    chartData["11월"] = 1428
    chartData["12월"] = 1333

    chartData2 = OrderedDict()
    chartData2["1월"] = 1506
    chartData2["2월"] = 1496
    chartData2["3월"] = 1557
    chartData2["4월"] = 898
    chartData2["5월"] = 1472
    chartData2["6월"] = 1921
    chartData2["7월"] = 1884
    chartData2["8월"] = 972
    chartData2["9월"] = 1175
    chartData2["10월"] = 1423
    chartData2["11월"] = 1478
    chartData2["12월"] = 1249

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
    column2D = FusionCharts("column2d", "ex1"  , "650", "340", "chart-1", "json", dataSource)
    column2D2 = FusionCharts("column2d", "ex2"  , "650", "340", "chart-3", "json", dataSource2)

    chartObj = FusionCharts( 'bar2d', 'ex3', '650', '340', 'chart-4', 'json', """{
  "chart": {
    "caption": "상품 판매 순위",
    "yaxisname": "판매 개수",
    "paletteColors": "#e4dbb2,#cfc183",
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
    "paletteColors": "#e68dcf,#6d9bdf,#ff4868,#B0D67A,#894523",
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
      "value": "10000",
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
    "paletteColors": "#e68dcf,#6d9bdf,#ff4868,#B0D67A,#894523",
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
      "label": "여성",
      "value": "2100"
    },
    {
      "label": "남성",
      "value": "3200"
    }
  ]
}""")
    chartObj4 = FusionCharts( 'line', 'ex7', '650', '350', 'chart-7', 'json', """{
  "chart": {
    "caption": "구독자 수",
    "yaxisname": "명",
    "paletteColors": "#cfc183",
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
   chartConfig["palettecolors"] = "e4dbb2"
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

   column2D = FusionCharts("column2d", "ex1"  , "610", "340", "chart-1", "json", dataSource)
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
  #  chartConfig["bgcolor"] = "263812"  
   chartConfig["palettecolors"] = "d6c98d"
   # The `chartData` dict contains key-value pairs data
   chartData = OrderedDict()
   chartData["Jan"] = 320
   chartData["Feb"] = 270
   chartData["Mar"] = 120
   chartData["Apr"] = 180
   chartData["May"] = 175
   chartData["Jun"] = 134
   chartData["Jul"] = 214
   chartData["Aug"] = 142
   chartData["Sep"] = 97
   chartData["Oct"] = 214
   chartData["Nov"] = 351
   chartData["Dec"] = 227  
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

   column2D2 = FusionCharts("column2d", "ex6"  , "610", "340", "chart-6", "json", dataSource) 
   chartObj = FusionCharts( 'pie2d', 'ex2', '300', '300', 'chart-2', 'json', """{
  "chart": {
    "caption": "구매자 남녀성비",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion",
  },
"data": [{
    "label": "여자",
    "value": "60"
}, {
    "label": "남자",
    "value": "40"
}]
}""")
   chartObj2 = FusionCharts( 'pie2d', 'ex3', '300', '300', 'chart-3', 'json', """{
  "chart": {
    "caption": "구매자 남녀성비",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion",
  },
"data": [{
    "label": "여자",
    "value": "80"
}, {
    "label": "남자",
    "value": "20"
}]
}""")
   chartObj3 = FusionCharts( 'pie2d', 'ex4', '300', '300', 'chart-4', 'json', """{
  "chart": {
    "caption": "구매자 연령대",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion"
  },
"data": [{
    "label": "10대",
    "value": "30"
}, {
    "label": "20대",
    "value": "40"
}, {
    "label": "30대",
    "value": "20"
}, {
    "label": "40대",
    "value": "7"
},{
    "label": "50대이상",
    "value": "3"
}]
}""")
   chartObj4 = FusionCharts( 'pie2d', 'ex5', '300', '300', 'chart-5', 'json', """{
  "chart": {
    "caption": "구매자 연령대",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion"
  },
"data": [{
    "label": "10대",
    "value": "20"
}, {
    "label": "20대",
    "value": "35"
}, {
    "label": "30대",
    "value": "20"
}, {
    "label": "40대",
    "value": "17"
},{
    "label": "50대이상",
    "value": "8"
}]
}""")
   return  render(request, 'product_chart.html', {'output' : column2D.render(),'output2' :  chartObj.render(),'output3' :  chartObj2.render(),'output4' :  chartObj3.render(),'output5' :  chartObj4.render(),'output6' : column2D2.render(),}) 
   
def main_chart(request):
  dataSource = OrderedDict()

  chartConfig = OrderedDict()
  chartConfig["caption"] = "[2021] 기업 매출 현황"
  chartConfig["subCaption"] = "2021년도 매출"
  chartConfig["xAxisName"] = "월별"
  chartConfig["yAxisName"] = "상품 판매액"
  chartConfig["numberSuffix"] = "만원"
  chartConfig["theme"] = "fusion"
  chartConfig["palettecolors"] = "e4dbb2"

  chartData = OrderedDict()
  chartData["1월"] = 1620
  chartData["2월"] = 980
  chartData["3월"] = 1239
  chartData["4월"] = 1634
  chartData["5월"] = 1957
  chartData["6월"] = 932
  chartData["7월"] = 1153
  chartData["8월"] = 1573
  chartData["9월"] = 0
  chartData["10월"] = 0
  chartData["11월"] = 0
  chartData["12월"] = 0
  dataSource["chart"] = chartConfig
  dataSource["data"] = []

  for key, value in chartData.items():
      data = {}
      data["label"] = key
      data["value"] = value
      dataSource["data"].append(data)
  column2D = FusionCharts("column2d", "ex1" , "650", "340", "chart-1", "json", dataSource)
  chartObj = FusionCharts( 'line', 'ex2', '650', '340', 'chart-2', 'json', """{
  "chart": {
    "caption": "최근 10일간 매출 추이",
    "yaxisname": "만원",
    "subcaption": "07.27 ~ 08.06",
    "numbersuffix": " 만원",
    "paletteColors": "#cfc183,#cca356",
    "rotatelabels": "1",
    "setadaptiveymin": "1",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "07.27",
      "value": "12229"
    },
    {
      "label": "07.28",
      "value": "8249"
    },
    {
      "label": "07.29",
      "value": "9245"
    },
    {
      "label": "07.30",
      "value": "15584"
    },
    {
      "label": "07.31",
      "value": "18529"
    },
    {
      "label": "08.01",
      "value": "14289"
    },
    {
      "label": "08.02",
      "value": "19562"
    },
    {
      "label": "08.03",
      "value": "16240"
    },
    {
      "label": "08.04",
      "value": "24153"
    },
    {
      "label": "08.05",
      "value": "24091"
    },
    {
      "label": "08.06",
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
  
  chartObj3 = FusionCharts( 'msline', 'ex4', '650', '340', 'chart-4', 'json', """{
  "chart": {
    "caption": "구독자 증가 수 및 방문자 수",
    "yaxisname": "명",
    "subcaption": "08.01 ~ 08.06",
    "showhovereffect": "1",
    "numbersuffix": "명",
    "paletteColors": "#cfc183,#cca356",
    "drawcrossline": "1",
    "plottooltext": "$seriesName : <b>$dataValue</b>",
    "theme": "fusion"
  },
  "categories": [
    {
      "category": [
        {
          "label": "08.01"
        },
        {
          "label": "08.02"
        },
        {
          "label": "08.03"
        },
        {
          "label": "08.04"
        },
        {
          "label": "08.05"
        },
        {
          "label": "08.06"
        }
      ]
    }
  ],
  "dataset": [
    {
      "seriesname": "구독자 증가 수",
      "data": [
        {
          "value": "12"
        },
        {
          "value": "24"
        },
        {
          "value": "16"
        },
        {
          "value": "14"
        },
        {
          "value": "20"
        },
        {
          "value": "17"
        }
      ]
    },
    {
      "seriesname": "방문자 수",
      "data": [
        {
          "value": "160"
        },
        {
          "value": "128"
        },
        {
          "value": "134"
        },
        {
          "value": "142"
        },
        {
          "value": "154"
        },
        {
          "value": "111"
        }
      ]
    }
  ]
}""")
  return render(request, 'main_chart.html', {'output' : column2D.render(), 'output2': chartObj.render(), 'output3': chartObj2.render(),'output4': chartObj3.render()})

def research_chart(request):
    chartObj = FusionCharts( 'bar2d', 'ex1','610', '340', 'chart-1', 'json', """{
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
    chartObj2 = FusionCharts( 'bar2d', 'ex2', '610', '340', 'chart-2', 'json', """{
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
    chartObj3 = FusionCharts( 'bar2d', 'ex3',  '610', '340', 'chart-3', 'json', """{
    "chart": {
      "caption": "우리 기업의 보완점",
      "yaxisname": "응답 비율",
      "aligncaptionwithcanvas": "0",
      "plottooltext": "<b>$dataValue</b> %",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "해당 기업만의 뚜렷한 가치관이 없음",
        "value": (31/100)*100
      },
      {
        "label": "가격이 비싼 편임",
        "value": "12"
      },
      {
        "label": "소비자와의 소통이 부족함",
        "value": "41"
      },
      {
        "label": "홍보 수단이 부족함",
        "value": "31"
      },
      {
        "label": "그 외",
        "value": "31"
      }
    ]
  }""")
    chartObj4 = FusionCharts( 'doughnut2d', 'ex4', '600', '400', 'chart-4', 'json', """{
    "chart": {
      "caption": "3개의 제품 중 대표 제품",
      "subcaption": "중복 선택",
      "showpercentvalues": "1",
      "defaultcenterlabel": "구매자 통계",
      "aligncaptionwithcanvas": "0",
      "captionpadding": "0",
      "decimals": "1",
      "plottooltext": "고객의 <b>$percentValue</b>는 대표 상품을 <b>$label</b> 이라고 생각합니다.",
      "centerlabel": "<b>$label</b>: $value",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "1번 상품",
        "value": "10400"
      },
      {
        "label": "2번 상품",
        "value": "5300"
      },
      {
        "label": "3번 상품",
        "value": "10500"
      }
    ]
  }""")
    chartObj5 = FusionCharts( 'doughnut2d', 'ex5', '600', '400', 'chart-5', 'json', """{
    "chart": {
      "caption": "우리 기업을 설명할 수 있는 해시태그",
      "subcaption": "중복 선택",
      "showpercentvalues": "1",
      "defaultcenterlabel": "구매자 통계",
      "aligncaptionwithcanvas": "0",
      "captionpadding": "0",
      "decimals": "1",
      "plottooltext": "고객의 <b>$percentValue</b>는 대표 해시태그를 <b>$label</b> 이라고 생각합니다.",
      "centerlabel": "<b>$label</b>: $value",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "#친환경적인",
        "value": "10400"
      },
      {
        "label": "#혁신적인",
        "value": "5300"
      },
      {
        "label": "#깔끔한_디자인",
        "value": "10500"
      },
      {
        "label": "#감각적인",
        "value": "10500"
      },
      {
        "label": "#저렴한_가격",
        "value": "10500"
      },
      {
        "label": "#비건_제품",
        "value": "10500"
      }
    ]
  }""")
    return render(request, 'research_chart.html',{'output' : chartObj.render(),'output2' : chartObj2.render(),'output3' : chartObj3.render(),'output4' : chartObj4.render(),'output5' : chartObj5.render()})