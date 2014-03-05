/**
 * Created by wenbin on 22/2/14.
 */

    // data
function draw_voronoi() {
    // center node
    $.ajax({
        dataType: 'json',
        url: '/_get_voronoi_data',
        async: false,
        success: function(data) {
            console.log(data);
            var edges = data[0]['links'];
            var node = data[1]['nodes'];
            var vono = data[1]['polygons'];
            var w = 960;
            var h = 720;
            // compute coordinate max, min for scale
            //
            cluster_dict = {}
            var xlist = [];
            var ylist = [];
            for (var i = 0; i < node.length; i++) {
                xlist.push(node[i].x);
                ylist.push(node[i].y);
                cluster_id = node[i].cluster;
                cluster_dict[cluster_id] = {'x': node[i].x, 'y': node[i].y};
                for (var j = 0; j < vono[i].length; j++) {
                    xlist.push(vono[i][j].x);
                    ylist.push(vono[i][j].y);
                }
            }

            // x, y axis scale
            var xscale =  d3.scale.linear().domain([Math.min.apply(Math, xlist), Math.max.apply(Math, xlist)]).range([0, w]);
            var yscale = d3.scale.linear().domain([Math.min.apply(Math, ylist), Math.max.apply(Math, ylist)]).range([0, h]);

            var svg = d3.select('body').append('svg')
                        .attr('width', w)
                        .attr('height', h)
                        .on('click', function() {
                            console.log(d3.mouse(this));
                        });

            // draw nodes
            svg.selectAll('circle')
                .data(node)
                .enter()
                .append('circle')
                .attr('r', 5)
                .attr('cx', function(d) {return xscale(d.x);})
                .attr('cy', function(d) {return yscale(d.y);})
                .attr('fill', '#2ca25f');

            // draw path
            svg.selectAll('path')
                .data(vono)
                .enter()
                .append('path')
                .attr('d', function(d, i) {

                    var scale = 50;
                    var tmp = interp(node[i], d[0], scale);
                    var s = 'M ' + xscale(tmp.x) + ' ' + yscale(tmp.y);

                    for(var j = 1; j < d.length; j++) {
                        tmp = interp(node[i], d[j], scale);
                        s += ' L ' + xscale(tmp.x) + ' ' + xscale(tmp.y);
                    }
                    s += 'Z';
                    return s;

                })
                .style('fill', 'steelblue')
                .style('opacity', function(d) {
                    return Math.random() / 1.5;
                })
                .attr('stroke', 'steelblue')
                .attr('stroke-width', '3px')
                .attr('stroke-opacity', 1);

            link = svg.selectAll('.link')
                    .data(edges)
                    .enter().append('line')
                    .attr('class', function(d) {
                        return 'link';
                    })
                    .attr('x1', function(d) { return cluster_dict[d.source].x; })
                    .attr('y1', function(d) { return cluster_dict[d.source].y; })
                    .attr('x2', function(d) { return cluster_dict[d.target].x; })
                    .attr('y2', function(d) { return cluster_dict[d.target].y; })
                    .style('stroke', '#222222')
                    .style('opacity', 0.1)
                    .style('stroke-width', function(d) {
                        return d.weight;
                        //return 1;
                    });

        }
    });
}

// helper function, just ignore
function vectorNorm(from, to) {
    var v = {
        x: to.x - from.x,
        y: to.y - from.y
    };
    v.length = Math.sqrt(v.x * v.x + v.y * v.y);
    v.x = v.x / v.length;
    v.y = v.y / v.length;
    return v;
}

//                            <--scale-->
// center --------------------X---------> point,
// compute X coordinates
function interp(center, point, scale) {
    var v = vectorNorm(center, point);
    var k = (v.length - scale) / v.length;
    return{
        x: (k * v.length * v.x + center.x),
        y: (k * v.length * v.y + center.y)
    };
}


