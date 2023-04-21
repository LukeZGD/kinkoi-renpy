#!/bin/bash

printf '' > defs_bg.rpy
resize=0 # set to 1 for half size

bg_process() {
    dir=$1
    ext=$2

    mkdir Kinkoi_processed/$dir
    if [[ $dir != "evcg" ]]; then
        cp Kinkoi_extract/$dir/*.$ext Kinkoi_processed/$dir
        if [[ $resize == 1 ]]; then
            pushd Kinkoi_processed/$dir
            mogrify -resize 50% *.$ext
            popd
        fi
    fi
    if [[ $dir == "ui" ]]; then
        return
    fi
    for i in $(ls Kinkoi_processed/$dir/*.$ext); do
        name=$(basename $i)
        name=${name%%.*}
        echo "image bg $name = \"images/$dir/$name.$ext\"" >> defs_bg.rpy
    done
}

bg_process bg webp
bg_process effects png
bg_process effects webp
bg_process effects2 png
bg_process effects2 webp
bg_process evcg webp
bg_process ui png
