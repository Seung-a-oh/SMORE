FusionCharts.ready(function(){
    var chartObj = new FusionCharts({
type: 'pie2d',
renderAt: 'chart-container',
width: '550',
height: '350',
dataFormat: 'json',
dataSource: {
"chart": {
    "caption": "구매자 평균 남녀성비",
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