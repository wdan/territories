/**
 * Created by wenbin on 16/3/14.
 */

LG.utils = LG.utils || {};

LG.utils.vector = (function(){
    return {
        norm : function(from, to){
            var v = {
                x : to.x - from.x,
                y : to.y - from.y
            };
            v.length = Math.sqrt( v.x * v.x + v.y * v.y);
            v.x = v.x / v.length;
            v.y = v.y / v.length;
            return v;
        }
    };
})();