var width = 800;
var height = 600;
var color = d3.scale.category10();

var svg = d3.select('#paint_zone')
            .append('svg')
            .attr('width', width * 2)
            .attr('height', height * 2);

set_mouse_event_handler();
draw_force_directed_graph();
