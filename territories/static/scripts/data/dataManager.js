/**
 * Created by wenbin on 11/3/14.
 */
LG.data.DataManager = function(){

    var DataManager = function(){
        console.log('[LOG] Data manager initialized');
        this.dataName = '';
        this.polygon = {};
        this.constraints = {};
        this.original = {};
        this.width = undefined;
        this.height = undefined;
        this.rate = undefined;
        this.visibleBoundaryNode = undefined;
        this.externalBoundaryNode = undefined;
        this.boundaryEdge = undefined;
        this.insideNode = undefined;
        this.clusterAttr = {};
    };

    Object.defineProperties(DataManager.prototype, {
        getPolygon : {
            value: function(dataName, width, height, rate){
                var _this = this;
                var startTime = new Date().getTime();

                this.dataName = dataName;
                this.width = width;
                this.height = height;
                if (rate == undefined){this.rate = 1.0;}else{this.rate = rate}

                console.log('[URL] /get_polygon?name=' + this.dataName + '&width=' + this.width + '&height='
                    + this.height + '&rate=' + this.rate);

                $.ajax({
                    url: '/get_polygon?name=' + _this.dataName + '&width=' + _this.width + '&height='
                        + _this.height + '&rate=' + _this.rate,

                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.polygon = data;
                        console.log('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });
            }
        },

        getNewPosition : {
            value : function(exchangeCluster){
                var _this = this;
                var startTime = new Date().getTime();
                console.log('[LOG] Get New Position');
                console.log('[URL] /select_voronoi?src=' + exchangeCluster[0] + '&tgt=' + exchangeCluster[1]);

                $.ajax({
                    url: '/select_voronoi?src=' + exchangeCluster[0] + '&tgt=' + exchangeCluster[1],

                    dataType:'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.polygon = data;
                        console.log('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });
            }
        },

        getConstraints : {
            value : function(){
                var _this = this;
                var startTime = new Date().getTime();
                console.log('[LOG] Get Constraints');
                console.log('[URL] /get_constraints');
                $.ajax({
                    url: '/get_constraints',
                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.constraints = data;
                        console.log('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });
            }
        },

        getClusterAttr : {
            value : function(){
                var _this = this;
                var startTime = new Date().getTime();
                console.log('[URL] /get_cluster_attr');
                $.ajax({
                    url: '/get_cluster_attr',
                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.clusterAttr = data;
                        console.log('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });

            }
        },

        getOriginal : {
            value : function(){
                var _this = this;
                var startTime = new Date().getTime();
                console.log('[URL] /get_original');
                $.ajax({
                    url: '/get_original',
                    dataType: 'json',
                    async: false,
                    success: function(data){
                        var endTime = new Date().getTime();
                        _this.original = data;
                        _this.visibleBoundaryNode = undefined;
                        _this.externalBoundaryNode = undefined;
                        _this.boundaryEdge = undefined;
                        _this.insideNode = undefined;
                        console.log('[LOG] Data Transmission Done. Used ' + (endTime-startTime)/1000 + 's');
                        console.log(data);
                    }
                });
            }
        },

        getExternalBoundaryNode : {

            value : function(){

                if (this.externalBoundaryNode == undefined){
                    var node = [];
                    var node_list = this.original.nodes;
                    for(var i=0;i<node_list.length;i++){
                        if(node_list[i]['external'] == 1 && node_list[i].x != undefined) node.push(node_list[i]);
                    }
                    this.externalBoundaryNode = node;
                }

                return this.externalBoundaryNode;
            }

        },

        getVisibleBoundaryNode : {
            value : function(){
                if (this.visibleBoundaryNode == undefined){
                    var node = [];
                    var node_list = this.original.nodes;
                    for(var i=0;i<node_list.length;i++){
                        if(node_list[i]['external'] == 1 && node_list[i].visible == 1) node.push(node_list[i]);
                    }
                    this.visibleBoundaryNode = node;
                }

                return this.visibleBoundaryNode;
            }
        },

        getEdge : {
            value : function(){
                if (this.boundaryEdge == undefined){
                    var edge = [];
                    var edge_list = this.original.links;
                    for(var i=0;i<edge_list.length;i++){
                        if(edge_list[i].visible == 1) edge.push(edge_list[i]);
                    }
                    this.boundaryEdge = edge;
                }

                return this.boundaryEdge;
            }
        },

        getInsideNode : {
            value : function(){
                if (this.insideNode == undefined){
                    var node = [];
                    var node_list = this.original.nodes;
                    for(var i=0;i<node_list.length;i++){
                        if(node_list[i]['external'] == 0) node.push(node_list[i]);
                    }
                    this.insideNode = node;
                }

                return this.insideNode;
            }
        }

    });

    return DataManager;
}();