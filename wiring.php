<?php 
// I used 5V WS2812B Eco Led Panels 8x32 pixel density

//*********************************************************************
// Because I find python array handling to be an abomination (c) 2021
//*********************************************************************
// This spits out a python array definition of the pixels to STDOUT

$number_of_panels   = 4;    // How many panels you have?
$matrix_pixelsy     = 8;    // Vertical pixel density of a panel
$matrix_pixelsx     = 32;   // Horizontal pixel density of a panel

// Use this for later to contain my panels / pixels
$panels         = [];

// Create all the pixels (in numerical order starting at 0 
// Pixel density: ($matrix_pixelsy * $matrixpixelsx * $number_of_panels) 

for ($panel = 0;$panel < $number_of_panels;$panel++) {
    for ($pixel = 0;$pixel < ($matrix_pixelsx * $matrix_pixelsy);$pixel++) {
        $panels[$panel][] = $pixel + ($panel * $matrix_pixelsx * $matrix_pixelsy);
    }
}

/********************************/
/* This is where the fun begins */
/********************************/
// Start spitting out the (python) matrix definition file 
// python and its "tabs" (tsk tsk) what problem does this solve again?

print "def getMatrix():\n\treturn[\n";

// Since I stacked my panels VERITCALLY I need to array chunk my 
// pixels into {$matrix_pixelsy} slices (across the top) (thanks PHP!)

foreach($panels as $panel=>$pixels) {
    $panelpixel[$panel] = array_chunk($pixels,$matrix_pixelsy);
}

// Now go through each panelpixel array on the X axis and spit out the chain of 
// "zigzag" - chained panels.  this should also work with chained strings where applicable

for ($x =0; $x < $matrix_pixelsx;$x++) { 
    foreach($panelpixel as $panel=>$pixels) {
        print "# {$panel}\n";

        // Even rows keep "sane" and print straight 
        if ($x % 2 == 0) { 
            $pixels[$x] = $pixels[$x];
        }
        // Odd Rows we need to reverse these and start at the "rightmost" edge and go backwards
        else {
            $pixels[$x] = array_reverse($pixels[$x]);
        }

        // Print all my pixels out (thanks php!) with commas and newlines formatted for python3
        print join(',',$pixels[$x]).",\n";
        
    }
}
print "\t]\n"; 

// That's it!
