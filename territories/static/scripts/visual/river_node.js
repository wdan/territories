/**
 * Created by wenbin on 16/3/14.
 */

LG.visual.RiverNode = function(Visualization){
    var RiverNode = function(dat, svg, dataManager, sandBox, className){
        console.log('[LOG] Init River Node');
        Visualization.call(this, dat, svg, dataManager, sandBox, className);
        this.data = dataManager.constraints;
        this.r = 2;
        this.opacity = 0.5;
        this.scale = 40;
        this.x_margin = 0.85;
        this.y_margin = 0.85;
        this.control();
    };

    RiverNode.prototype = Object.create(Visualization.prototype, {
        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);
                folder.add(this, 'r', 0, 10).step(1).onFinishChange(function(){
                    _this.update();
                });
                folder.add(this, 'opacity', 0, 1).step(0.05).onFinishChange(function(){
                   _this.update();
                });
                folder.add(this, 'x_margin', 0, 1).step(0.01).onFinishChange(function(){
                    _this.display();
                });
                folder.add(this, 'y_margin', 0, 1).step(0.01).onFinishChange(function(){
                    _this.display();
                });
            }
        },

        display : {
            value : function(){
                this.svg.selectAll('circle')
                    .data([])
                    .exit()
                    .remove();
                var n = this.data.length;

                for(var i=0; i<n; i++){

                    var river = this.data[i];
                    var points = this.data[i]['points'];
                    var src = {x:river['src_cluster_x'], y:river['src_cluster_y']};
                    var tgt = {x:river['tgt_cluster_x'], y:river['tgt_cluster_y']};
                    var p1 = {x:river['x1'], y:river['y1']};
                    var p2 = {x:river['x2'], y:river['y2']};
                    var base = collapse(src, tgt, p1, p2, this.y_margin);
                    var max_degree = d3.max(points, function(d){return d['in_degree'] + d['out_degree']});

                    for(var j=0;j<points.length;j++){
                        var p = points[j];
                        var pos = layout(src, tgt, base, this.scale * this.x_margin, p, max_degree);
                        p['x'] = pos.x;
                        p['y'] = pos.y;
                    }

                    var degree_scale = d3.scale.linear().domain([0, max_degree]).range([2, 10]);
                    this.svg.append('g')
                        .attr('id', river['src_cluster'] + '-' + river['tgt_cluster'])
                        .selectAll('circle')
                        .data(points)
                        .enter()
                        .append('circle')
                        .attr('r', function(d){
                            return degree_scale(d['in_degree']+d['out_degree']);
                        })
                        .attr('cx', function(d){
                            return d.x;
                        })
                        .attr('cy', function(d){
                            return d.y;
                        })
                        .style('fill', this.classColor[river['src_cluster']])
                        .on('click', function(d){
                            console.log(d['label']);
                            console.log(d['in_degree']+':'+d['out_degree']);
                        });
                    this.update();
                }
            }
        },

        update_scale : {
            value : function(scale){
                this.scale = scale;
                this.display();
            }
        },

        update : {
            value : function(){
                this.svg.selectAll('circle')
//                    .attr('r', this.r)
                    .style('opacity', this.opacity);
            }
        }
    });

     var collapse = function(src, tgt, p1, p2, margin){
        var point1 = {}, point2 = {};
        var right = {
            x: tgt.y - src.y,
            y: -(tgt.x - src.x)
        };

        var src2p1 = {
            x : p1.x - src.x,
            y : p1.y - src.y
        };

        if(right.x*src2p1.x + right.y*src2p1.y > 0){
            point1 = p1;
            point2 = p2;
        }else{
            point1 = p2;
            point2 = p1;
        }

        var tmp = (1-margin) / 2;
        return {
            start : vector_scale(point1, point2, tmp),
            end : vector_scale(point1, point2, 1-tmp)
        }
    };

    var layout = function(src, tgt, base, margin, p, max_degree){
        var scale = d3.scale.linear().domain([0, 1]).range([margin, 0]);
        var origin = {}, degree_rate = 0;
        if(p['out_degree']<=p['in_degree']){
            origin = src;
            degree_rate = p['out_degree']/p['in_degree'];
        }else{
            origin = tgt;
            degree_rate = p['in_degree']/p['out_degree'];
        }
        var p1 = vector_len(origin, base.start, scale(degree_rate));
        var p2 = vector_len(origin, base.end, scale(degree_rate));
//        var degree_scale;
//        if(Math.random()>0.5) degree_scale = 0.5 * (2 - (p['out_degree'] + p['in_degree'])/max_degree);
//        else degree_scale = 0.5 * ((p['out_degree'] + p['in_degree'])/max_degree);

        var degree_scale = 0.45 * ((p['out_degree'] + p['in_degree'])/max_degree);
        return vector_scale(p1, p2, degree_scale);

    };

    var vector_scale = function(from, to, scale){
        var v = vector_norm(from, to);
        var new_len = v.length * scale;
        return {
            x : from.x + new_len * v.x,
            y : from.y + new_len * v.y
        };
    };

    var vector_len = function(from, to, len){
        var v = vector_norm(from, to);
        var new_len = v.length - len;
        return {
            x : from.x + new_len * v.x,
            y : from.y + new_len * v.y
        };

    };

    var vector_norm = function(from, to){
        var v = {
            x : to.x - from.x,
            y : to.y - from.y
        };
        v.length = Math.sqrt( v.x * v.x + v.y * v.y);
        v.x = v.x / v.length;
        v.y = v.y / v.length;
        return v;
    };

    return RiverNode;

}(LG.visual.Visualization);