/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.BoundaryEdge = function(Visualization){

    var BoundaryEdge = function(dat, svg, dataManager, className){
        console.log('[LOG] Init Boundary Edge');
        Visualization.call(this, dat, svg, dataManager, className);
        this.data = dataManager.getEdge();
        this.node = dataManager.original.nodes;
        this.opacity = 0.1;
        this.draw_inside = true;
        this.control();
    };

    BoundaryEdge.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);
                folder.add(this, 'opacity', 0, 1).step(0.1).onFinishChange(function(){
                    _this.update();
                });

                folder.add(this, 'draw_inside').onFinishChange(function(){
                    _this.update();
                })
            }
        },

        update : {
            value : function(){
                var _this = this;
                this.svg.selectAll('path')
                    .style('stroke', '#000')
                    .style('stroke-width', 1)
                    .style('fill', 'none')
                    .style('stroke-opacity', function(d){

                        if(_this.draw_inside){
                            return _this.opacity;
                        }else{
                            if(_this.node[d.target].cluster == _this.node[d.source].cluster){
                                return 0;
                            }else{
                                return _this.opacity;
                            }
                        }
                    });
            }
        },

        display : {
            value : function(){

                var startTime = new Date().getTime();
                var fundling = d3.ForceEdgeBundling().nodes(this.node).edges(this.data);
                var results = fundling();

                var endTime = new Date().getTime();

                console.log('time');
                console.log(endTime-startTime);

                var d3line = d3.svg.line()
                    .x(function(d){return d.x;})
                    .y(function(d){return d.y;})
                    .interpolate('linear');

                this.svg.selectAll('path')
                    .data(this.data)
                    .enter()
                    .append('path')
                    .attr('d', function(d, i){
                        return d3line(results[i]);
                    });

                this.update();

            }
        }
    });

    return BoundaryEdge;

}(LG.visual.Visualization);