#!/bin/bash

SECONDS=0
java -cp liblinear-1.94.jar de.bwaldvogel.liblinear.Train -s 0 $1 $2
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."