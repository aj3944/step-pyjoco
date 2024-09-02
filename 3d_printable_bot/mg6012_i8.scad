$fn = 100;

module mg6012(){

	color("grey"){

	difference(){
	cylinder(r=31.5,h=12);
	translate([28.1,-40,-1])
	cube(size=[40,80,40], center=false);
	}

	difference(){

	translate([0,0,-29])
	cylinder(r=40,h=29);
	mg6012_screw_holes();

	}
	translate([0,0,-32])
	difference(){

		cylinder(r=26,h=3.5);
		translate([0,0,-1])
		cylinder(r=19,h=3.5);

	}

	difference(){

	translate([0,0,-33])
	cylinder(r=18.5,h=3.5);

	mg6012_mounting_holes();
	}


	mg6012_mounting_bumps();

	}
}


module mg6012_screw_holes(h = 8){
	translate([0,0,-30 ])
	for(i=[0:6]){
		rotate([0,0,60*i])
		translate([33.5,0,0])
		cylinder(r=3/2+0.2,h=h,$fn=20,center=true);
		rotate([0,0,30+60*i])
		translate([33.5,0,0])
		cylinder(r=4/2+0.2,h=h,$fn=20,center=true);
	}	
	translate([0,0,+1])
	for(i=[0:6]){
		rotate([0,0,30+60*i])
		translate([36,0,0])
		cylinder(r=3/2+0.2,h=h,$fn=20,center=true);
	}	
}
module mg6012_mounting_bumps(h = 12.5,del = 0){
	translate([0,0,-35])
	for(i=[0:3]){
		rotate([0,0,60+120*i])
		translate([19.43/2,0,0])
		cylinder(r=4/2+0.2 +del,h=h,$fn=20,center=true);
	}	
}

// mg6012_screw_holes();

// mg6012_mounting_holes();
// mg6012();

module mg6012_mounting_holes(h = 8,del = 0){
	translate([0,0,-34])
	for(i=[0:3]){
		rotate([0,0,120*i])
		translate([23/2 ,0,0])
		cylinder(r=4/2+0.2 +del,h=h,$fn=20,center=true);
	}

}


module bearing(){
	color("grey")
	difference(){
		cylinder(r=15/2,h=5,center=true);
		translate([0,0,0])
		cylinder(r=6/2,h=7,center=true);
	}
}
module bearing_blank(){
	color("grey")
	cylinder(r=15/2,h=10,center=true);
}

module bearing_mount_A(){
	difference(){
		cylinder(r=28/2,h=7+0.5,center=true);
		translate([0,0,0])
		cylinder(r=15/2+0.01,h=7+1,center=true);
	}
}
module bearing_mount_B(){
	difference(){
	cylinder(r=6/2-0.2,h=9,center=true);
	cylinder(r=4/2-0.2,h=10,center=true);
	
	}
}
module bearing_mount_C(){
	cylinder(r=9/2,h=7,center=true);
}


// mg6012();

module mg6012_back_grip(){

	difference(){
		cylinder(r=42,h=15);
		translate([0,0,-1])
		cylinder(r=32,h=13.5);
		translate([38,0,1])
		cube(30,center=true);
		mg6012_screw_holes(30);

	}

}


module tail_stand()
{

	mg6012_back_grip();

	intersection(){

		difference(){

			hull(){

				translate([-15,-45,0])
				cube(size=[40,90,10], center=false);


				translate([-15,-40,70])
				cube(size=[4,80,10], center=false);
			}
			translate([-10,-30,25])
			cube(size=[50,60,50], center=false);

			translate([0,0,-1])
			cylinder(r=32,h=12);
		}
		cylinder(r=42,h=120);
	}
}
// difference(){
// 	translate([0,0,-40 + 0.8])
// 	cylinder(r=42,h=10);
// 	translate([0,0,-41 + 0.8])
// 	cylinder(r=28,h=12);
// 	// translate([40,0,-40])
// 	// cube(30,center=true);
// 	screw_holes(30);

// }

// tail_stand();
// mg6012_back_grip();

// mg6012();


// module bracket(){

// 	difference()
// 	{

// 		translate([0,0,-40.5])
// 		cylinder(r=22,h=8);

// 		mounting_holes(20,0.2);

// 		mg6012();
// 	}	
// }

// bracket();

// module bare_bracket(d = 0){
// 	translate([0,0,-40.5])
// 	cylinder(r=22,h=8+d);
// }



// module bearing_mount(){

// 	difference(){

// 	cylinder(r=10,h=8);
// 	bearing_mount_C();
// 	translate([0,0,7])
// 	bearing_blank();

// 	}

// }

// module first_link(){
// bracket();

// difference(){

// hull()
// {

// translate([0,200,-40])
// {
// 	// bearing();
// 	bearing_mount_A();
// }


// // bare_bracket();

// translate([0,0,-40])
// cylinder(r=26,h=8);


// }

// translate([0,200,-42])
// bearing_blank();

// translate([0,200,-38])
// bearing_mount_C();

// translate([0,0,-42])
// cylinder(r=21,h=8+3);

// }
// }

// module second_link(){
// // bearing_mount_B();

// difference(){

// hull()
// {

// translate([0,200,-12])
// {
// 	// bearing();
// 	bearing_mount_A();
// }


// // bare_bracket();

// translate([0,0,-12])
// cylinder(r=10,h=8);


// }
// translate([0,0,-20])
// cylinder(r=6/2,h=28);

// translate([0,200,-9])
// bearing_blank();

// translate([0,200,-13])
// bearing_mount_C();

// }
// }



// bearing_mount();

// // 
// translate([0,200,-40])
// bearing_mount_B();


// translate([0,200,-40])
// bearing_mount_B();

// first_link();



// translate([0,200,-40.5])
// second_link();
// cylinder(r=7/2-0.2,h=7,center=true);
