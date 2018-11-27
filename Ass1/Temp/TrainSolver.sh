#!/bin/bash

java -Xmx1024m -cp liblinear-2.11.jar de.bwaldvogel.liblinear.Train -s 0 -c 0.001 $1 $2
echo "Done!"

