/**
 * Created by wenbin on 14/3/14.
 */

LG.visual.NodeLabel = function(Visualization){

    var NodeLabel = function(dat, svg, dataManager, className){
        console.log('[LOG] Init Node Label');
        Visualization.call(this, dat, svg, dataManager, className);
        this.show = false;
        this.data = dataManager.getVisibleBoundaryNode();
        this.control();
    };

    NodeLabel.prototype = Object.create(Visualization.prototype, {
        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);

                folder.add(this, 'show').onFinishChange(function(){
                    _this.update();
                });
            }
        },

        update : {
            value : function(){
                var _this = this;
                this.svg.selectAll('text')
                    .style('visibility', function(){
                        if(_this.show) return 'visible';
                        else return 'hidden';
                    })
            }
        },

        display : {
            value : function(){

                this.svg.selectAll('text')
                    .data(this.data)
                    .enter()
                    .append('text')
                    .text(function(d){
                        return d.label;
                    })
                    .attr('x', function(d){
                        return d.x;
                    })
                    .attr('y', function(d){
                        return d.y;
                    });
                this.update();


            }
        }
    });

    return NodeLabel;
}(LG.visual.Visualization);
