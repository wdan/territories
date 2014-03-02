function set_attribute(nodes, edges) {
    svg.selectAll('.axis')
       .remove();
    svg.selectAll('.link')
       .transition().duration(1000)
       .style('visibility', 'visible')
       .attr('class', function(d, i)  {
           var temp_edge_highlight = 'common link';
           if (edges[i].highlight == 1) {
               temp_edge_highlight = 'highlight link';
           }
           return temp_edge_highlight;
       });
    svg.selectAll('.node')
       .transition().duration(1000)
       .style('fill', function(d, i) {
           var temp_node_color = color(d.group);
           if (nodes[i].highlight == 3) {
               temp_node_color = '#d62728';
           }else if (nodes[i].highlight == 2) {
               temp_node_color = '#f7b6d2';
           }else if (nodes[i].highlight == 1) {
               temp_node_color = '#7f7f7f';
           }
           return temp_node_color;
       });
    svg.selectAll('.circle')
       .transition().duration(1000)
       .attr('r', function(d, i) {
           var temp_node_highlight = 5;
           if (nodes[i].highlight == 3) {
               temp_node_highlight = 8;
           }
           return temp_node_highlight;
       });
}

function draw_force_directed_graph() {
    $.getJSON('/_get_graph_data', {}, function(data) {
        var link, node;
        var edges = data.links;
        var nodes = data.nodes;

        var link_scale = d3.scale.linear().domain(
                [d3.min(edges, function(d) {return d.weight;}), d3.max(edges, function(d) {return d.weight;})]
            ).range([100,500]);
        var tMax = d3.max(edges, function(d) {return d.weight;});
        var force = d3.layout.force()
              .nodes(nodes)
              .links(edges)
              .linkDistance(function(d) {
                  //console.log("weight" + d.weight);
                  //console.log("max1: " + 10 * (tMax - Math.sqrt(d.weight)));
                  //console.log("max2: " + 10 * Math.sqrt(d.source.size) + 10 * Math.sqrt(d.target.size) + 50);
                  //return 10 * (50 - Math.sqrt(d.weight)) + 10 * Math.sqrt(d.source.size) + 10 * Math.sqrt(d.target.size);
                  //return Math.max(10 * (50 - Math.sqrt(d.weight)) , 10 * Math.sqrt(d.source.size) + 10 * Math.sqrt(d.target.size) + 20);
                  return 10;
                //return link_scale(d.weight) + 10 * Math.sqrt(d.source.size) + 10 * Math.sqrt(d.target.size);

              })
              .linkStrength(function(d) {
                  //return 1.0 / 85 * d.weight;
                  return 1;
              })
              .charge(-100)
              .on('tick', tick)
              .size([width, height]);

        force.start();

        node = svg.selectAll('.node')
                .data(nodes)
                .enter().append('circle')
                .attr('class', 'node')
                .style('opacity', 0.5)
                .attr('r', function(d) {
                    //return 10 * Math.sqrt(d.size);
                    return 5;
                })
                .style('fill', function(d) {
                    //return color(d.id);
                    return color(d.cluster);
                }).call(force.drag);

        link = svg.selectAll('.link')
                .data(edges)
                .enter().append('line')
                .attr('class', function(d) {
                    return 'link';
                })
                .style('stroke', '#222222')
                .style('opacity', 0.3)
                .style('stroke-width', function(d) {
                    //return Math.sqrt(d.weight);
                    return 1;
                });

        //var k = 0;
        //while ((force.alpha() > 1e-2) && (k < 300)) {
            //force.tick(),
            //k = k + 1;
        //}

        function collide(alpha) {
          var quadtree = d3.geom.quadtree(nodes);
          return function(d) {
              var radius = 10 * Math.sqrt(d.size);
              var r = radius + 20,
                  nx1 = d.x - r,
                  nx2 = d.x + r,
                  ny1 = d.y - r,
                  ny2 = d.y + r;
              quadtree.visit(function(quad, x1, y1, x2, y2) {
                    if (quad.point && (quad.point !== d)) {
                            var x = d.x - quad.point.x,
                                y = d.y - quad.point.y,
                                l = Math.sqrt(x * x + y * y),
                                r = radius + Math.sqrt(quad.point.size * 10) + 20;
                            if (l < r) {
                                      l = (l - r) / l * alpha;
                                      d.x -= x *= l;
                                      d.y -= y *= l;
                                      quad.point.x += x;
                                      quad.point.y += y;
                                    }
                          }
                    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                  });
            };
        }

        function tick(e) {
            link.attr('x1', function(d) { return d.source.x; })
                .attr('y1', function(d) { return d.source.y; })
                .attr('x2', function(d) { return d.target.x; })
                .attr('y2', function(d) { return d.target.y; });

            //node.each(collide(.5));
            node.attr('cx', function(d) { return d.x; })
                .attr('cy', function(d) { return d.y; });
        }
    });
}
