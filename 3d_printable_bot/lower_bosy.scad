
module hip_bracket(){
	difference(){

		hull(){
			translate([0,-LINK_OFFSET_1,-43])
			cylinder(h=10, r=26, center=false, $fn=50);	


			translate([0,-LINK_OFFSET_1 - 10,-LINK_LENGTH_2])
			rotate([0,90,-90])
			difference(){

				cylinder(r=42,h=15);
				translate([30,0,0])
				cube(size=[70,90,50], center=true);
			}
		}

		translate([0,-LINK_OFFSET_1 + 25,-LINK_LENGTH_2])
		rotate([0,90,-90])
		cylinder(r=42,h=50);

		translate([0,-LINK_OFFSET_1,-LINK_LENGTH_2 + 17])
		cylinder(h=32, r=20, center=false, $fn=50);

		translate([0,-LINK_OFFSET_1,0])
		rotate([0,0,180])
		{
			mg6012_mounting_holes(40);
			mg6012_mounting_bumps();
		}

		translate([0,-LINK_OFFSET_1 - 10,-LINK_LENGTH_2])
		rotate([0,90,-90])
		mg6012_screw_holes(40);

	}

	translate([0,-LINK_OFFSET_1 - 10,-LINK_LENGTH_2])
	rotate([0,90,-90])
	mg6012_back_grip();

}



module thigh_bracket()
{
	difference(){

	sequentialHull()
	{

	translate([0,-LINK_OFFSET_1 + 40,-LINK_LENGTH_2])
	rotate([0,90,-90])
	cylinder(h=17, r=29, center=false, $fn=50);

	translate([0,-LINK_OFFSET_1 + 40,-LINK_LENGTH_2 - 80])
	rotate([0,90,-90])
	cylinder(h=17, r=29, center=false, $fn=50);

	translate([0,-LINK_OFFSET_1,-LINK_LENGTH_3])
	rotate([0,90,90])
	difference(){
		cylinder(r=42,h=15);
		translate([30,0,0])
		cube(size=[70,90,50], center=true);
	}
	}



	translate([0,-LINK_OFFSET_1 - 10,-LINK_LENGTH_2])
	rotate([0,90,-90])
	{
		mg6012_mounting_bumps(40);
		mg6012_mounting_holes(40);
	}

		translate([0,-LINK_OFFSET_1,-LINK_LENGTH_3])
		rotate([0,90,90])
		mg6012_screw_holes(50);

		translate([0,-LINK_OFFSET_1 + 20,-LINK_LENGTH_3])
		rotate([0,90,90])
		cylinder(r=42,h=45);

		translate([0,-LINK_OFFSET_1 - 1,-LINK_LENGTH_3])
		rotate([0,90,90])
		cylinder(r=31.5,h=14);

	}

	translate([0,-LINK_OFFSET_1,-LINK_LENGTH_3])
	rotate([0,90,90])
	mg6012_back_grip();
}


module shin_bracket(){

	difference(){


		sequentialHull()
		{

		translate([0,-LINK_OFFSET_1 - 35,-LINK_LENGTH_3])
		rotate([0,90,-90])
		cylinder(h=17, r=29, center=false, $fn=50);

		translate([10,-LINK_OFFSET_1 - 35,-LINK_LENGTH_3 - 80])
		rotate([0,90,-90])
		cylinder(h=17, r=25, center=false, $fn=50);


		translate([7,-LINK_OFFSET_4,-LINK_LENGTH_4])
		rotate([-90,0,90])
			translate([0,-40,0])
			cube([60,10,36],center=true);
		}
		translate([0,-LINK_OFFSET_4,-LINK_LENGTH_4])
		rotate([-90,0,90])
		translate([0,0,-60]){
			ds5160_monuting_holes(120);
			ds5160_body();
		
		}	

		translate([0,-LINK_OFFSET_1,-LINK_LENGTH_3])
		rotate([0,90,90])
		{
			mg6012_mounting_bumps(40);
			mg6012_mounting_holes(40);
		}




	}


	translate([0,-LINK_OFFSET_4,-LINK_LENGTH_4])
	rotate([-90,0,90])
	ds5160_back_bracket();
}




module foot_bracket(){

	translate([LINK_OFFSET_5,-LINK_OFFSET_1-20,-LINK_LENGTH_5])
	sequentialHull()
	{
		cube([40,80,10],center=true);

		translate([-100,0,10])
		cube([40,80,20],center=true);
		translate([-150,0,00])
		cube([40,80,10],center=true);
	}

	translate([LINK_OFFSET_5,-LINK_OFFSET_1-20,-LINK_LENGTH_5])
	translate([-115,0,40])
	cube([20,80,40],center=true);

}

module right_leg(){


	hip_bracket();
	thigh_bracket();
	shin_bracket();
	foot_bracket();

}

	// translate([0,-25,0])
	// ds5160();


module ankle_motor(){

translate([0,-LINK_OFFSET_4,-LINK_LENGTH_4])
rotate([-90,0,90])
{	
	ds5160();
}

}


module hip_motor(){

translate([0,-LINK_OFFSET_1,0])
rotate([0,0,180])
mg6012();	
}

module thigh_motor(){


translate([0,-LINK_OFFSET_1 - 10,-LINK_LENGTH_2])
rotate([0,90,-90])
mg6012();
}

module knee_motor(){
translate([0,-LINK_OFFSET_1,-LINK_LENGTH_3])
rotate([0,90,90])
mg6012();

}
module right_actuators(){

	hip_motor();
	thigh_motor();
	knee_motor();
	ankle_motor();
}




module hip_plate(){
	translate([0,-LINK_OFFSET_1,0])
	rotate([0,0,180])
	mg6012_back_grip();
	translate([0,LINK_OFFSET_1,0])
	rotate([0,0,180])
	mg6012_back_grip();


	sequentialHull()
	{
	translate([0,LINK_OFFSET_1,14])
	cylinder(r=32,h=5);		
	translate([0,LINK_OFFSET_1,30])
	cylinder(r=40,h=20);		
	translate([0,0,30])
	cylinder(r=90,h=20);		
	translate([0,-LINK_OFFSET_1,30])
	cylinder(r=40,h=20);	
	translate([0,-LINK_OFFSET_1,14])
	cylinder(r=32,h=5);	
	}

}
// mirror([0,1,0])
hip_plate ();
{
	hip_bracket();
	hip_motor();
}
{
	thigh_bracket();
	thigh_motor();

}

{

	shin_bracket();
	knee_motor();
	ankle_motor();
}
{

	foot_bracket();
}