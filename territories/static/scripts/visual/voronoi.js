/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.Voronoi = function(Visualization){

    var Voronoi = function(dat, svg, dataManager, className){
        console.log('[LOG] Init Voronoi');
        Visualization.call(this, dat, svg, dataManager, className);
        this.data = dataManager.polygon;
        this.label = dataManager.getlabel();
        this.voronoi_color_set = true;
        this.voronoi_fill = '#4682B4';
        this.color_scale = d3.scale.linear().domain([0, 1]).range(['white', this.voronoi_fill]);
        this.voronoi_opacity = 1.0;
        this.draw_mid_node = false;
        this.subdivision = 0;
        this.scale = 40;
        this.control();
    };

    var subdivision_k = function(points, k){

        for(var i=0;i<k;i++){
            points = subdivision_one(points);
        }
        return points;
    };

    var subdivision_one = function(points){

        n = points.length;
        mid = [];
        res = [];
        for(var i=0;i<n;i++){
            mid.push({x:(points[i].x+points[(i+1)%n].x)/2,y:(points[i].y+points[(i+1)%n].y)/2});
        }

        for(i=0;i<n;i++){
            res.push({x:(points[i].x+mid[i].x)/2, y:(points[i].y+mid[i].y)/2});
            res.push({x:(points[(i+1)%n].x+mid[i].x)/2, y:(points[(i+1)%n].y+mid[i].y)/2});
        }

        return res;

    };

    // helper function
    var vectorNorm = function(from, to){
        var v = {
            x : to.x - from.x,
            y : to.y - from.y
        };
        v.length = Math.sqrt( v.x * v.x + v.y * v.y);
        v.x = v.x / v.length;
        v.y = v.y / v.length;
        return v;
    };

    var interp = function (center, point, scale){

        var v = vectorNorm(center, point);
        var k = (v.length - scale) / v.length;

        return{
            x : ( k * v.length * v.x + center.x),
            y : ( k * v.length * v.y + center.y)
        };
    };

    var expand = function(d, mid, scale){

        var res = [];

        for(var i=0;i< d.length;i++){
            res.push(interp(mid, d[i], scale));
        }

        return res;
    };


    Voronoi.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);
                folder.add(this, 'voronoi_color_set').onFinishChange(function(){
                    _this.update();
                });

                folder.add(this, 'subdivision', 0, 10).step(1).onFinishChange(function(){
                   _this.update();
                });

                folder.add(this, 'scale', 0, 100).step(5).onChange(function(){
                    _this.update();
                });

                folder.addColor(this, 'voronoi_fill').onChange(function(){

                    if(!_this.voronoi_color_set){
                        _this.color_scale = d3.scale.linear().domain([0, 1]).range(['white', _this.voronoi_fill]);
                        _this.update();
                    }
                });

                folder.add(this, 'voronoi_opacity', 0, 1).step(0.1).onFinishChange(function(){
                    _this.update();
                });

                folder.add(this, 'draw_mid_node').onFinishChange(function(){
                    _this.middle_node();
                });
            }
        },

        update : {
            value : function(){
                var _this = this;
                this.svg.selectAll('path')
                    .transition()
                    .duration(1000)
                    .attr('d', function(d){
                        var points = expand(d.points, {x: d.mid_x, y:d.mid_y}, _this.scale);
                        points = subdivision_k(points, _this.subdivision);

                        var s = 'M ' + points[0].x + ' ' + points[0].y;
                        for(var j=1;j< points.length;j++){
                            s += ' L ' + points[j].x + ' ' + points[j].y;
                        }
                        s += 'Z';
                        return s;
                    })
                    .style('fill', function(d){
                        if (_this.voronoi_color_set) return _this.classColor[d.cluster];
                        else{
                            var c = Math.random();
                            return _this.color_scale(c);
                        }
                    })
                    .style('fill-opacity', _this.voronoi_opacity);
            }
        },

        middle_node :{
            value : function(){
                if(this.draw_mid_node){
                    this.svg.selectAll('circle')
                        .data(this.data)
                        .enter()
                        .append('circle')
                        .attr('r', 5)
                        .attr('cx', function(d) {return d.mid_x;})
                        .attr('cy', function(d) {return d.mid_y;})
                        .attr('fill', '#fff')
                        .attr('opacity', 0.8);
                }else{
                    this.svg.selectAll('circle')
                        .data([])
                        .exit()
                        .remove();
                }
            }
        },

        showLabel : {
            value : function(){
                var _this = this;

                this.svg.selectAll('text')
                    .data(this.data)
                    .enter()
                    .append('text')
                    .text(function(d){

                        var tmp = _this.label[d.cluster];

                        if( tmp == 2308){
                            return "VAST";
                        }else if(tmp == 1984){
                            return "INFOVIS";
                        }else if(tmp == 1512){
                            return "SIGGRAPH";
                        }else if(tmp == 3078){
                            return "SIGKDD"
                        }else if(tmp == 2960){
                            return "TVCG";
                        }else{
                            return "";
                        }
                    })
                    .attr('text-anchor', 'middle')
                    .attr("x", function(d){
                        return d.mid_x;
                    })
                    .attr("y", function(d){
                        return d.mid_y;
                    })
            }
        },

        display : {
            value : function(){

                var _this = this;

                this.svg.selectAll('path')
                    .data([])
                    .exit()
                    .remove();

                this.svg.selectAll('path')
                    .data(this.data)
                    .enter()
                    .append('path')
                    .attr('d', function(d){
                        var points = expand(d.points, {x: d.mid_x, y:d.mid_y}, _this.scale);
                        points = subdivision_k(points, _this.subdivision);

                        var s = 'M ' + points[0].x + ' ' + points[0].y;
                        for(var j=1;j< points.length;j++){
                            s += ' L ' + points[j].x + ' ' + points[j].y;
                        }
                        s += 'Z';
                        return s;
                    })
                    .style('fill', function(d){
                        if (_this.voronoi_color_set) return _this.classColor[d.cluster];
                        else{
                            var c = Math.random();
                            return _this.color_scale(c);
                        }
                    })
                    .style('fill-opacity', _this.voronoi_opacity);
//                this.update();
            }
        }
    });

    return Voronoi;
}(LG.visual.Visualization);