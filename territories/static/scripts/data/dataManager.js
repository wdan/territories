/**
 * Created by wenbin on 11/3/14.
 */
LG.data.DataManager = function(){

    var DataManager = function(){
        console.log('[LOG] Data manager initialized');
        this.dataName = '';
        this.polygon = {};
        this.constraints = {};
        this.detailed_info = {};
        this.original = {};
        this.width = undefined;
        this.height = undefined;
        this.rate = undefined;
//        this.visibleBoundaryNode = undefined;
//        this.externalBoundaryNode = undefined;
//        this.boundaryEdge = undefined;
//        this.insideNode = undefined;
        this.clusterAttr = {};
        this.max_degree_dict = {};
        this.max_degree = undefined;
        this.overview_max_degree_dict = {};
    };

    Object.defineProperties(DataManager.prototype, {

        getConnection : {
            value : function(src_cluster, tgt_cluster){
                var res = [];
                var n = this.detailed_info.length;
                for(var i=0;i<n;i++){
                    var tmp = this.detailed_info[i];
                    if(tmp['src_cluster'] == src_cluster && tmp['tgt_cluster'] == tgt_cluster){
                        res = res.concat(tmp['points']);
                    }else if(tmp['src_cluster'] == tgt_cluster && tmp['tgt_cluster'] == src_cluster){
                        res = res.concat(tmp['points']);
                    }

                    if(res.length==2)break;
                }
                return res;
            }
        },

        sendMergeRequest : {
            value : function(cluster_list, merge_number){
                var pos = get_poly_pos(this.polygon);
                var _this = this;
                var startTime = new Date().getTime();
                console.log('[POST] /merge_cluster?' + cluster_list + '&' + merge_number);
                $.ajax({
                    url: '/merge_cluster',
                    data: {'cluster_list':cluster_list,'merge_number':merge_number, 'pos':pos},
                    traditional: true,
                    dataType: 'json',
                    type: 'POST',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.polygon = data;
                        console.info('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }

                });
            }
        },

        getDetailed : {
            value : function(){
                var _this = this;
                var startTime = new Date().getTime();
                console.info('[URL] /get_detailed_info');
                $.ajax({
                    url: '/get_detailed_info',
                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.detailed_info = data;
                        console.info('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                        console.debug('[LOG] Calculate maximum degree');
                        _this.max_degree_dict = cal_max_degree(data);
                        var tmp = Object.keys(_this.max_degree_dict)
                            .map(function(key){return _this.max_degree_dict[key];});
                        _this.max_degree = d3.max(tmp);
                    }
                });
            }
        },

        getPolygon : {
            value: function(dataName, width, height, rate){
                var _this = this;
                var startTime = new Date().getTime();

                this.dataName = dataName;
                this.width = width;
                this.height = height;
                if (rate == undefined){this.rate = 1.0;}else{this.rate = rate}

                console.info('[URL] /get_polygon?name=' + this.dataName + '&width=' + this.width + '&height='
                    + this.height + '&rate=' + this.rate);

                $.ajax({
                    url: '/get_polygon?name=' + _this.dataName + '&width=' + _this.width + '&height='
                        + _this.height + '&rate=' + _this.rate,

                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.polygon = data;
                        console.info('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });
            }
        },

        getNewPosition : {
            value : function(exchangeCluster){
                var _this = this;
                var startTime = new Date().getTime();
                console.info('[URL] /select_voronoi?src=' + exchangeCluster[0] + '&tgt=' + exchangeCluster[1]);

                $.ajax({
                    url: '/select_voronoi?src=' + exchangeCluster[0] + '&tgt=' + exchangeCluster[1],

                    dataType:'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.polygon = data;
                        console.info('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });
            }
        },

        getConstraints : {
            value : function(){
                var _this = this;
                var startTime = new Date().getTime();
                console.info('[URL] /get_constraints');
                $.ajax({
                    url: '/get_constraints',
                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.constraints = data;
                        console.info('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                        console.debug('[LOG] Calculate maximum degree');
                        _this.overview_max_degree_dict = cal_max_degree(data);
                    }
                });
            }
        },

        getClusterAttr : {
            value : function(){
                var _this = this;
                var startTime = new Date().getTime();
                console.info('[URL] /get_cluster_attr');
                $.ajax({
                    url: '/get_cluster_attr',
                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.clusterAttr = data;
                        console.info('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });

            }
        }

//        getOriginal : {
//            value : function(){
//                var _this = this;
//                var startTime = new Date().getTime();
//                console.log('[URL] /get_original');
//                $.ajax({
//                    url: '/get_original',
//                    dataType: 'json',
//                    async: false,
//                    success: function(data){
//                        var endTime = new Date().getTime();
//                        _this.original = data;
//                        _this.visibleBoundaryNode = undefined;
//                        _this.externalBoundaryNode = undefined;
//                        _this.boundaryEdge = undefined;
//                        _this.insideNode = undefined;
//                        console.log('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
//                        console.log(data);
//                    }
//                });
//            }
//        },
//
//        getExternalBoundaryNode : {
//
//            value : function(){
//
//                if (this.externalBoundaryNode == undefined){
//                    var node = [];
//                    var node_list = this.original.nodes;
//                    for(var i=0;i<node_list.length;i++){
//                        if(node_list[i]['external'] == 1 && node_list[i].x != undefined) node.push(node_list[i]);
//                    }
//                    this.externalBoundaryNode = node;
//                }
//
//                return this.externalBoundaryNode;
//            }
//
//        },
//
//        getVisibleBoundaryNode : {
//            value : function(){
//                if (this.visibleBoundaryNode == undefined){
//                    var node = [];
//                    var node_list = this.original.nodes;
//                    for(var i=0;i<node_list.length;i++){
//                        if(node_list[i]['external'] == 1 && node_list[i].visible == 1) node.push(node_list[i]);
//                    }
//                    this.visibleBoundaryNode = node;
//                }
//
//                return this.visibleBoundaryNode;
//            }
//        },
//
//        getEdge : {
//            value : function(){
//                if (this.boundaryEdge == undefined){
//                    var edge = [];
//                    var edge_list = this.original.links;
//                    for(var i=0;i<edge_list.length;i++){
//                        if(edge_list[i].visible == 1) edge.push(edge_list[i]);
//                    }
//                    this.boundaryEdge = edge;
//                }
//
//                return this.boundaryEdge;
//            }
//        },
//
//        getInsideNode : {
//            value : function(){
//                if (this.insideNode == undefined){
//                    var node = [];
//                    var node_list = this.original.nodes;
//                    for(var i=0;i<node_list.length;i++){
//                        if(node_list[i]['external'] == 0) node.push(node_list[i]);
//                    }
//                    this.insideNode = node;
//                }
//
//                return this.insideNode;
//            }
//        }

    });

    var get_poly_pos = function(data){

        var n = data.length;
        var res = [];
        for(var i=0;i<n;i++){
            var p = data[i];
            res.push([p['cluster'], p['mid_x'], p['mid_y']])
        }
        return res;
    };

    var cal_max_degree = function(constraints){

        var maxDegree = {};
        var n = constraints.length;
        for(var i=0;i<n;i++){
            var river = constraints[i];
            var points = river['points'];
            var key = river['src_cluster']+'-'+river['tgt_cluster'];
            maxDegree[key] = d3.max(points, function(d){
                return d['in_degree']+d['out_degree'];
            });
        }
        return maxDegree;
    };

    return DataManager;
}();
