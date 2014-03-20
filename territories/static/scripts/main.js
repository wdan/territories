/**
 * Created by wenbin on 12/3/14.
 */

var dataManager = new LG.data.DataManager();
var sandBox = new LG.control.SandBox();
//var visList = [];
//var width = Math.floor($(window).width()*0.8);
var height = 600;
var width = 860;
var overview_svg;
var detail_svg;
var gui;
var detail;
var merge_number;
var orig_cluster_number;

$('#dataTypeList').change(function(){
    var val = $('#dataTypeList').val();
    if(val!='null'){

        merge_number = 1;
        if(gui!=undefined)gui.destroy();
        gui = new dat.GUI();

        if(overview_svg!=undefined){
            d3.select('#paint_zone').select('svg').data([]).exit().remove();
        }
        overview_svg = d3.select('#paint_zone').append('svg')
            .attr('width', width)
            .attr('height', height);
        dataManager.getPolygon(val, width, height, 1);
        dataManager.getConstraints();
        orig_cluster_number = dataManager.polygon.length;
        console.log('orig:'+orig_cluster_number);
        dataManager.getDetailed();
//        dataManager.getOriginal();
        dataManager.getClusterAttr();

//        var hull = new LG.visual.ConvexHull(gui, svg, dataManager, 'convex_hull');
//        hull.display();
//
//        var boundary_contour = new LG.visual.BoundaryContour(gui, svg, dataManager, 'boundary_contour');
//        boundary_contour.display();

        var voronoi = new LG.visual.Voronoi(gui, overview_svg, dataManager, sandBox, 'voronoi');
        sandBox.add('voronoi', voronoi);

//        var river_node = new LG.visual.RiverNode(gui, overview_svg, dataManager, sandBox, 'river_node');
//        sandBox.add('river_node', river_node);
//
//        if(detail_svg!=undefined){
//            d3.select('#detailed_view').select('svg').data([]).exit().remove();
//        }
//        detail_svg = d3.select('#detailed_view').append('svg')
//            .attr('width', 250)
//            .attr('height', 600);
//        detail = new LG.visual.DetailedView(gui, detail_svg, dataManager, sandBox, 'detailed_view');
//        sandBox.add('detailed_view', detail);

        voronoi.display();
//        river_node.display();


//        var boundary_node = new LG.visual.BoundaryNode(gui, svg, dataManager, 'boundary_node');
//        boundary_node.display();
//
//        var boundary_edge = new LG.visual.BoundaryEdge(gui, svg, dataManager, 'boundary_edge');
//        boundary_edge.display();
//
//        var inside_node = new LG.visual.InsideNode(gui, svg, dataManager, 'inside_node');
//        inside_node.display();
//
//        var node_label = new LG.visual.NodeLabel(gui, svg, dataManager, 'node_label');
//        node_label.display();

    }
});

//$('#update_cluster').click(function(){
//    if(sandBox.exchangeCluster.length==2){
//        dataManager.getNewPosition(sandBox.exchangeCluster);
//        dataManager.getConstraints();
////        sandBox.update_data_All();
//            voronoi.update_data(dataManager.polygon);
//        sandBox.clearClusterQueue();
//    }else{
//        console.log('[WARNING] Please select two groups.');
//    }
//});

//$('#show_cluster').click(function(){
//    if(sandBox.exchangeCluster.length==2){
//        sandBox.addDetail();
//        sandBox.clearClusterQueue();
//    }else{
//        console.log('[WARNING] Please select two groups.');
//    }
//});

$('#merge_cluster').click(function(){
    var merge = sandBox.getMergeQueue();
    if(merge.length>=2){
        dataManager.sendMergeRequest(merge, merge_number);
        sandBox.merge_data('voronoi', dataManager.merge_info, merge, orig_cluster_number + merge_number - 1);
        merge_number += 1;
    }else{
        console.log('[WARNING] Please select more than two groups.');
    }
});
