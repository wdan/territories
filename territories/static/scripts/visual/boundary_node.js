/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.BoundaryNode = function(Visualization){
    var BoundaryNode = function(dat, svg, dataManager, className){

        console.log('[LOG] Init Boundary Node');
        Visualization.call(this, dat, svg, dataManager, className);

        this.data = dataManager.getVisibleBoundaryNode();
        this.boundary_node_r = 5;
        this.boundary_node_opacity = 0.5;
        this.control();

    };

    BoundaryNode.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);

                folder.add(this, 'boundary_node_r', 0, 10).step(0.5).onFinishChange(function(){
                    _this.update();
                });
                folder.add(this, 'boundary_node_opacity', 0, 1).step(0.1).onFinishChange(function(){
                    _this.update();
                });
            }
        },

        update : {
            value : function(){
                this.svg.selectAll('circle')
                    .attr('r', this.boundary_node_r)
                    .style('opacity', this.boundary_node_opacity);
            }
        },

        display : {
            value : function(){
                var _this = this;
                this.svg.selectAll('circle')
                    .data(this.data)
                    .enter()
                    .append('circle')
                    .attr('cx', function(d){return d.x})
                    .attr('cy', function(d){return d.y})
                    .style('fill', function(d){
                        return _this.classColor[d.cluster];
                    });

                this.update();
            }
        }

    });

    return BoundaryNode;

}(LG.visual.Visualization);