/**
 * Created by wenbin on 22/2/14.
 */

    // data
function draw_voronoi() {
    $.ajax({
        dataType: 'json',
        url: '/_get_voronoi_data_r',
        async: false,
        success: function(data) {
            var nodes = data['cluster']['nodes'];
            var edges = data['cluster']['links'];
            var polygons = data['voronoi'];
//            console.log(polygons);


            var ori_node = data['original'].nodes;
            var  reduced_nodes = [];
            for (var i = 0; i < ori_node.length; i++) {
                if (ori_node[i]['visible'] == 1)
                    reduced_nodes.push(ori_node[i]);
            }

//            draw_hulls(reduced_nodes, polygons);
            draw_contour(reduced_nodes, polygons);

            cluster_dict = {};
            var xlist = [];
            var ylist = [];
            var node = [];
            var vono = [];
            for (var i = 0; i < polygons.length; i++) {
                xlist.push(polygons[i]['mid_x']);
                ylist.push(polygons[i]['mid_y']);
                node.push({'x': polygons[i]['mid_x'], 'y': polygons[i]['mid_y']});
                cluster_id = polygons[i]['cluster'];
                cluster_dict[cluster_id] = {'x': polygons[i]['mid_x'], 'y': polygons[i]['mid_y']};
                vono[i] = polygons[i]['points'];
                for (var j = 0; j < vono[i].length; j++) {
                    xlist.push(vono[i][j]['x']);
                    ylist.push(vono[i][j]['y']);
                }
            }

            // x, y axis scale
            //var xscale =  d3.scale.linear().domain([Math.min.apply(Math, xlist), Math.max.apply(Math, xlist)]).range([0, width]);
            //var yscale = d3.scale.linear().domain([Math.min.apply(Math, ylist), Math.max.apply(Math, ylist)]).range([0, height]);

            // draw path
            svg.selectAll('path .vono')
                .data(vono)
                .enter()
                .append('path')
                .attr("class", "vono")
                .attr('d', function(d, i) {

                    //var scale = 50;
                    //var tmp = interp(node[i], d[0], scale);
                    var s = 'M ' + d[0]['x'] + ' ' + d[0]['y'];

                    for (var j = 1; j < d.length; j++) {
                        s += ' L ' + d[j]['x'] + ' ' + d[j]['y'];
                    }
                    s += 'Z';
                    return s;

                })
                .style('fill', function(d, i) {
                    return color(polygons[i]['cluster']);
                })
                .style('opacity', function(d) {
                    return 0.3 + Math.random() * 0.5;
                })
                .attr('stroke', function(d, i){
                    return color(polygons[i]['cluster']);
                })
                .attr('stroke-width', '3px')
                .attr('stroke-opacity', 1);

            //link = svg.selectAll('.link')
                    //.data(edges)
                    //.enter().append('line')
                    //.attr('class', function(d) {
                        //return 'link';
                    //})
                    //.attr('x1', function(d) { return cluster_dict[nodes[d.source]["id"]].x; })
                    //.attr('y1', function(d) { return cluster_dict[nodes[d.source]["id"]].y; })
                    //.attr('x2', function(d) { return cluster_dict[nodes[d.target]["id"]].x; })
                    //.attr('y2', function(d) { return cluster_dict[nodes[d.target]["id"]].y; })
                    //.style('stroke', '#222222')
                    //.style('opacity', 0.1)
                    //.style('stroke-width', function(d) {
                        //return Math.sqrt(d.weight);
                    //});

            // draw nodes
            svg.selectAll('circle')
                .data(node)
                .enter()
                .append('circle')
                .attr('r', 5)
                .attr('cx', function(d) {return d.x;})
                .attr('cy', function(d) {return d.y;})
                .attr('fill', '#fff')
                .attr('opacity', 0.8);

            draw_river_nodes(data['original']);
        }
    });
}

//// helper function, just ignore
//function vectorNorm(from, to) {
//    var v = {
//        x: to.x - from.x,
//        y: to.y - from.y
//    };
//    v.length = Math.sqrt(v.x * v.x + v.y * v.y);
//    v.x = v.x / v.length;
//    v.y = v.y / v.length;
//    return v;
//}
//
////                            <--scale-->
//// center --------------------X---------> point,
//// compute X coordinates
//function interp(center, point, scale) {
//    var v = vectorNorm(center, point);
//    var k = (v.length - scale) / v.length;
//    return{
//        x: (k * v.length * v.x + center.x),
//        y: (k * v.length * v.y + center.y)
//    };
//}


