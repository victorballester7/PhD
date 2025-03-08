// Macro parameters
deltaStar = 1;
D = 4 * deltaStar; // depth of the gap 
W = 12 * deltaStar; // width of the gap
BL = 0.5 * deltaStar; // height of the second layer of quad elements
x0 = 50 * deltaStar; // x distance from inflow to gap
lengthOutflow = 500 * deltaStar; // length after the gap
BLquads_outflow = Sqrt(lengthOutflow) * BL;
x3 = W + lengthOutflow; // last point of the domain
height = 75 * deltaStar; // height of the triangular region
triagHeightRegion_inflow = height - BL; // height of the triangular region
triagHeightRegion_outflow = height - BLquads_outflow; // height of the triangular region


// Micro parameters
dx = 0.05; // dx of square elements near the leading and trailing edge of the gap (most resolution-demanding points in the domain)
size_triag_v_top = 16; // size of the elements in the upper triangular region

// All the value below are between 0 and 1. =1  means the elements are all equal in size. Avoid using values very close to 1, because we dividing by log(p) in the formula.
p_in_v_right = 0.87; // densitiy concentration of elements inside the gap, vertically, near the right wall.
p_in_v_right_upper = 0.95; // densitiy concentration of elements inside the gap, vertically, near the right wall.
p_in_v_left = 0.8; // densitiy concentration of elements inside the gap, vertically, near the left wall.
p_in_v_left_upper = 0.89; // densitiy concentration of elements inside the gap, vertically, near the left wall.
p_in_h = 0.9; // densitiy concentration of elements inside the gap, horizontally. 

p_out_h = 0.5; // densitiy concentration of elements outside the gap, horizontally.
p_out_v_inflow_upper = 0.98; // densitiy concentration of elements outside the gap, vertically, near the inflow.
p_out_v_inflow_lower = 0.95; // densitiy concentration of elements outside the gap, vertically, near the inflow.
p_out_v_outflow_upper = 0.98; // densitiy concentration of elements outside the gap, vertically, near the outflow on the upper layer of the quads.
p_out_v_outflow_lower = 0.97; // densitiy concentration of elements outside the gap, vertically, near the outflow on the lower layer of the quads.
p_triag_h_inflow = 0.8; // densitiy concentration of elements in the triangular region of the domain, horizontally.
p_triag_h_outflow = p_triag_h_inflow; // densitiy concentration of elements in the triangular region of the domain, horizontally.

enlarge_triag_inflow = 1.2; // heigher the value, larger the elements in the triangular region near the inflow
enlarge_triag_outflow = 1; // heigher the value, larger the elements in the triangular region near the outflow


// Automated parameters 
a_in_v_right = dx / (W / 2);
a_in_v_left = dx / (W / 2);
a_in_h = dx / (D / 2);
a_out_h = dx / BL;
a_out_v_inflow = dx / x0;
a_out_v_outflow = dx / lengthOutflow;

// for the derivation of the formula, see file 20250123_gmshFormula.md in the docs folder
N_in_v_right = Ceil( Log (a_in_v_right / (1 - p_in_v_right + a_in_v_right * p_in_v_right)) / Log(p_in_v_right) );
N_in_v_left = Ceil( Log (a_in_v_left / (1 - p_in_v_left + a_in_v_left * p_in_v_left)) / Log(p_in_v_left) );
N_in_h = Ceil( Log (a_in_h / (1 - p_in_h + a_in_h * p_in_h)) / Log(p_in_h) );
N_out_h = Ceil( Log (a_out_h / (1 - p_out_h + a_out_h * p_out_h)) / Log(p_out_h) ) + 1; // + 1 is to correct the fact that the distance is too small to properly approximate the dx length
N_out_v_inflow = Ceil( Log (a_out_v_inflow / (1 - p_out_v_inflow_lower + a_out_v_inflow * p_out_v_inflow_lower)) / Log(p_out_v_inflow_lower) );
N_out_v_outflow = Ceil( Log (a_out_v_outflow / (1 - p_out_v_outflow_lower + a_out_v_outflow * p_out_v_outflow_lower)) / Log(p_out_v_outflow_lower) );


// ---------------------------
// for triangular region
// ---------------------------
a_triag_h_inflow = (BL) / (triagHeightRegion_inflow) * (1 - p_out_h) / (1 - p_out_h^(N_out_h + 1));
a_triag_h_outflow = (BLquads_outflow) / (triagHeightRegion_outflow) * (1 - p_out_h) / (1 - p_out_h^(N_out_h + 1));
N_triag_v_top = Ceil( (x3 + x0) / size_triag_v_top ); // we assume p_triag_v = 1, otherwise the formula is different
N_triag_h_inflow = Ceil( Log(a_triag_h_inflow / (1 - p_triag_h_inflow + a_triag_h_inflow * p_triag_h_inflow)) / Log(p_triag_h_inflow) );
N_triag_h_outflow = Ceil( Log(a_triag_h_outflow / (1 - p_triag_h_outflow + a_triag_h_outflow * p_triag_h_outflow)) / Log(p_triag_h_outflow) );
N_triag_h_inflow = Ceil( N_triag_h_inflow / enlarge_triag_inflow );
N_triag_h_outflow = Ceil( N_triag_h_outflow / enlarge_triag_outflow );

Point(1) = {-x0, 0, 0};
Point(2) = {0,0,0};
Point(3) = {0,-D,0};
Point(4) = {W,-D,0};
Point(5) = {W,0,0};
Point(6) = {x3,0,0};
Point(8) = {x3,height,0};
Point(7) = {x3,BLquads_outflow,0};
Point(9) = {-x0,height,0};
Point(10) = {-x0,BL,0};
Point(11) = {0,BL,0};
Point(12) = {W,BL,0};
Point(13) = {W/2,0,0};
Point(14) = {W/2,BL,0};
Point(15) = {0,-D/2,0};
Point(16) = {W/2,-D,0};
Point(17) = {W,-D/2,0};

Line(1) = {1,2};
Line(2) = {2,15};
Line(3) = {3,16};
Line(4) = {4,17};
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};
Line(10) = {10,11};
Line(11) = {10,1};
Line(12) = {11,14};
Line(13) = {12,7};
Line(14) = {2,13};
Line(15) = {15,3};
Line(16) = {16,4};
Line(17) = {17,5};
Line(18) = {13,5};
Line(19) = {14,12};

// outer quads
Curve Loop(1) = {5, 6, -13, -19, -12, -10, 11, 1, 14, 18};
Plane Surface(1) = {1};

// inside gap
Curve Loop(2) = {2, 15, 3, 16, 4, 17, -18, -14};
Plane Surface(2) = {2};

// triangular region
Curve Loop(3) = {10, 12, 19, 13, 7, 8, 9};
Plane Surface(3) = {3};


// This defines the surfaces that will be meshed with quad elements
Transfinite Surface {1} = {1, 6, 7, 10};
Transfinite Surface {2} = {3, 4, 5, 2}; // number '2' must match the number '2' of plane surface

Transfinite Curve {18, 16} = N_in_v_right Using Progression p_in_v_right;
Transfinite Curve {19} = N_in_v_right Using Progression p_in_v_right_upper;
Transfinite Curve {-14, -3} = N_in_v_left Using Progression p_in_v_left;
Transfinite Curve {-12} = N_in_v_left Using Progression p_in_v_left_upper;
Transfinite Curve {-2, 15, 17, -4} = N_in_h Using Progression p_in_h;

Transfinite Curve {11, -6} = N_out_h Using Progression p_out_h;
Transfinite Curve {-13} = N_out_v_outflow Using Progression p_out_v_outflow_upper;
Transfinite Curve {-5} = N_out_v_outflow Using Progression p_out_v_outflow_lower;
Transfinite Curve {10} = N_out_v_inflow Using Progression p_out_v_inflow_upper;
Transfinite Curve {1} = N_out_v_inflow Using Progression p_out_v_inflow_lower;

Recombine Surface {1, 2};

// for triangluar region
Transfinite Curve {8} = N_triag_v_top Using Progression 1;
Transfinite Curve {-7} = N_triag_h_outflow Using Progression p_triag_h_outflow;
Transfinite Curve {9} = N_triag_h_inflow Using Progression p_triag_h_inflow;


// defining boundary
Physical Curve(1) = {9,11}; // inlet
Physical Curve(2) = {7,6}; // outlet
Physical Curve(3) = {8}; // top
Physical Curve(4) = {1, 2, 15, 3, 16, 4, 17, 5}; // wall


Physical Surface(100) = {1};
Physical Surface(101) = {2};
Physical Surface(102) = {3};
