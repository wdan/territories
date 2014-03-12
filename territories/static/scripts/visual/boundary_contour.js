/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.BoundaryContour = function(Visualization){

    var BoundaryContour = function(dat, svg, dataManager, className){

        console.log('[LOG] Init Boundary Contour');
        Visualization.call(this, dat, svg, dataManager, className);
        this.polygon = dataManager.polygon;
        this.node = dataManager.getBoundaryNode();
        this.data = {};
        this.cluster_list = [];
        this.getData();
        this.contour_pix = 2;
        this.contour_scale = 50;
        this.control();

    };

    BoundaryContour.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);
                folder.add(this, 'contour_pix', 1, 10).step(1).onFinishChange(function(){
                    _this.display();
                });
                folder.add(this, 'contour_scale', 5, 100).step(5).onFinishChange(function(){
                    _this.display();
                });
            }

        },

        getData : {
            value : function(){

                for(var i=0;i<this.polygon.length;i++){
                    var p = this.polygon[i];
                    this.data[p.cluster] = [];
                    this.cluster_list.push(p.cluster);
                }

                for(i=0;i<this.node.length;i++){
                    this.data[this.node[i].cluster].push({x:this.node[i].x, y:this.node[i].y});
                }

                console.log(this.data);
            }
        },

        display : {

            value : function(){

                this.svg.selectAll('.' + this.className)
                    .data([])
                    .exit()
                    .remove();

                for(var i=0;i<this.cluster_list.length;i++){
                    var cid = this.cluster_list[i];
                    if(this.data[cid].length!=0){
                        LG.visual.ContourMap(this.data[cid], this.svg.append('g').attr('class', this.className),
                            this.contour_pix, this.contour_scale, this.classColor[cid]);
                    }
                }
            }
        }
    });

    return BoundaryContour;
}(LG.visual.Visualization);