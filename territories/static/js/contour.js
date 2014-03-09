/**
 * Created by wenbin on 9/3/14.
 */


//var data = [{x:100, y:200}, {x:300, y:200}];





function draw_contour(nodes, polygons){


    var scale = 50;
    var pix = 10;

    data = {};
    cluster_list = [];

    for(var i=0;i<polygons.length;i++){
        var p = polygons[i];
        data[p.cluster] = [];
        cluster_list.push(p.cluster);

    }

    for(i=0;i<nodes.length;i++){
        data[nodes[i].cluster].push({x:nodes[i].x, y:nodes[i].y});
    }

    contour = svg.append('g').attr("class", "contour");

    for(i=0;i<cluster_list.length;i++){
        var cid = cluster_list[i];
        var tmp = contour.append('g').attr("class", "contour-"+cid);
        heatmap(data[cid], tmp, width, height, pix, scale, color(cid));
    }
}