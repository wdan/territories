var width = 960;
var height = 720;
var color = d3.scale.category10();

var svg = d3.select('#paint_zone')
            .append('svg')
            .attr('width', width * 2)
            .attr('height', height * 2);

set_mouse_event_handler();
//draw_force_directed_graph();
draw_voronoi();
//draw_cluster()
function draw_cluster() {
    $.ajax({
        dataType: 'json',
        url: '/_get_graph_data',
        async: false,
        success: function(data) {
            var link, node;
            var edges = data.links;
            var nodes = data.nodes;

            node = svg.selectAll('.node')
                    .data(nodes)
                    .enter().append('circle')
                    .attr('class', 'node')
                    .style('opacity', 0.5)
                    .attr('cx', function(d) {
                        return d.x;
                    })
                    .attr('cy', function(d) {
                        return d.y;
                    })
                    .attr('r', function(d) {
                        //return 5;
                        if (d.size < 5)
                            return 5;
                        else
                            return d.size;
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
                    .style('fill', function(d) {
                        //return color(d.id);
                        return color(d.cluster);
                    });
                    //}).call(force.drag);

            link = svg.selectAll('.link')
                    .data(edges)
                    .enter().append('line')
                    .attr('class', function(d) {
                        return 'link';
                    })
                    .attr('x1', function(d) { return nodes[d.source].x;})
                    .attr('y1', function(d) { return nodes[d.source].y; })
                    .attr('x2', function(d) { return nodes[d.target].x; })
                    .attr('y2', function(d) { return nodes[d.target].y; })
                    .style('stroke', '#222222')
                    .style('opacity', 0.1)
                    .style('stroke-width', function(d) {
                        return Math.sqrt(d.weight);
                        //return 1;
                    });
        }
    });
}
