/**
 * Created by wenbin on 13/3/14.
 */

LG.visual.InsideNode = function(Visualization){

    var InsideNode = function(dat, svg, dataManager, className){

        console.log('[LOG] Init Inside Node');
        Visualization.call(this, dat, svg, dataManager, className);
        this.data = dataManager.getInsideNode();
        this.r = 3;
        this.stroke_width = 1;
        this.control();

    };

    InsideNode.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){

                var _this = this;

                var folder = this.dat.addFolder(this.className);

                folder.add(this, 'r', 0, 10).step(0.1).onFinishChange(function(){
                    _this.update();

                });

                folder.add(this, 'stroke_width', 0, 5).step(0.5).onFinishChange(function(){
                    _this.update();
                });
            }
        },

        update : {
            value : function(){

                var _this = this;

                this.svg.selectAll('circle')
                    .attr('r', _this.r)
                    .attr('stroke-width',_this.stroke_width);
            }
        },

        display : {
            value : function(){
                var _this = this;

                this.svg.selectAll('circle')
                    .data(this.data)
                    .enter()
                    .append('circle')
                    .attr('stroke', '#fff')
                    .attr('fill', function(d){

                        return _this.classColor[d.cluster];

                    })
                    .attr('cx', function(d){
                        return d.x;
                    })
                    .attr('cy', function(d){
                        return d.y;
                    });

                this.update();




            }
        }

    });

    return InsideNode;

}(LG.visual.Visualization);