/**
 * Created by wenbin on 16/3/14.
 */

LG.control.SandBox = function(){

    var SandBox = function(){
        console.log('[LOG] SandBox initialized');
        this.module = {};
        this.exchangeCluster = [];
        this.mergeCluster = {};
    };

    Object.defineProperties(SandBox.prototype, {

        add : {
            value : function(className, obj){
                this.module[className] = obj;
            }
        },

        update_data : {
            value : function(className, data){
                if(className in this.module){
                    this.module[className].update_data(data);
                }
            }
        },

        merge_data : {
            value : function(className, data, merge_list, add_id){
                if(className in this.module){
                    this.module[className].merge_data(data, merge_list, add_id);
                }
            }
        },

        update_exchange : {
            value : function(polygon){

                if('voronoi' in this.module){
                    this.module['voronoi'].update_data(polygon);
                }
            }
        },

//        updateAll : {
//            value : function(){
//                for(var key in this.module){
//                    if(this.module.hasOwnProperty(key)){
//                        this.module[key].update();
//                    }
//                }
//            }
//        },

        remove : {
            value : function(className){
                if(className in this.module){
                    delete this.module[className];
                }
            }
        },

        updateRiver : {
            value : function(data){
                var target_obj = this.module['river_node'];
                if(target_obj instanceof LG.visual.RiverNode){
                    target_obj.update_scale(data);
                }
            }
        },

        addClusterQueue : {
            value : function(data){
                if(this.exchangeCluster.length!=1){
                    this.exchangeCluster.shift();
                }
                this.exchangeCluster.push(data);
            }
        },

        clearClusterQueue : {
            value : function(){
                this.exchangeCluster = [];
            }
        },

        addMergeQueue : {
            value : function(data){
                this.mergeCluster[data] = 1;
            }
        },

        getMergeQueue : {
            value : function(){
                return Object.keys(this.mergeCluster).map(function(d){return parseInt(d);});
            }
        },

        clearMergeQueue : {
            value : function(){
                this.mergeCluster = [];
            }
        },

        removeMergeQueue : {
            value : function(data){
                if(data in this.mergeCluster){
                    delete this.mergeCluster[data];
                }
            }
        },

        addDetail : {
            value : function(){
                var detailed = this.module['detailed_view'];
                if(detailed instanceof LG.visual.DetailedView){
                    detailed.add();
                }
            }
        }

    });


    return SandBox;

}();