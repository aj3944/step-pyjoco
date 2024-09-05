

dummy_rr = 22;
dummy_rs = 30;
dummy_ss = 50; 

dummy_hs = 20;
dummy_hrs = 24;
dummy_hrr = 26;

module actuator_dummy(){
	cylinder(h=dummy_hs, r=dummy_ss, center=false, $fn=20);
	cylinder(h=dummy_hrs, r=dummy_rs, center=false, $fn=20);
	cylinder(h=dummy_hrr, r=dummy_rr, center=false, $fn=20);
}

module r_drills(skip = 0,h = 10,tol = 0){
	translate([0,0,20])
	for(i=[0:6])
	{	
		if(!skip || i%2){
			rotate([0,0,i*60])
			translate([0,15,0])
			cylinder(r=2+skip+tol,h=h,center=true);
		}
	}
}
module sr_drills(skip = 0,h = 15,tol = 0){
	translate([0,0,15])
	for(i=[0:11])
	{	
		rotate([0,0,i*30])
		translate([0,40,0])
		cylinder(r=2+i%2+tol,h=h,center=true);
	}
}
module ss_drills(skip = 0,h = 15,tol = 0){
	translate([0,0,-5])
	for(i=[0:11])
	{	
		rotate([0,0,15+i*30])
		translate([0,40,0])
		cylinder(r=2+tol,h=h,center=true);
	}
}


module actuator_dummy_unit(){
	difference(){
		actuator_dummy();
		r_drills();
		sr_drills();
		ss_drills();		
	}

	r_drills(1);
}

module actuator_dummy_interface_r(){
	difference(){
		translate([0,0,dummy_hrr+1])
		cylinder(r=dummy_rr,h=10);

		r_drills(0,50,.2);
		r_drills(1,50,.2);
	}
}
module actuator_dummy_mi_r(){
	translate([0,0,dummy_hrr+1])
	cylinder(r=dummy_rr,h=10);
}

module actuator_dummy_interface_s(){
	difference(){
		translate([0,0,-10-1])
		cylinder(r=dummy_ss,h=10);

		ss_drills(0,30,.2);
	}
}
module actuator_dummy_mi_s(){
	translate([0,0,-10-1])
	cylinder(r=dummy_ss,h=10);
}


// actuator_dummy_unit();
// actuator_dummy_interface_r();
// actuator_dummy_mi_r();
// actuator_dummy_interface_s();
// actuator_dummy_mi_s();
