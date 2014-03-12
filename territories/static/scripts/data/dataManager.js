/**
 * Created by wenbin on 11/3/14.
 */
LG.data.DataManager = function(){

    var DataManager = function(){
        console.log('[LOG] Data manager initialized');
        this.dataName = '';
        this.polygon = {};
        this.original = {};
        this.width = undefined;
        this.height = undefined;
        this.shrink = undefined;
        this.rate = undefined;
        this.visibleBoundaryNode = undefined;
        this.externalBoundaryNode = undefined;
        this.boundaryEdge = undefined;
    };

    Object.defineProperties(DataManager.prototype, {
        getPolygon : {
            value: function(dataName, width, height, shrink, rate){
                var _this = this;
                this.dataName = dataName;
                this.width = width;
                this.height = height;
                if (shrink == undefined){this.shrink = 50;}else{this.shrink = shrink;}
                if (rate == undefined){this.rate = 1.0;}else{this.rate = rate}

                console.log('[LOG] Get Polygon Data : ' + this.dataName);
                console.log('[URL] /get_polygon?name=' + this.dataName + '&width=' + this.width + '&height='
                    + this.height + '&shrink=' + this.shrink + '&rate=' + this.rate);

                $.ajax({
                    url: '/get_polygon?name=' + _this.dataName + '&width=' + _this.width + '&height='
                        + _this.height + '&shrink=' + _this.shrink + '&rate=' + _this.rate,

                    dataType: 'json',
                    async: false,
                    success: function(data){
                        _this.polygon = data;
                        console.log('[LOG] Data Transmission Done.');
                        console.log(data);
                    }
                });
            }
        },

        getOriginal : {
            value : function(){
                var _this = this;

                console.log('[LOG] Get Original Data.');
                console.log('[URL] /get_original');

                $.ajax({
                    url: '/get_original',
                    dataType: 'json',
                    async: false,
                    success: function(data){
                        _this.original = data;
                        _this.visibleBoundaryNode = undefined;
                        _this.externalBoundaryNode = undefined;
                        _this.boundaryEdge = undefined;
                        console.log('[LOG] Data Transmission Done.');
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
                        if(node_list[i].external == 1) node.push(node_list[i]);
                    }
                    this.externalBoundaryNode = node;
                }

                console.log('external nodes');
                console.log(this.externalBoundaryNode);
                return this.externalBoundaryNode;


            }

        },

        getVisibleBoundaryNode : {
            value : function(){
                if (this.visibleBoundaryNode == undefined){
                    var node = [];
                    var node_list = this.original.nodes;
                    for(var i=0;i<node_list.length;i++){
                        if(node_list[i].external == 1 && node_list[i].visible == 1) node.push(node_list[i]);
                    }
                    this.visibleBoundaryNode = node;
                }


                console.log('visible nodes');
                console.log(this.visibleBoundaryNode);
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
        }

    });

    return DataManager;
}();