var width = 700;
var height = 700;
var color = d3.scale.category10();

var svg = d3.select('#paint_zone')
            .append('svg')
            .attr('width', width * 4)
            .attr('height', height * 4);

set_mouse_event_handler();
draw_force_directed_graph();
