Point(1) = {0, 0, 0};
Point(2) = {2,0,0};
Point(3) = {2,-1,0};
Point(4) = {6,-1,0};
Point(5) = {6,0,0};
Point(6) = {20,0,0};
Point(7) = {20,1.5,0};
Point(8) = {20,10,0};
Point(9) = {0,10,0};
Point(10) = {0,1.5,0};
Point(11) = {2,1.5,0};
Point(12) = {6,1.5,0};
Point(13) = {4,0,0};
Point(14) = {4,1.5,0};
Point(15) = {2,-0.5,0};
Point(16) = {4,-1,0};
Point(17) = {6,-0.5,0};

Line(1) = {1,2};
Line(2) = {2,15};
Line(3) = {3,16};
Line(4) = {4,17};
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};
Line(10) = {10,1};
Line(11) = {10,11};
Line(12) = {11,14};
Line(13) = {12,7};
Line(14) = {2,13};
Line(15) = {15,3};
Line(16) = {16,4};
Line(17) = {17,5};
Line(18) = {13,5};
Line(19) = {14,12};

Curve Loop(1) = {2, 15, 3, 16, 4, 17, -18, -14};
Plane Surface(1) = {1};

Curve Loop(2) = {1,14,18,5,6,-13,-19,-12,-11,10};
Plane Surface(2) = {2};

Curve Loop(3) = {11, 12, 19, 13, 7, 8, 9};
Plane Surface(3) = {3};


// Meshing
a = 18;
b = 22;
c = 80;
d = 30;

p = 0.85;
q = 0.9;
r = 0.95;

Transfinite Surface {1} = {3, 4, 5, 2}; // number '1' must match the number '1' of plane surface
Transfinite Surface {2} = {1, 6, 7, 10}; // number '2' must match the number '2' of plane surface

Transfinite Curve {-14, 18, -3, 16, -12, 19} = d Using Progression q;
Transfinite Curve {-2, 15, 17, -4} = a Using Progression p;


Transfinite Curve {1, 11} = b Using Progression p;
Transfinite Curve {10, -6} = a Using Progression p;
Transfinite Curve {-13, -5} = c Using Progression r;

Recombine Surface {1, 2};

Transfinite Curve {8} = 12 Using Progression 1;
Transfinite Curve {-7, 9} = 12 Using Progression r;

// defining boundary
Physical Curve(1) = {9, 10}; // inlet
Physical Curve(2) = {6, 7}; // outlet
Physical Curve(3) = {8}; // top
Physical Curve(4) = {1, 3, 16, 5, 2, 15, 4, 17}; // wall


Physical Surface(100) = {1};
Physical Surface(101) = {2};
Physical Surface(102) = {3};
