/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.Voronoi = function(Visualization){

    var Voronoi = function(dat, svg, dataManager, className){
        console.log('[LOG] Init Voronoi');
        Visualization.call(this, dat, svg, dataManager, className);
        this.data = dataManager.polygon;
        this.voronoi_color_set = false;
        this.voronoi_fill = '#4682B4';
        this.color_scale = d3.scale.linear().domain([0, 1]).range(['white', this.voronoi_fill]);
        this.voronoi_opacity = 1.0;
//        this.voronoi_stroke = '#4682B4';
//        this.voronoi_stroke_width = 3;
        this.draw_mid_node = false;
        this.control();
    };

    Voronoi.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);
                folder.add(this, 'voronoi_color_set').onFinishChange(function(){
                    _this.update();
                });

                folder.addColor(this, 'voronoi_fill').onChange(function(){

                    if(!_this.voronoi_color_set){
//                        _this.voronoi_stroke = _this.voronoi_fill;
                        _this.color_scale = d3.scale.linear().domain([0, 1]).range(['white', _this.voronoi_fill]);
                        _this.update();
                    }
                });

//                Visualization.prototype.addControl.call(this, 0, 'voronoi_color_set', function(){
//                    _this.update();
//                });

//                Visualization.prototype.addControl.call(this, 1, 'voronoi_fill', function(){
//
//                    if(!_this.voronoi_color_set){
////                        _this.voronoi_stroke = _this.voronoi_fill;
//                        _this.color_scale = d3.scale.linear().domain([0, 1]).range(['white', _this.voronoi_fill]);
//                        _this.update();
//                    }
//                });

                folder.add(this, 'voronoi_opacity', 0, 1).step(0.1).onFinishChange(function(){
                    _this.update();
                });

                folder.add(this, 'draw_mid_node').onFinishChange(function(){
                    _this.middle_node();
                });
//                Visualization.prototype.addControl.call(this, 0, 'draw_mid_node', function(){
//                    _this.middle_node();
//                });

//                this.datList.push(tmp);
            }
        },

        update : {
            value : function(){
                var _this = this;
                this.svg.selectAll('path')
                    .style('fill', function(d){
                        if (_this.voronoi_color_set) return _this.classColor[d.cluster];
                        else{
                            var c = Math.random();
                            return _this.color_scale(c);
                        }
                    })
//                    .style('stroke', function(d){
//                        if (_this.voronoi_color_set) return _this.classColor[d.cluster];
//                        else return _this.voronoi_stroke;
//                    })
                    .style('fill-opacity', _this.voronoi_opacity)
//                    .style('stroke-opacity', _this.voronoi_opacity)
//                    .style('stroke-width', _this.voronoi_stroke_width+'px');
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

        display : {
            value : function(){
                this.svg.selectAll('path')
                    .data(this.data)
                    .enter()
                    .append('path')
                    .attr('d', function(d){
                        var points = d.points;
                        var s = 'M ' + points[0].x + ' ' + points[0].y;
                        for(var j=1;j< points.length;j++){
                            s += ' L ' + points[j].x + ' ' + points[j].y;
                        }
                        s += 'Z';
                        return s;
                    });
                this.update();
            }
        }
    });

    return Voronoi;
}(LG.visual.Visualization);