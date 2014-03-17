/**
 * Created by wenbin on 16/3/14.
 */

LG.control.SandBox = function(){

    var SandBox = function(){
        console.log('[LOG] SandBox initialized');
        this.module = {};
        this.exchangeCluster = [];
    };

    Object.defineProperties(SandBox.prototype, {

        add : {
            value : function(className, obj){
                this.module[className] = obj;
            }
        },

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

                console.log('add_Cluster_queue');
                console.log(this.exchangeCluster);
            }
        }

    });


    return SandBox;

}();