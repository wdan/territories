var width = 1200;
var height = 1200;
var color = d3.scale.category10();

var svg = d3.select('#paint_zone')
            .append('svg')
            .attr('width', width * 2)
            .attr('height', height * 2);

set_mouse_event_handler();
//draw_force_directed_graph();
draw_voronoi();
function draw_river_nodes(data) {
    var link, node;
    var edges = data.links;
    var nodes = data.nodes;
    console.log(nodes);
    reduced_nodes = [];
    reduced_edges = [];
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i]['visible'] == 1)
        reduced_nodes.push(nodes[i]);
    }
    console.log(reduced_nodes);
    for (var i = 0; i < edges.length; i++) {
        if (edges[i]['visible'] == 1)
        reduced_edges.push(edges[i]);
    }
    node = svg.selectAll('.river-node')
            .data(reduced_nodes)
            .enter().append('circle')
            .attr('class', 'river-node')
            .style('opacity', 0.5)
            .attr('cx', function(d) {
                return d.x;
            })
            .attr('cy', function(d) {
                return d.y;
            })
            .attr('r', function(d) {
                return 5 + 3 * d['out_degree'];
                //return 5;
            })
            //.style('stroke', 'black')
            //.style('stroke-width', 2)
            //.style('stroke-opacity', function(d) {
                //if (d.out_degree > 0) {
                    //return 1;
                //}else {
                    //return 0;
                //}
            //})
            .attr('filter', 'url(#ball-glow)')
            .style('fill', function(d) {
                //return color(d.id);
                return color(d.cluster);
            });
            //}).call(force.drag);

    link = svg.selectAll('.river-link')
            .data(reduced_edges)
            .enter().append('line')
            .attr('class', function(d) {
                return 'river-link';
            })
            .attr('x1', function(d) { return nodes[d.source].x;})
            .attr('y1', function(d) { return nodes[d.source].y; })
            .attr('x2', function(d) { return nodes[d.target].x; })
            .attr('y2', function(d) { return nodes[d.target].y; })
            .style('stroke', '#222222')
            .style('opacity', 0.1)
            .style('stroke-width', function(d) {
                return Math.sqrt(d.weight);
            });
}
