include <./constants.scad>


module side_plate(){
difference(){


sequentialHull(){


translate([0,-SHOULDER_OFFSET,SHOULDER_HEIGHT+45])
translate([0,0,-70])
cube(size=[100,20,20], center=true);

translate([0,-SHOULDER_OFFSET/2,SHOULDER_HEIGHT/2])
cube(size=[150,20,20], center=true);

translate([0,-LINK_OFFSET_1 ,40])
cube(size=[100,20,20], center=true);
}

for(i=[0:3])
{
	translate([0,0,90*i])
	cube(size=[80,LINK_OFFSET_1*3,60], center=true);
}
}	
}



module top_plate(){
	sequentialHull(){

	translate([0,-SHOULDER_OFFSET,SHOULDER_HEIGHT+45])
	translate([0,0,-70])
	cube(size=[100,20,20], center=true);
	translate([0,-SHOULDER_OFFSET,SHOULDER_HEIGHT+45])
	cube(size=[100,20,20], center=true);
	translate([0,0,SHOULDER_HEIGHT+55])
	cube(size=[150,20,20], center=true);
	translate([0,SHOULDER_OFFSET,SHOULDER_HEIGHT+45])
	cube(size=[100,20,20], center=true);
	translate([0,SHOULDER_OFFSET,SHOULDER_HEIGHT+45])
	translate([0,0,-70])
	cube(size=[100,20,20], center=true);
	}

}

module mid_plates(){
	difference(){

	sequentialHull(){
		translate([0,-SHOULDER_OFFSET/2,SHOULDER_HEIGHT/2])
		cube(size=[150,20,20], center=true);
		translate([0,0,SHOULDER_HEIGHT/2])
		cube(size=[200,20,20], center=true);
		translate([0,SHOULDER_OFFSET/2,SHOULDER_HEIGHT/2])
		cube(size=[150,20,20], center=true);
	}

	for(i=[-1:1])
	{
		translate([0,-i*SHOULDER_OFFSET/3,SHOULDER_HEIGHT/2])
		cube([120,20,90],center=true);
	}
	}
}

module torso(){
	side_plate();
	mirror([0,1,0])
	side_plate();
	top_plate();
	mid_plates();

	translate([0,0,SHOULDER_HEIGHT+65])
	cube(size=[50,20,40], center=true);

}




module right_arm_actuators(){

	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([0,0,-ELBOW_HEIGHT])
	rotate([0,90,0])
	scale(1.5)
	{
		base_bracket();
		servo();
	}



	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	rotate([0,90,90])
	scale(1.2)
	{
		base_bracket();
		servo();
	}


	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	translate([DIGIT_OFFSET,-DIGIT_HEIGHT,0])
	rotate([90,0,0])
	{
		base_bracket();
		servo();
	}



	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	translate([DIGIT_OFFSET,DIGIT_HEIGHT,0])
	rotate([90,0,0])
	{
		base_bracket();
		servo();
	}




	translate([0,-SHOULDER_OFFSET,SHOULDER_HEIGHT])
	scale(2)
	shoulder_joint();

}


module bicep_link(){
	sequentialHull(){

	translate([0,-SHOULDER_OFFSET,SHOULDER_HEIGHT])
	translate([-20,-45,-80])
	rotate([0,90,0])
	cylinder(r=30,h=20,center=true);



	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([0,0,-ELBOW_HEIGHT])
	translate([0,20,30])
	rotate([180,0,0])
	cube([20,50,20],center=true);

	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([0,0,-ELBOW_HEIGHT])
	translate([0,20,-15])
	rotate([220,0,0])
	cube([20,50,20],center=true);
	}
}

module forearm_link(){
	sequentialHull(){
		translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
		translate([0,0,-ELBOW_HEIGHT])
		translate([0,-25,0])
		rotate([90,0,0])
		cylinder(r=25,h=15,center=true);


		translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
		translate([WRIST_OFFSET-10,0,-ELBOW_HEIGHT])
		rotate([90,0,0])
		cube([20,40,20],center=true);
	}
}



module wrist_mount(){

	sequentialHull(){

	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	translate([DIGIT_OFFSET,-DIGIT_HEIGHT,0])
	rotate([0,0,90])
	cube([20,40,10],center=true);

	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	translate([30,0,0])
	rotate([0,0,90])
	cube([20,40,10],center=true);



	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	translate([DIGIT_OFFSET,DIGIT_HEIGHT,0])
	rotate([0,0,90])
	cube([20,40,10],center=true);
	}

	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET+20,0,-ELBOW_HEIGHT])
	rotate([0,90,0])
	cylinder(r=25,h=15,center=true);
}


module digit(){
	sequentialHull(){
		cube(size=[20,20,20], center=false);
		translate([GRIPPER_OFFSET,-GRIPPER_HEIGHT,10])
		cube(size=[10,10,10], center=false);
	}
}


module gripper(){
	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	translate([DIGIT_OFFSET,DIGIT_HEIGHT,0])
	translate([-10,-10,-30])
	digit();	
	translate([0,-ELBOW_OFFSET,SHOULDER_HEIGHT])
	translate([WRIST_OFFSET,0,-ELBOW_HEIGHT])
	translate([DIGIT_OFFSET,-DIGIT_HEIGHT,0])
	translate([-10,10,-30])
	mirror([0,1,0])
	digit();	
}


module right_arm(){
	bicep_link();
	forearm_link();
	wrist_mount();
	gripper();	
}



module face_actuators(){
	translate([0,0,SHOULDER_HEIGHT+85])
	rotate([-90,0,0])
	{
		base_bracket();
		servo();
	}


	translate([0,-4,SHOULDER_HEIGHT+115])
	rotate([-0,0,0])
	{
		base_bracket();
		servo();
	}
}


module face_brackets(){

	sequentialHull(){

	translate([0,0,SHOULDER_HEIGHT+95])
	cylinder(r=10,h=10);


	translate([0,0,SHOULDER_HEIGHT+115])
	cube(size=[70,10,20], center=true);
	}

	sequentialHull(){

		translate([0,-14,SHOULDER_HEIGHT+115])
		rotate([90,0,0])
		cylinder(r=20,h=10);
		translate([0,-24,SHOULDER_HEIGHT+155])
		cylinder(r=10,h=10);
		translate([0,-24,SHOULDER_HEIGHT+155])
		cylinder(r=20,h=10);
		translate([0,24,SHOULDER_HEIGHT+155])
		cylinder(r=20,h=10);
	}
}
