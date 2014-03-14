/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.BoundaryEdge = function(Visualization){

    var BoundaryEdge = function(dat, svg, dataManager, className){
        console.log('[LOG] Init Boundary Edge');
        Visualization.call(this, dat, svg, dataManager, className);
        this.data = dataManager.getEdge();
        this.node = dataManager.original.nodes;
    };

    BoundaryEdge.prototype = Object.create(Visualization.prototype, {
        display : {
            value : function(){
                var _this = this;
                this.svg.selectAll('path')
                    .data(this.data)
                    .enter()
                    .append('path')
                    .attr('d', function(d){
                        return 'M' + _this.node[d.source].x + ' ' + _this.node[d.source].y
                        +'L' + _this.node[d.target].x + ' ' + _this.node[d.target].y;
                    })
                    .style('stroke', 'black')
                    .style('stroke-opacity', 0.1);
            }
        }
    });

    return BoundaryEdge;

}(LG.visual.Visualization);