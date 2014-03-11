/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.Voronoi = function(){

    var Voronoi = function(dat, svg, dataManager){
        this.svg = svg;
//        this.dataManager = dataManager;
        this.width = dataManager.width;
        this.height = dataManager.height;
        this.data = dataManager.aggregate.nodes;
        this.voronoi_fill = '#4682B4';
        this.voronoi_stroke = '#4682B4';
        this.voronoi_stroke_width = 3;

        dat.addColor(this, 'voronoi_fill').onFinishChange(function(value){
            console.log(value);
            this.update();
        });

        dat.addColor(this, 'voronoi_stroke').onFinishChange(function(value){
            console.log(value);
            this.update();
        });
        dat.add(this, 'voronoi_stroke_width', 1, 5).step(0.1).onFinishChange(function(value){
            console.log(value);
            this.update();
        });

    };

    Object.defineProperties(Voronoi.prototype, {

       update : {
           value : function(){
               var _this = this;
               this.svg.selectAll('path .voronoi')
                   .attr('fill', _this.voronoi_fill)
                   .attr('stroke', _this.voronoi_stroke)
                   .attr('stroke-width', _this.voronoi_stroke_width+'px');
           }
       },
       display : {
           value : function(){
               var _this = this;
               this.svg.selectAll('path .voronoi')
                   .data(_this.data)
                   .enter()
                   .append('path')
                   .attr('class', 'voronoi')
                   .attr('d', function(d, i){

                       console.log(d);
                       console.log(i);

                       var s = 'M ' + d[0].x + ' ' + d[0].y;

                       for(var j=1;j< d.length;j++){
                           s += ' L ' + d[j].x + ' ' + d[j].y;
                       }

                       s += 'Z';
                       return s;

                   });

               this.update();
           }
       }
    });

    return Voronoi;
}();