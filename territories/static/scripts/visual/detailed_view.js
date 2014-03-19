/**
 * Created by wenbin on 19/3/14.
 */

LG.visual.DetailedView = function(Visualization){
    var DetailedView = function(dat, svg, dataManager, sandBox, className){
        console.log('[LOG] Init Detailed View');
        Visualization.call(this, dat, svg, dataManager, sandBox, className);
        this.padding = 10;
        this.cluster_margin = 15;
        this.control();
        this.view_list = [];
        this.pos_list = [];
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
            }
        },

        add : {
            value : function(){
                var src_id = this.sandBox.exchangeCluster[0];
                var tgt_id = this.sandBox.exchangeCluster[1];
                var data = dataManager.getConnection(src_id, tgt_id);
                if(data.length==0)return;
                var pos = {x:0, y:-this.height};
                var g = this.svg.append('g')
                    .data([pos])
                    .attr('width', this.width)
                    .attr('height', this.height)
                    .attr("transform", function(d){
                        return "translate(" + d.x + "," + d.y + ")";
                    });
                this.display(data, g, src_id, tgt_id);
                this.pos_list.push(pos);
                this.view_list.push(g);
                for(var i=0;i<this.pos_list.length;i++){
                    var tmp = this.pos_list[i];
                    tmp['y'] = tmp['y'] + this.height;
                    this.view_list[i]
                        .transition()
                        .duration(1000)
                        .attr("transform", function(d){
                            return "translate(" + d.x + "," + d.y + ")";
                        });
                }

                if(this.pos_list.length>this.MAX_VIEWS+1){
                    this.view_list.shift()
                        .data([])
                        .exit()
                        .remove();
                    this.pos_list.shift();
                }

            }
        },

        get_data : {
            value : function(){
                this.src_id = sandBox.exchangeCluster[0];
                this.tgt_id = sandBox.exchangeCluster[1];
                this.data = dataManager.getConnection(this.src_id, this.tgt_id);
            }
        },

        display : {
            value : function(data, g, src_id, tgt_id){

                var _this = this;

                var max_degree = d3.max(data, function(d){
                    return d['in_degree'] + d['out_degree'];
                });

                var degree_scale = d3.scale.linear().domain([0, max_degree]).range([2,10]);
                var x_scale = d3.scale.linear().domain([0, 1])
                    .range([_this.padding, _this.width/2]);
                var y_scale = d3.scale.linear().domain([0, 1])
                    .range([_this.height - _this.padding - _this.cluster_margin,_this.height/2]);

                g.selectAll('circle')
                    .data(data)
                    .enter()
                    .append('circle')
                    .style('fill', 0)
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
                    .style('opacity', 1);

                g.selectAll('circle')
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
                    .style('fill', _this.classColor[tgt_id]);

                g.append('rect')
                    .attr('x', 0)
                    .attr('y', _this.height - _this.cluster_margin)
                    .attr('width', _this.width)
                    .attr('height', _this.cluster_margin)
                    .style('fill', _this.classColor[src_id]);
        }

        }
    });

    return DetailedView;
}(LG.visual.Visualization);