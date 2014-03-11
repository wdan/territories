/**
 * Created by wenbin on 11/3/14.
 */
LG.data.DataManager = function(){

    var DataManager = function(){
        console.log('[LOG] Data manager initialized');
        this.dataName = '';
        this.aggregate = {};
        this.original = {};
        this.width = undefined;
        this.height = undefined;
        this.shrink = undefined;
        this.rate = undefined;
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
                        _this.aggregate = data;
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
                    async: true,
                    success: function(data){
                        _this.original = data;
                        console.log('[LOG] Data Transmission Done.');
                        console.log(data);
                    }
                });
            }
        }

    });

    return DataManager;
}();