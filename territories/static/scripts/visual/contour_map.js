/**
 * Created by wenbin on 12/3/14.
 */


LG.visual.ContourMap = function(){

    return function(data, svg, pix, scale, color){
        var maxValue = 300;
        var start = 10;
        var end = 300;
        var step = 100;

        var grid = [];
        var left = d3.min(data, function(d){return d.x;}) - scale;
        var right = d3.max(data, function(d){return d.x;}) + scale;
        var top = d3.min(data, function(d){return d.y}) - scale;
        var bottom = d3.max(data, function(d){return d.y}) + scale;


        for (var i = left; i<right; i+=pix){
            for(var j = top; j<bottom; j+=pix){
                grid.push({x:i, y:j});
            }
        }

        var kde = kernelDensityEstimator(epanechnikovKernel(scale), grid);
        var raw_data = kde(data);

        var scaleValue = d3.scale.linear()
            .domain([0, d3.max(raw_data, function(d){return d.z;})])
            .range([0, maxValue]);

        var count = 0;
        var grid_data = [];
        for (i = left; i<right; i+=pix){
            var tmp = [];
            for(j = top; j<bottom; j+=pix){
                tmp.push(scaleValue(raw_data[count++].z));
            }
            grid_data.push(tmp);
        }

        var cliff = -100;
        grid_data.push(d3.range(grid_data[0].length).map(function() { return cliff; }));
        grid_data.unshift(d3.range(grid_data[0].length).map(function() { return cliff; }));
        grid_data.forEach(function(d) {
            d.push(cliff);
            d.unshift(cliff);
        });

        var c = new Conrec,
            xs = d3.range(0, grid_data.length),
            ys = d3.range(0, grid_data[0].length),
            zs = d3.range(start, end, step),
            x = d3.scale.linear().range([left, right]).domain([0, grid_data.length]),
            y = d3.scale.linear().range([top, bottom]).domain([0, grid_data[0].length]),
            colours = d3.scale.linear().domain([start, end]).range(["#fff", color]);

        c.contour(grid_data, 0, xs.length - 1, 0, ys.length - 1, xs, ys, zs.length, zs);

        svg.selectAll("path")
            .data(c.contourList())
            .enter()
            .append("path")
            .style("fill",function(d) { return colours(d.level);})
            .style("stroke",function(d) { return colours(d.level);})
            .style("fill-opacity", 0.3)
            .attr("d", d3.svg.line()
                .x(function(d) { return x(d.x); })
                .y(function(d) { return y(d.y); }));

    };

    function kernelDensityEstimator(kernel, grid) {
        return function(sample){
            return grid.map(function(grid){
                return {x:grid.x, y:grid.y, z:d3.mean(sample, function(g){
                    var d = Math.sqrt((grid.x-g.x)*(grid.x-g.x) + (grid.y-g.y)*(grid.y-g.y));
                    return kernel(d);
                })};
            });
        };
    }

    function epanechnikovKernel(scale) {
        return function(u) {
            return Math.abs(u /= scale) <= 1 ? .75 * (1 - u * u) / scale : 0;
        };
    }

};