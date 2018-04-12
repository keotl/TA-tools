#!/bin/bash
touch rapport.html;
for dir in ./*/
do
    dir=${dir%*/}
    echo $dir;
    ./showContributions.sh $dir >> rapport.html;
done
