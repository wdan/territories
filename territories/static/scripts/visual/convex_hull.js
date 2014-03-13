/**
 * Created by wenbin on 12/3/14.
 */


LG.visual.ConvexHull = function(Visualization){

    var ConvexHull = function(dat, svg, dataManager, className){
        console.log('[LOG] Init Convex Hull');
        Visualization.call(this, dat, svg, dataManager, className);
        this.node = dataManager.getVisibleBoundaryNode();
        this.polygon = dataManager.polygon;
        this.data = {};
        this.cluster_list = [];
        this.cluster_dict = {};
        getConvexHullData(this, this.node, this.polygon);
        this.hull_roundlen = 10;
        this.ratio = 0.12;
        this.hull_bend = 8;
        this.hull_fill = '#a6bddb';
        this.hull_fill_opacity = 0;
        this.hull_color_set = false;
        this.control();

    };

    var getConvexHullData = function(obj, node, polygon){
        for(var i=0;i<polygon.length;i++){
            var p = polygon[i];
            obj.data[p.cluster] = [];
            obj.cluster_list.push(p.cluster);
            obj.cluster_dict[i] = p.cluster;
            for(var j=0;j< p.points.length;j++){
                obj.data[p.cluster].push([p.points[j].x, p.points[j].y]);
            }
        }
        for(i=0;i<node.length;i++){
            obj.data[node[i].cluster].push([node[i].x, node[i].y]);
        }
    };

    function segment(cur, next, roundlen, bend, ratio){
        var s ="";
        var v = vectorNorm(cur, next);
        var r = vecterRotate(v, 0);
        s += " A " + roundlen + " " + roundlen + " 0 0 1 "
            + (r.x * roundlen + cur[0]) + " " + (r.y * roundlen + cur[1]);
        if (v.length<=2*roundlen) bend = 0;
        s += " q " + vecterAdd(r, 0, v, ratio * v.length) + " " +
            vecterAdd(r, -0.5 * bend, v, 0.25 * v.length);
        s += " t " + vecterAdd(r, -0.5 * bend, v, 0.25 * v.length) +
            " " + vecterAdd(r, 0.5 * bend, v, 0.25 * v.length) +
            " " + vecterAdd(r, 0.5 * bend, v, 0.25 * v.length);
        return s;
    }

    function vectorNorm(from, to){
        var v = {
            x : (to[0]-from[0]),
            y : (to[1]-from[1])
        };
        v.length = Math.sqrt( v.x * v.x + v.y * v.y);
        v.x = v.x / v.length;
        v.y = v.y / v.length;
        return v;
    }

    function vecterAdd(v1, u1, v2, u2){
        // return vector: v1 * u1 + v2 * u2
        return (v1.x * u1 + v2.x * u2) + " " + (v1.y * u1 + v2.y * u2);
    }

    function vecterRotate(v, direction){
        // direction == 1 counterclockwise
        if(!direction){
            return { x : v.y, y : -v.x};
        }else {
            return { x : -v.y, y : v.x};
        }
    }

    ConvexHull.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);

                folder.add(this, 'hull_roundlen', 0, 25).step(2)
                    .onFinishChange(function(){_this.display();});

                folder.add(this, 'hull_bend', 0, 15).step(1)
                    .onFinishChange(function(){_this.display();});

                folder.add(this, 'hull_fill_opacity', 0, 1).step(0.1)
                    .onFinishChange(function(){_this.update();});

                folder.add(this, 'hull_color_set')
                    .onFinishChange(function(){_this.update();});

                folder.addColor(this,'hull_fill').onChange(function(){
                    if(!_this.hull_color_set){
                        _this.update();
                    }
                });
            }
        },

        update : {
            value : function(){
                var _this = this;
                this.svg.selectAll('path')
                    .style("fill", function(d, i){
                        if(_this.hull_color_set) {
                            return _this.classColor[_this.cluster_dict[i]];
                        }
                        else return _this.hull_fill;
                    })
                    .style("fill-opacity", _this.hull_fill_opacity);
            }
        },

        display : {
            value : function(){

                this.svg.selectAll('path')
                    .data([])
                    .exit()
                    .remove();

                var _this = this;

                for(var i=0;i<this.cluster_list.length;i++){
                    var cid = this.cluster_list[i];
                    this.svg.append("path")
                        .datum(d3.geom.hull(_this.data[cid]))
                        .attr("d", function(d){
                            var n = d.length;
                            var v = vectorNorm(d[n-1], d[0]);
                            var r = vecterRotate(v, 0);
                            var s = "M " + (_this.hull_roundlen * r.x + d[0][0]) + " " + (_this.hull_roundlen * r.y + d[0][1]);
                            for (var i = 0; i < n; i++){
                                s += segment(d[i], d[(i+1)%n], _this.hull_roundlen, _this.hull_bend, _this.ratio);
                            }
                            s += "Z";
                            return s;
                        });
                }
                this.update();
            }
        }

    });

    return ConvexHull;

}(LG.visual.Visualization);