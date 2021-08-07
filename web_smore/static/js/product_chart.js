FusionCharts.ready(function(){
    var chartObj = new FusionCharts({
type: 'pie2d',
renderAt: 'chart-container',
width: '300',
height: '300',
dataFormat: 'json',
dataSource: {
"chart": {
    "caption": "구매자 남녀성비",
    "subCaption": "2021.08",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    //Theme
    "theme": "fusion"
},
"data": [{
    "label": "여자",
    "value": "60"
}, {
    "label": "남자",
    "value": "40"
}]
}
}
);
    chartObj.render();
});

FusionCharts.ready(function(){
    var chartObj = new FusionCharts({
type: 'pie2d',
renderAt: 'chart-container_01',
width: '300',
height: '300',
dataFormat: 'json',
dataSource: {
"chart": {
    "caption": "구매자 연령대",
    "subCaption": "2021.08",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    //Theme
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
}
}
);
    chartObj.render();
});