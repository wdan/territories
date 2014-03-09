/**
 * Created by wenbin on 9/3/14.
 */


function segment(cur, next, roundlen, bend, ratio){

    var s ="";

    var v = vectorNorm(cur, next);
    var r = vecterRotate(v, 0);


    s += " A " + roundlen + " " + roundlen + " 0 0 0 "
        + (r.x * roundlen + cur[0]) + " " + (r.y * roundlen + cur[1]);

    if (v.length<=2*roundlen) bend = 0;
    s += " q " + vecterAdd(r, 0, v, ratio * v.length) + " " +
        vecterAdd(r, -0.5 * bend, v, 0.25 * v.length);
    s += " t " + vecterAdd(r, -0.5 * bend, v, 0.25 * v.length) +
        " " + vecterAdd(r, 0.5 * bend, v, 0.25 * v.length) +
        " " + vecterAdd(r, 0.5 * bend, v, 0.25 * v.length);

    return s;

}


function vectorNorm(from, to){

    var v = {
        x : (to[0]-from[0]),
        y : (to[1]-from[1])
    };
    v.length = Math.sqrt( v.x * v.x + v.y * v.y);

    v.x = v.x / v.length;
    v.y = v.y / v.length;

    return v;
}

function vecterAdd(v1, u1, v2, u2){
    // return vector: v1 * u1 + v2 * u2
    return (v1.x * u1 + v2.x * u2) + " " + (v1.y * u1 + v2.y * u2);
}

function vecterRotate(v, direction){
    // direction == 1 counterclockwise

    if(direction){
        return { x : v.y, y : -v.x};
    }else {
        return { x : -v.y, y : v.x};
    }

}

function draw_hulls(nodes, polygons){
    data = {};
    cluster_list = [];

    for(var i=0;i<polygons.length;i++){
        var p = polygons[i];
        data[p.cluster] = [];
        cluster_list.push(p.cluster);

        for(var j=0;j< p.points.length;j++){
            data[p.cluster].push([p.points[j].x, p.points[j].y]);
        }

    }

    for(i=0;i<nodes.length;i++){
        data[nodes[i].cluster].push([nodes[i].x, nodes[i].y]);
    }

    hull = svg.append('g').attr("class", "hull");

    for(i=0;i<cluster_list.length;i++){
        var cid = cluster_list[i];

        hull.append("path")
            .datum(d3.geom.hull(data[cid]))
//            .data(data[cid])
//            .enter()
            .attr("d", function(d){

                var n = d.length;

                var v = vectorNorm(d[n-1], d[0]);
                var r = vecterRotate(v, 0);

                var roundlen = 10;
                var ratio = 0.12;
                var bend = 8;

                var s = "M " + (roundlen * r.x + d[0][0]) + " " + (roundlen * r.y + d[0][1]);

                for (var i = 0; i < n; i++){
                    s += segment(d[i], d[(i+1)%n], roundlen, bend, ratio);
                }

                s += "Z";

                return s;
            })
            .style("fill", function(d){
                return "#a6bddb";
//                return color(cid);
            })
            .style("fill-opacity", 0.3)
            .style("stroke", '#a6bddb')
            .style("stroke-opacity", 0.3)
            .style("stroke-width", "3px")
            .style("stroke-linejoin", 'round');

    }


}