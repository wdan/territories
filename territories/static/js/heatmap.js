/**
 * Created by wenbin on 7/3/14.
 */

var heatmap = function(data, svg, w, h, pix, scale){

    var maxValue = 300;
    var grid = [];

    for (var i = 0; i<w; i+=pix){
        for(var j = 0; j<h; j+=pix){
            grid.push({x:i, y:j});
        }
    }

    var kde = kernelDensityEstimator(epanechnikovKernel(scale), grid);

    var raw_data = kde(data);

    var scaleValue = d3.scale.linear()
        .domain([0, d3.max(raw_data, function(d){return d.z;})])
        .range([0, maxValue]);

    var c = d3.scale.linear()
        .domain([0, maxValue])
        .range(["white", "red"]);

    var o = d3.scale.linear()
        .domain([0, maxValue])
        .range([0, 1]);

    svg.selectAll(".gas")
        .data(raw_data)
        .enter()
        .append("circle")
        .attr("r", 1)
        .attr("class", "gas")
        .attr("cx", function(d){
            return d.x;
        })
        .attr("cy", function(d){
            return d.y;
        })
        .attr("fill", function(d){
            return c(scaleValue(d.z));
        })
        .attr("fill-opacity",function(d){
            return o(scaleValue(d.z));
        });
}

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