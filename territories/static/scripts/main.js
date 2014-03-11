/**
 * Created by wenbin on 12/3/14.
 */

var dataManager;
var width = window.screen.width;
var height = window.screen.height;
var svg = d3.select('#paint_zone').append('svg')
    .attr('width', width)
    .attr('height', height);
var gui = new dat.GUI();

$('#dataTypeList').change(function(){
    var val = $('#dataTypeList').val();
    if(val!='null'){
        dataManager = new LG.data.DataManager();
        dataManager.getAggregate(val, width, height);
        var voro = svg.append('g').attr('class', 'voronoi');
        var voronoi = new LG.visual.Voronoi(gui, voro, dataManager);

    }
});