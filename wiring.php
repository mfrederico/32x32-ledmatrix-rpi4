<?php

$matrix_panels  = 4;
$matrix_panelx  = 32;
$matrix_panely  = 8;

//
$panels         = [];


for ($panel = 0;$panel < $matrix_panels;$panel++) {
    for ($pixel = 0;$pixel < ($matrix_panelx * $matrix_panely);$pixel++) {
        $panels[$panel][] = $pixel + ($panel * $matrix_panelx * $matrix_panely);
    }
}

foreach($panels as $panel=>$pixels) {
    $panelpixel[$panel] = array_chunk($pixels,$matrix_panely);
}



print "def getMatrix():\n\treturn[\n";

for ($x =0; $x < $matrix_panelx;$x++) { 
    foreach($panelpixel as $panel=>$pixels) {
        print "# {$panel}\n";
        if ($x % 2 == 0) { 
            $pixels[$x] = $pixels[$x];
        }
        else {
            $pixels[$x] = array_reverse($pixels[$x]);
        }

        print join(',',$pixels[$x]).",\n";
        
    }
}
print "\t]\n";

