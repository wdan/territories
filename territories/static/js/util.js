function draw_ruler(r, max, max_step) {
    //var ruler = [1, 2, 5, 10, 20, 50, 100, 200, 400, 800];
    var ruler = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024];
    var ruler_angle = [];
    for (var i = 0; i < ruler.length; i++) {
        ruler_angle[i] = log2(ruler[i]) / max * 2 * Math.PI;
    }

    svg.selectAll('line')
       .data(ruler_angle)
       .enter()
       .append('line')
       .attr('class', 'ruler-line')
       .attr('stroke', 'black')
       .attr('stroke-width', 1)
       .attr('stroke-dasharray', '5, 5')
       .attr('stroke-opacity', function(d, i) {
           //if (i == 0) {
                 //return 0.5;
           //}else {
           return 0.7;
           //}
       })
       .attr('x1', width / 2)
       .attr('y1', height / 2)
       .attr('x2', function(d) {
           return width / 2 + (r * max_step) * Math.sin(d);
       })
       .attr('y2', function(d) {
           return height / 2 - (r * max_step) * Math.cos(d);
       });

    svg.selectAll('text')
       .data(ruler_angle)
       .enter()
       .append('text')
       .attr('class', 'ruler-label')
       .attr('fill', 'black')
       .attr('stroke', 'black')
       .style('opacity', 1)
       .text(function(d, i) {
           return ruler[i];
       })
       .attr('transform', function(d) {
           var l = r * max_step + 25;
           var x = width / 2 + l * Math.sin(d);
           var y = height / 2 - l * Math.cos(d);
           return ['translate(', x, ',', y, ')'].join('');
       });
}

function draw_axis(r, max) {
    circles = [];
    for (var i = 1; i <= max; i++)
        circles.push(i * r);

    svg.selectAll('.axis')
       .remove();

    svg.selectAll('.axis')
       .data(circles)
       .enter()
       .append('circle')
       .transition().duration(1000)
       .attr('class', 'axis')
       .attr('cx', width / 2)
       .attr('cy', height / 2)
       .attr('stroke', 'black')
       .attr('stroke-width', 1)
       .attr('stroke-dasharray', '5, 5')
       .attr('stroke-opacity', 0.7)
       .attr('fill', 'none')
       .attr('r', function(d) {
           return d;
       });
}

function log2(x) {
    return Math.log(x) / Math.log(2);
}

//function set_mouse_event_handler() {
//    jQuery('#paint_zone').bind('mousedown', function(event) {
//        if (!visdiv_draging) {
//            visdiv_draging = true;
//        }
//        draging_updating_page.x = event.pageX;
//        draging_updating_page.y = event.pageY;
//    }).bind('mousemove', function(event) {
//        if (visdiv_draging) {
//            var delta_page = {};
//            delta_page.x = event.pageX - draging_updating_page.x;
//            delta_page.y = event.pageY - draging_updating_page.y;
//            draging_updating_page.x = event.pageX;
//            draging_updating_page.y = event.pageY;
//            var $svg = jQuery('#paint_zone svg');
//            var curTop = $svg.css('margin-top');
//            curTop = new Number(curTop.substring(0, curTop.length - 2));
//            var curLeft = $svg.css('margin-left');
//            curLeft = new Number(curLeft.substring(0, curLeft.length - 2));
//            curTop += delta_page.y;
//            curLeft += delta_page.x;
//            if (curTop > 0)
//                curTop = 0;
//            if (curTop < -height / 2)
//                curTop = -height / 2;
//            if (curLeft > 0)
//                curLeft = 0;
//            if (curLeft < -width / 2)
//                curLeft = -width / 2;
//            $svg.css('margin-top', curTop + 'px');
//            $svg.css('margin-left', curLeft + 'px');
//        }
//    }).bind('mouseup', function(event) {
//        visdiv_draging = false;
//        draging_updating_page = {};
//    });
//
//}

function do_ajax(get_url, data_text, data_url) {
    var t_nodes, t_edges;
    var t_ajax_data = {
        type: 'GET',
        url: get_url,
        success: function(data) {
            t_edges = data.edges;
            t_nodes = data.nodes;
        },
        async: false
    };
    if (data_url) {
        t_ajax_data['data'] = data_text + '=' + $(data_url).val();
    }
    $.ajax(t_ajax_data);
    set_attribute(t_nodes, t_edges);
    if (data_url) {
        $(data_url)[0].focus();
        $(data_url).val('');
    }
    return [t_nodes, t_edges];
}

function backup_positions() {
    nodes_backup = [];
    edges_backup = [];
    svg.selectAll('.circle')
       .each(function(d, i) {
           nodes_backup.push([this.getAttribute('cx'), this.getAttribute('cy')]);
       });
    svg.selectAll('.link')
       .each(function(d, i) {
           edges_backup.push([this.getAttribute('x1'), this.getAttribute('y1'),
                              this.getAttribute('x2'), this.getAttribute('y2')]);
       });
}

function restore_positions() {
    svg.selectAll('.circle')
       .transition().duration(1000)
       .attr('cx', function(d, i) {
           return nodes_backup[i][0];
       })
       .attr('cy', function(d, i) {
           return nodes_backup[i][1];
       });
    svg.selectAll('.link')
       .transition().duration(1000)
       .attr('x1', function(d, i) {
           return edges_backup[i][0];
       })
       .attr('y1', function(d, i) {
           return edges_backup[i][1];
       })
       .attr('x2', function(d, i) {
           return edges_backup[i][2];
       })
       .attr('y2', function(d, i) {
           return edges_backup[i][3];
       });
    svg.selectAll('.node')
       .select('text')
       .transition().duration(1000)
       .attr('transform', function(d, i) {
           if (this.getClientRects()[0] === undefined) {
               return ['translate(', nodes_backup[i][0], ',', (nodes_backup[i][1] + 13), ')'].join('');
           }
           if (this.getAttribute('text-anchor') == 'start') {
               return ['translate(', (nodes_backup[i][0] - this.getClientRects()[0]['width'] / 2),
                        ',', (nodes_backup[i][1] + 13), ')'].join('');
           } else if (this.getAttribute('text-anchor') == 'end') {
               return ['translate(', (nodes_backup[i][0] + this.getClientRects()[0]['width'] / 2),
                ',', (nodes_backup[i][1] + 13), ')'].join('');
           } else {
               return ['translate(', nodes_backup[i][0], ',', (nodes_backup[i][1] + 13), ')'].join('');
           }
       });
}
