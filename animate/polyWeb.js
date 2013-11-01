var myApp = {};
(function(context) { 
    
    var data;
    var width;
    var height;
    var svg;
    var lattice;

    
    context.setData = function(d) {
        data = d;
    }

    context.animate = function(name, w, h) {
        width = w;
        height = h;
        
        // Create the svg element
        svg = d3.select(name).append("svg")
                .attr("width", w)
                .attr("height", h);

        // Create the lattice

        lattice = svg.selectAll("text")
            .data(data)
            .enter()
            .append("rect");
      
        var additional_time = 0;
        var time_step = 1;
        var shape_count = 0;

        lattice.transition()
            .attr("x", function(d,i) { return 50*d.cell[1] ; } )
            .attr("y", function(d,i) { return 50*d.cell[0] ; } )
            .attr("width", 45)
            .attr("height", 45)
            .attr("fill", function(d) {

                var t = d.type;
                var val = d.val;

                if( t === "make" ) {
                    if( val === true ) {
                        return "#ABC"; // AVAILABLE TO EXPLORE
                    }
                    else {
                        return "black"; // NEVER AVAILABLE
                    }
                }
                
                else if( t === "mark" ) {
                    if( val === true ) {
                        return "#ABC"; // AVAILABLE TO EXPLORE
                    }
                    else {
                        return "#CBA" // NOT AVAILABLE TO EXPLORE
                    }
                }
                else if( t === "path" ) {
                    if( val === true ) {
                        return "red";// ON THE PATH
                    }
                    else {
                        return "#CBA"; // NOT AVAILABLE TO EXPLORE
                    }
                }
                else if( t === "neighbors" ) {
                    return "blue";// NEIGHBOR OF TOP OF PATH
                }
            })
            .delay(function(d,i) {

                if( d.type === "path" && d.val == false )
                    additional_time += 5*time_step;
                    shape_count++;
                if( d.type === "neighbors")
                    additional_time += 5*time_step;

                return i*time_step + additional_time;
            });  
    }//animate

})(myApp);


