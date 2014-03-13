/**
 * Created by wenbin on 12/3/14.
 */

LG.visual.Visualization = function(){
    var Visualization = function(dat, svg, dataManager, className){
        this.dat = dat;
        this.svg = svg.append('g').attr('class', className);
        this.className = className;
        //this.classColor = colorbrewer.Set3[12];
        this.classColor = colorbrewer.Pastel1[9];
    };

    Object.defineProperties(Visualization.prototype, {

        update : {
            value : function(){
                console.error('[ERROR] Function update() should be overridden');
            }
        },

        display : {
            value : function(){
                console.error('[ERROR] Function display() should be overridden');
            }
        }

    });

    return Visualization;
}();
