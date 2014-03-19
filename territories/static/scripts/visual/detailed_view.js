/**
 * Created by wenbin on 19/3/14.
 */

LG.visual.DetailedView = function(Visualization){
    var DetailedView = function(dat, svg, dataManager, sandBox, className){
        console.log('[LOG] Init Detailed View');
        Visualization.call(this, dat, svg, dataManager, sandBox, className);
        this.padding = 10;
        this.cluster_margin = 15;
        this.opacity = 0.5;
        this.degree_scale = 1;// global
        this.scale_type = 1;// log
        this.control();
        this.view_list = [];
        this.state_list = [];
        this.width = 250;
        this.height = 120;
        this.MAX_VIEWS = Math.ceil(600/this.height);
    };

    DetailedView.prototype = Object.create(Visualization.prototype, {

        control : {
            value : function(){
                var _this = this;
                var folder = this.dat.addFolder(this.className);
                folder.add(this, 'padding', 0, 20).step(1).onFinishChange(function(){
                    _this.update();
                });
                folder.add(this, 'opacity', 0, 1).step(0.05).onFinishChange(function(){
                    _this.update();
                });
                folder.add(this, 'degree_scale', {Global:1, Local:2}).onFinishChange(function(){
                    _this.update();
                });
                folder.add(this, 'scale_type', {log:1, linear:2}).onFinishChange(function(){
                    _this.update();
                })
            }
        },

        add : {
            value : function(){
                var src_id = this.sandBox.exchangeCluster[0];
                var tgt_id = this.sandBox.exchangeCluster[1];
                var data = dataManager.getConnection(src_id, tgt_id);
                if(data.length==0)return;
                var state = {
                    x:0,
                    y:-this.height,
                    src_id: src_id,
                    tgt_id: tgt_id,
                    active: 'both'
                };
                var g = this.svg.append('g')
                    .data([state])
                    .attr('width', this.width)
                    .attr('height', this.height)
                    .attr('id', 'detailed_'+src_id+'_'+tgt_id)
                    .attr("transform", function(d){
                        return "translate(" + d.x + "," + d.y + ")";
                    });

                this.display(data, g, src_id, tgt_id);
                this.state_list.push(state);
                this.view_list.push(g);
                for(var i=0;i<this.state_list.length;i++){
                    var tmp = this.state_list[i];
                    tmp['y'] = tmp['y'] + this.height;
                    this.view_list[i]
                        .transition()
                        .duration(1000)
                        .attr("transform", function(d){
                            return "translate(" + d.x + "," + d.y + ")";
                        });
                }

                if(this.state_list.length>this.MAX_VIEWS+1){
                    this.view_list.shift().data([]).exit().remove();
                    this.state_list.shift();
                }

            }
        },

        update : {
            value : function(){
                for(var i=0;i<this.view_list.length;i++){
                    var g = this.view_list[i];
                    var src_id = this.state_list[i]['src_id'];
                    var tgt_id = this.state_list[i]['tgt_id'];

                    var _this = this;
                    var max_degree;
                    if(this.degree_scale==1){
                        max_degree = this.dataManager.max_degree;
                    }
                    else if(this.degree_scale==2){
                        var m1 = this.dataManager.max_degree_dict[src_id+'-'+tgt_id];
                        var m2 = this.dataManager.max_degree_dict[tgt_id+'-'+src_id];
                        max_degree = Math.max(m1, m2);
                    }
                    var degree_scale = d3.scale.linear().domain([0, max_degree]).range([2, 10]);

                    var x_scale;
                    if(this.scale_type==1){
                        x_scale = d3.scale.log().domain([1/max_degree, 1])
                            .range([_this.padding, _this.width/2]);
                    }else if(this.scale_type==2){
                        x_scale = d3.scale.linear().domain([1/max_degree, 1])
                            .range([_this.padding, _this.width/2]);
                    }

                    var y_scale = d3.scale.linear().domain([0, 1])
                        .range([_this.height - _this.padding - _this.cluster_margin,_this.height/2]);

                    g.selectAll('circle')
                        .transition()
                        .duration(1000)
                        .attr('r', function(d){
                            return degree_scale(d['in_degree']+d['out_degree']);
                        })
                        .attr('cx', function(d){
                            if(d['cluster']== src_id){
                                return x_scale((d['in_degree']+d['out_degree'])/max_degree);
                            }else{
                                return _this.width - x_scale((d['in_degree']+d['out_degree'])/max_degree);
                            }
                        })
                        .attr('cy', function(d){
                            if(d['cluster']== src_id){
                                if(d['in_degree']>=d['out_degree']){
                                    return y_scale(d['out_degree']/d['in_degree']);
                                }else{
                                    return _this.height - y_scale(d['in_degree']/d['out_degree']);
                                }
                            }else{
                                if(d['in_degree']>=d['out_degree']){
                                    return _this.height - y_scale(d['out_degree']/d['in_degree']);
                                }else{
                                    return y_scale(d['in_degree']/d['out_degree']);
                                }
                            }

                        })
                        .style('opacity', this.opacity);
                }
            }
        },

        display : {
            value : function(data, g, src_id, tgt_id){

                var _this = this;
                var max_degree;
                if(this.degree_scale==1){
                    max_degree = this.dataManager.max_degree;
                }
                else if(this.degree_scale==2){
                    var m1 = this.dataManager.max_degree_dict[src_id+'-'+tgt_id];
                    var m2 = this.dataManager.max_degree_dict[tgt_id+'-'+src_id];
                    max_degree = Math.max(m1, m2);
                }
                var degree_scale = d3.scale.linear().domain([0, max_degree]).range([3,10]);

                var x_scale;
                if(this.scale_type==1){
                    x_scale = d3.scale.log().domain([0.01, 1])
                        .range([_this.padding, _this.width/2]);
                }else if(this.scale_type==2){
                    x_scale = d3.scale.linear().domain([0.01, 1])
                        .range([_this.padding, _this.width/2]);
                }

                var y_scale = d3.scale.linear().domain([0, 1])
                    .range([_this.height - _this.padding - _this.cluster_margin,_this.height/2]);

                g.selectAll('circle')
                    .data(data)
                    .enter()
                    .append('circle')
                    .attr('class', function(d){
                        if(d['cluster']==src_id){
                            return 'src';
                        }else{
                            return 'tgt';
                        }
                    })
                    .attr('r', function(d){
                        return degree_scale(d['in_degree']+d['out_degree']);
                    })
                    .attr('cx', function(d){
                        if(d['cluster']== src_id){
                            return x_scale((d['in_degree']+d['out_degree'])/max_degree);
                        }else{

                            return _this.width - x_scale((d['in_degree']+d['out_degree'])/max_degree);
                        }
                    })
                    .attr('cy', function(d){
                        if(d['cluster']== src_id){
                            if(d['in_degree']>=d['out_degree']){
                                return y_scale(d['out_degree']/d['in_degree']);
                            }else{
                                return _this.height - y_scale(d['in_degree']/d['out_degree']);
                            }
                        }else{
                            if(d['in_degree']>=d['out_degree']){
                                return _this.height - y_scale(d['out_degree']/d['in_degree']);
                            }else{
                                return y_scale(d['in_degree']/d['out_degree']);
                            }
                        }

                    })
                    .style('fill', function(d){
                        return _this.classColor[d['cluster']];
                    })
                    .style('opacity', this.opacity)
                    .on('click', function(d){
                        console.log(d['label']);
                        console.log(d['in_degree']+':'+d['out_degree']);
                    });

                g.append('path')
                    .attr('d', function(){
                        return 'M ' + _this.padding + ' ' + _this.height/2 +
                            'L ' + (_this.width - _this.padding) + ' ' + _this.height/2;
                    })
                    .style('stroke-dasharray', '5,5')
                    .style('fill', 'none')
                    .style('stroke', 'gray')
                    .style('stroke-width', '1')
                    .style('stroke-opacity', 0.5);

                g.append('path')
                    .attr('d', function(){
                        return 'M ' + _this.width/2 + ' ' + (_this.cluster_margin + _this.padding)
                        +' L' + _this.width/2 + ' ' + (_this.height - _this.cluster_margin - _this.padding);
                    })
                    .style('stroke-dasharray', '5,5')
                    .style('fill', 'none')
                    .style('stroke', 'gray')
                    .style('stroke-width', '1')
                    .style('stroke-opacity', 0.5);

                g.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', _this.width)
                    .attr('height', _this.cluster_margin)
                    .style('fill', _this.classColor[tgt_id])
                    .on("dblclick", function(){
                        var state;
                        d3.select(this.parentNode).each(function(d){
                            if(d['active'] == 'both'){
                                d['active'] = 'target';
                            }else {
                                d['active'] = 'both';
                            }
                            state = d['active'];
                        });
                        d3.select(this.parentNode).selectAll('.tgt')
                            .each(function(){
                                var pre_cx = _this.width - _this.padding - d3.select(this).attr('cx');
                                if(state=='both'){
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .attr('cx', _this.width - _this.padding - pre_cx/2);
                                }else if(state=='target'){
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .attr('cx', _this.width - _this.padding - pre_cx*2)
                                        .style('opacity', _this.opacity);
                                }else{
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .attr('cx', _this.width - _this.padding - pre_cx*2)
                                        .style('opacity', 0);
                                }
                            });
                        d3.select(this.parentNode).selectAll('.src')
                            .each(function(){
                                if(state=='both'){
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .style('opacity', _this.opacity);
                                }else{
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .style('opacity', 0);
                                }
                            });
                    });

                g.append('rect')
                    .attr('x', 0)
                    .attr('y', _this.height - _this.cluster_margin)
                    .attr('width', _this.width)
                    .attr('height', _this.cluster_margin)
                    .style('fill', _this.classColor[src_id])
                    .on('dblclick', function(){
                        var state;
                        d3.select(this.parentNode).each(function(d){
                            if(d['active'] == 'both'){
                                d['active'] = 'source';
                            }else {
                                d['active'] = 'both';
                            }
                            state = d['active'];
                        });
                        d3.select(this.parentNode).selectAll('.src')
                            .each(function(){
                                var pre_cx = d3.select(this).attr('cx') - _this.padding;
                                if(state=='both'){
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .attr('cx', _this.padding + pre_cx/2);
                                }else if(state=='source'){
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .attr('cx', _this.padding + pre_cx*2)
                                        .style('opacity', _this.opacity);
                                }else{
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .attr('cx', _this.padding + pre_cx*2)
                                        .style('opacity', 0);
                                }
                            });
                        d3.select(this.parentNode).selectAll('.tgt')
                            .each(function(){
                                if(state=='both'){
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .style('opacity', _this.opacity);
                                }else{
                                    d3.select(this)
                                        .transition()
                                        .duration(1000)
                                        .style('opacity', 0);
                                }
                            });
                    });
        }

        }
    });

    return DetailedView;
}(LG.visual.Visualization);