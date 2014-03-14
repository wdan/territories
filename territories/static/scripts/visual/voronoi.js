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
                            return "SIGKDD";
                        }else if(tmp == 1074){
                            return "SOSP";
                        }else if(tmp == 1615){
                            return "ASPLOS";
                        }else if(tmp == 1451){
                            return "PPOPP";
                        }else if(tmp == 890){
                            return "ISCA";
                        }else if(tmp == 853){
                            return "HPCA";
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
