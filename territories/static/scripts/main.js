/**
 * Created by wenbin on 12/3/14.
 */

var dataManager = new LG.data.DataManager();
//var visList = [];
//var width = Math.floor($(window).width()*0.8);
var height = Math.floor($(window).height()*0.8);
var width = 940;
var svg;
var gui;

$('#dataTypeList').change(function(){
    var val = $('#dataTypeList').val();
    if(val!='null'){

        if(gui!=undefined)gui.destroy();
        gui = new dat.GUI();

        if(svg!=undefined){
            d3.select('#paint_zone').select('svg').data([]).exit().remove();
        }
        svg = d3.select('#paint_zone').append('svg')
            .attr('width', width)
            .attr('height', height);
        dataManager.getPolygon(val, width, height, 80, 1.0);
        dataManager.getOriginal();

        var hull = new LG.visual.ConvexHull(gui, svg, dataManager, 'convex_hull');
        hull.display();

        //var boundary_contour = new LG.visual.BoundaryContour(gui, svg, dataManager, 'boundary_contour');
        //boundary_contour.display();

        var voronoi = new LG.visual.Voronoi(gui, svg, dataManager, 'voronoi');
        voronoi.display();

        var boundary_node = new LG.visual.BoundaryNode(gui, svg, dataManager, 'boundary_node');
        boundary_node.display();

        var boundary_edge = new LG.visual.BoundaryEdge(gui, svg, dataManager, 'boundary_edge');
        boundary_edge.display();

        var inside_node = new LG.visual.InsideNode(gui, svg, dataManager, 'inside_node');
        inside_node.display();

    }
});
