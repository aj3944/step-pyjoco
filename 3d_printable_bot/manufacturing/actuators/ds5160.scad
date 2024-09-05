



module ds5160(){

	color("grey"){
		cube([30,65,48],center=true);


		translate([0,0,15])
		difference(){
			cube([30,81,4],center=true);
			translate([0,0,-1])
			ds5160_monuting_holes();
		}
		translate([0,25,19.8])
		cylinder(r=5,h=10);
	}
}

module ds5160_body(t = 0.03){

	color("grey"){
		cube([30+t,65+t,88+t],center=true);
	}
}


module ds5160_monuting_holes(h = 10){
	translate([17/2,-75/2,-5])
	cylinder(h=h, r=3.5, center=false, $fn=20);

	translate([-17/2,-75/2,-5])
	cylinder(h=h, r=3.5, center=false, $fn=20);


	translate([-17/2,75/2,-5])
	cylinder(h=h, r=3.5, center=false, $fn=20);

	translate([17/2,75/2,-5])
	cylinder(h=h, r=3.5, center=false, $fn=20);
}


// ds5160_monuting_holes();


// ds5160();


module ds5160_back_bracket(){
	translate([0,0,-7])
	difference(){

	// translate([-5,-10,0])
	cube([60,90,38],center=true);

	cube([30,65,50],center=true);

	translate([0,20,-0])
	cube([12,95,50],center=true);

	translate([0,0,-45])
	ds5160_monuting_holes(120);

	}

}


// ds5160();
