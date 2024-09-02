module mg_90(){
	color("grey"){

	scale([32,3,12])
	cube(1,center=true);


	translate([0,6.5,0])
	scale([23,25,12])
	cube(1,center=true);


	translate([5,0,0])
	rotate([90,0,0])
	cylinder(r=6,h=8,center=false);


	translate([5,0,0])
	rotate([90,0,0])
	cylinder(r=2.5,h=12,center=false);
	}


	color("red"){

	translate([13.5,0,0])
	rotate([90,0,0])
	cylinder(r=1.2,h=15,center=true,$fn=20);


	translate([-13.5,0,0])
	rotate([90,0,0])
	cylinder(r=1.2,h=15,center=true,$fn=20);
	}
}

cl=0.8;

module base_bracket(){
	difference(){

		cube(size=[35,10,16], center=true);
		translate([0,-2,0])
		cube(size=[32+cl,12,12+cl], center=true);

		mg_90();
	}
}

// base_bracket();

module servo(){
	mg_90();
	color("white")
	translate([5,-10,0])
	rotate([-90,0,0])
	rotate([0,0,90])
	import("../horns/SG90_four_horns_with_holes.stl");
}


module shoulder_joint(left = 0){
	

	translate([0,0,5])
	rotate([0,90,0]){

		base_bracket();
		servo();
	}

	// symm_z = 0;

	// if(left)
	// {
	// 	symm_z = 90;
	// }
	if(left){
		translate([-5,-22,-37])
		rotate([0,90,0])
		rotate([90,0,0])
		{
			rotate([0,180,180])
			{

				base_bracket();
				servo();
			}
			

			translate([-18,6,0])
			cube([2,36,30],center=true);		
		}
	}
	else{
		translate([5,-22,-37])
		rotate([0,90,0])
		rotate([90,0,0])
		{

			base_bracket();
			servo();
			

			translate([-18,-6,0])
			cube([2,36,30],center=true);		
		}

	}
	if(left){
		translate([0,0,-5])
		rotate([0,180,0])
		{

			translate([5,-22,0])
			rotate([90,0,0]){

			translate([0,-10,-7])
			// difference(){

				cube(size=[30,30,2], center=true);
				// translate([0,0,0])
				// cube(size=[20+cl,12,12+cl], center=true);
				// }

				// rotate([180,0,180])
				rotate([0,0,180])
				{

				base_bracket();
				servo();
				}
			}
		}	
	}else{
		translate([10,0,-5])
		rotate([0,180,0])
		{

			translate([5,-22,0])
			rotate([90,0,0]){

			translate([0,-10,-7])
			// difference(){

				cube(size=[30,30,2], center=true);
				// translate([0,0,0])
				// cube(size=[20+cl,12,12+cl], center=true);
				// }

				rotate([180,0,180])
				rotate([0,0,180])
				{

				base_bracket();
				servo();
				}
			}
		}		
	}
}






// servo();


	// translate([0,0,300+5])
	// rotate([0,90,0]){

	// 	base_bracket();
	// 	servo();
	// }