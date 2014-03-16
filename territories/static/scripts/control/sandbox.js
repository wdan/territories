/**
 * Created by wenbin on 16/3/14.
 */

LG.control.SandBox = function(){

    var SandBox = function(){
        console.log('[LOG] SandBox initialized');
        this.module = {};
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
        }

    });


    return SandBox;

}();