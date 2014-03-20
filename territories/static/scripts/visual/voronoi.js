/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.Voronoi = function(Visualization){

    var Voronoi = function(dat, svg, dataManager, sandBox, className){
        console.log('[LOG] Init Voronoi');
        Visualization.call(this, dat, svg, dataManager, sandBox, className);

        // data
        this.data = dataManager.polygon;
        this.clusterName = dataManager.clusterAttr['cluster_name'];
//        this.quality = dataManager.clusterAttr['cluster_quality'];
        this.get_quality();


        // control color
        this.color_set = true;
        this.fill = '#4682B4';
        this.color_scale = d3.scale.linear().domain([0, 1]).range(['white', this.fill]);
        this.opacity = 1.0;

        // control subdivision
        this.subdivision = 0;
        this.scale = 40;

        this.draw_dashed_line = true;
        this.draw_mid_node = false;
        this.draw_label = true;

        this.control();
    };

    Voronoi.prototype = Object.create(Visualization.prototype, {

        get_quality : {
            value : function(){
                var q = this.dataManager.clusterAttr['cluster_quality'];
                console.log(q);
                var tmp = Object.keys(q).map(function(key){return q[key];});
                var max_quality = d3.max(tmp);
                var min_quality = d3.min(tmp);
                var scale = d3.scale.quantize().domain([max_quality, min_quality]).range([0,1,2,3]);
                this.quality = {};
                for(var key in q){
                    if(q.hasOwnProperty(key)){
                        this.quality[key] = scale(q[key]);
                    }
                }
                console.log('quality');
                console.log(this.quality);

            }
        },

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);
                folder.add(this, 'color_set').onFinishChange(function(){
                    _this.update();
                });

                folder.addColor(this, 'fill').onChange(function(){

                    if(!_this.color_set){
                        _this.color_scale = d3.scale.linear().domain([0, 1]).range(['white', _this.fill]);
                        _this.update();
                    }
                });

                folder.add(this, 'opacity', 0, 1).step(0.05).onFinishChange(function(){
                    _this.update();
                });

                folder.add(this, 'subdivision', 0, 10).step(1).onFinishChange(function(){
                   _this.update();
                });

                folder.add(this, 'scale', 0, 100).step(5).onFinishChange(function(value){
                    _this.update();
                    _this.sandBox.updateRiver(value);
                });

                folder.add(this, 'draw_dashed_line').onFinishChange(function(){
                    _this.dashed_line();
                });

                folder.add(this, 'draw_label').onFinishChange(function(){
                    _this.label();
                });

                folder.add(this, 'draw_mid_node').onFinishChange(function(){
                    _this.middle_node();
                });
            }
        },

        merge_data : {
            value : function(data, merge_list, add_id){
                var _this = this;
                this.get_quality();
                this.clusterName = dataManager.clusterAttr['cluster_name'];
                update_add(this.data, data, add_id);
                this.svg.selectAll('.poly')
                    .data(this.data,function(d){
                        return d['cluster'];
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'poly')
                    .attr('selected', 0)
                    .on('click', function(d){
                        d3.select(this)
                            .attr('selected', function(){
                                return 1-d3.select(this).attr('selected');
                            });
                        if(d3.select(this).attr('selected')==1){
                            _this.sandBox.addMergeQueue(d['cluster']);
                        }else{
                            _this.sandBox.removeMergeQueue(d['cluster']);
                        }

                        console.log(_this.sandBox.getMergeQueue());
                        _this.sandBox.addClusterQueue(d['cluster']);
                    })
                    .style('fill-opacity', 0);

                update_remove(this.data, merge_list);

                this.update();

                this.svg.selectAll('.poly')
                    .data(_this.data,function(d){
                        return d['cluster'];
                    })
                    .exit()
                    .transition()
                    .duration(1000)
                    .style('fill-opacity', 0)
                    .remove();

                this.svg.selectAll('.dash')
                    .data(_this.data,function(d){
                        return d['cluster'];
                    })
                    .exit()
                    .transition()
                    .duration(1000)
                    .style('fill-opacity', 0)
                    .remove();

//                this.svg.selectAll('text')

//                this.svg.selectAll('circle')
//                    .transition()
//                    .duration(1500)
//                    .attr('cx', function(d) {return d['mid_x'];})
//                    .attr('cy', function(d) {return d['mid_y'];});
//
//                this.svg.selectAll('text')
//                    .transition()
//                    .duration(1500)
//                    .attr("x", function(d){
//                            return d['mid_x'];
//                    })
//                    .attr("y", function(d){
//                        return d['mid_y'];
//                    });
            }
        },

        update_data : {

            value : function(data){
                var _this = this;
                update_same(this.data, data);
                this.svg.selectAll('.poly')
                    .transition()
                    .duration(1500)
                    .attr('d', function(d){
                        var points = expand(d['points'], {x: d['mid_x'], y:d['mid_y']}, _this.scale);
                        if($.isEmptyObject(_this.quality)){
                            points = subdivision_k(points, _this.subdivision);
                        }
                        else{
                            points = subdivision_k(points, _this.quality[d['cluster']]);
                        }

                        var s = 'M ' + points[0].x + ' ' + points[0].y;
                        for(var j=1;j< points.length;j++){
                            s += ' L ' + points[j].x + ' ' + points[j].y;
                        }
                        s += 'Z';
                        return s;
                    });

//                this.svg.selectAll('circle')
//                    .transition()
//                    .duration(1500)
//                    .attr('cx', function(d) {return d['mid_x'];})
//                    .attr('cy', function(d) {return d['mid_y'];});

                this.svg.selectAll('text')
                    .transition()
                    .duration(1500)
                    .attr("x", function(d){
                        return d['mid_x'];
                    })
                    .attr("y", function(d){
                        return d['mid_y'];
                    });

                this.svg.selectAll('.dash')
                    .transition()
                    .duration(1500)
                    .attr('d', function(d){
                        var points = d['points'];
                        var mid = {x: d['mid_x'], y:d['mid_y']};
                        var s = '';
                        var n = points.length;
                        for(var i=0;i<n;i++){
                            s += 'M ' + mid.x + ' ' + mid.y;
                            s += 'L ' + points[i].x + " " + points[i].y;
                            s += 'L ' + points[(i+1)%n].x + " " + points[(i+1)%n].y;
                        }
                        return s;
                    });
            }
        },

        update : {
            value : function(){
                var _this = this;
                this.svg.selectAll('.poly')
                    .transition()
                    .duration(1000)
                    .attr('d', function(d){
                        var points = expand(d['points'], {x: d['mid_x'], y:d['mid_y']}, _this.scale);
                        if($.isEmptyObject(_this.quality)){
                            points = subdivision_k(points, _this.subdivision);
                        }
                        else{
                            points = subdivision_k(points, _this.quality[d['cluster']]);
                            if(_this.quality[d['cluster']]==undefined)console.log('WRRRRRRR!!!!!');
                        }

                        var s = 'M ' + points[0].x + ' ' + points[0].y;
                        for(var j=1;j< points.length;j++){
                            s += ' L ' + points[j].x + ' ' + points[j].y;
                        }
                        s += 'Z';
                        return s;
                    })
                    .style('fill', function(d){
                        if (_this.color_set) return _this.classColor[d.cluster];
                        else{
                            var c = Math.random();
                            return _this.color_scale(c);
                        }
                    })
                    .style('fill-opacity', _this.opacity);
                this.dashed_line();
                this.label();
            }
        },

        middle_node :{
            value : function(){
                if(this.draw_mid_node){
                    this.svg.selectAll('circle')
                        .data(this.data, function(d){
                            return d['cluster'];
                        })
                        .enter()
                        .append('circle')
                        .attr('r', 5)
                        .attr('cx', function(d) {return d['mid_x'];})
                        .attr('cy', function(d) {return d['mid_y'];})
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

        label : {
            value : function(){

                this.svg.selectAll('text')
                        .data([])
                        .exit()
                        .remove();

                if(this.draw_label){
                    var _this = this;
                    this.svg.selectAll('text')
                        .data(this.data, function(d){
                            return d['cluster'];
                        })
                        .enter()
                        .append('text')
                        .text(function(d){
                            console.log(_this.clusterName[d.cluster]);
                            return _this.clusterName[d.cluster];
                        })
                        .attr('text-anchor', 'middle')
                        .attr("x", function(d){
                            return d['mid_x'];
                        })
                        .attr("y", function(d){
                            return d['mid_y'];
                        });
                }
            }
        },

        dashed_line : {
            value : function(){
                this.svg.selectAll('.dash')
                        .data([])
                        .exit()
                        .remove();

                if(this.draw_dashed_line){
                    this.svg.selectAll('.dash')
                        .data(this.data, function(d){
                            return d['cluster'];
                        })
                        .enter()
                        .append('path')
                        .attr('class', 'dash')
                        .attr('d', function(d){
                            var points = d['points'];
                            var mid = {x: d['mid_x'], y:d['mid_y']};
                            var s = '';
                            var n = points.length;
                            for(var i=0;i<n;i++){
                                s += 'M ' + mid.x + ' ' + mid.y;
                                s += 'L ' + points[i].x + " " + points[i].y;
                                s += 'L ' + points[(i+1)%n].x + " " + points[(i+1)%n].y;
                            }
                            return s;
                        })
                        .style('stroke-dasharray', '5,5')
                        .style('fill', 'none')
                        .style('stroke', 'gray')
                        .style('stroke-width', '1')
                        .style('stroke-opacity', 0.5);
                }
            }
        },

        display : {
            value : function(){

                this.svg.selectAll('.poly')
                    .data([])
                    .exit()
                    .remove();

                var _this = this;
                this.svg.selectAll('.poly')
                    .data(this.data, function(d){
                        return d['cluster'];
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'poly')
                    .attr('selected', 0)
                    .on('click', function(d){
                        d3.select(this)
                            .attr('selected', function(){
                                return 1-d3.select(this).attr('selected');
                            });
                        if(d3.select(this).attr('selected')==1){
                            _this.sandBox.addMergeQueue(d['cluster']);
                        }else{
                            _this.sandBox.removeMergeQueue(d['cluster']);
                        }

                        console.log(_this.sandBox.getMergeQueue());
                        _this.sandBox.addClusterQueue(d['cluster']);
                    })
                    .attr('d', function(d){
                        var n = d['points'].length;
                        var s = 'M'+ d['mid_x'] + ' ' + d['mid_y'];
                        for(var i=1;i<n;i++){
                            s += 'L'+ d['mid_x'] + ' ' + d['mid_y'];
                        }
                        return s;
                    })
                    .style('fill', function(d){
                        if (_this.color_set) return _this.classColor[d.cluster];
                        else{
                            var c = Math.random();
                            return _this.color_scale(c);
                        }
                    })
                    .style('fill-opacity', _this.opacity);
                this.update();
            }
        }
    });

    var update_add = function(data, poly, add_id){
        var n = poly.length;
        var dict = {};
        var add_index;
        for(var i=0;i<n;i++){
            var p = poly[i];
            if(p['cluster'] == add_id) add_index = i;
            dict[p['cluster']] = i;
        }

        var m = data.length;
        for(i=0;i<m;i++){
            var cluster = data[i]['cluster'];
            if(cluster in dict){
                data[i]['height'] = poly[dict[cluster]]['height'];
                data[i]['width'] = poly[dict[cluster]]['width'];
                data[i]['mid_x'] = poly[dict[cluster]]['mid_x'];
                data[i]['mid_y'] = poly[dict[cluster]]['mid_y'];
                data[i]['points'] = poly[dict[cluster]]['points'];
                delete dict[cluster];
            }
        }
        data.push(poly[add_index]);
    };

    var update_remove = function(data, merge_list){
        var n = data.length;
        var remove_list = [];
        for(var i=0;i<n;i++){
            for(var j=0;j<merge_list.length;j++){
                if(data[i]['cluster'] == merge_list[j])remove_list.push(i);
            }

        }

        for(i=0;i<remove_list.length;i++){
            data.splice(remove_list[i]-i, 1);
        }
    };

    var update_same = function(data, poly){

        var n = poly.length;
        var dict = {};
        for(var i=0;i<n;i++){
            var p = poly[i];
            dict[p['cluster']] = i;
        }

        for(i=0;i<n;i++){
            var cluster = data[i]['cluster'];
            data[i]['height'] = poly[dict[cluster]]['height'];
            data[i]['width'] = poly[dict[cluster]]['width'];
            data[i]['mid_x'] = poly[dict[cluster]]['mid_x'];
            data[i]['mid_y'] = poly[dict[cluster]]['mid_y'];
            data[i]['points'] = poly[dict[cluster]]['points'];
        }
    };

    var subdivision_k = function(points, k){

        for(var i=0;i<k;i++){
            points = subdivision_one(points);
        }
        return points;
    };

    var subdivision_one = function(points){

        var n = points.length;
        var mid = [];
        var res = [];
        for(var i=0;i<n;i++){
            mid.push({x:(points[i].x+points[(i+1)%n].x)/2,y:(points[i].y+points[(i+1)%n].y)/2});
        }
        for(i=0;i<n;i++){
            res.push({x:(points[i].x+mid[i].x)/2, y:(points[i].y+mid[i].y)/2});
            res.push({x:(points[(i+1)%n].x+mid[i].x)/2, y:(points[(i+1)%n].y+mid[i].y)/2});
        }
        return res;
    };

    // helper function
    var vectorNorm = function(from, to){
        var v = {
            x : to.x - from.x,
            y : to.y - from.y
        };
        v.length = Math.sqrt( v.x * v.x + v.y * v.y);
        v.x = v.x / v.length;
        v.y = v.y / v.length;
        return v;
    };

    var interp = function (center, point, scale){
        var v = vectorNorm(center, point);
        var k = (v.length - scale) / v.length;
        return{
            x : ( k * v.length * v.x + center.x),
            y : ( k * v.length * v.y + center.y)
        };
    };

    var expand = function(d, mid, scale){
        var res = [];
        for(var i=0;i< d.length;i++){
            res.push(interp(mid, d[i], scale));
        }
        return res;
    };

    return Voronoi;
}(LG.visual.Visualization);
