#!/bin/bash

printf '' > defs_bg.rpy
resize=0 # set to 1 for half size

if [[ -z $1 ]]; then
    echo "Usage: ./bg.sh [Aokana|AokanaEXTRA1|Kinkoi]"
    exit 1
fi

game="$1"

if [[ ! -d ${game}_Data ]]; then
    echo "${game}_Data folder not found"
    exit 1
fi

bg_process() {
    dir=$1
    ext=$2

    mkdir -p ${game}_processed/$dir
    if [[ $dir != "evcg" ]]; then
        cp ${game}_extract/$dir/*.$ext ${game}_processed/$dir
        if [[ $resize == 1 ]]; then
            pushd ${game}_processed/$dir
            mogrify -resize 50% *.$ext
            popd
        fi
    fi
    if [[ $dir == "ui" ]]; then
        return
    fi
    for i in $(ls ${game}_processed/$dir/*.$ext); do
        name=$(basename $i)
        name=${name%%.*}
        echo "image bg $name = \"images/$dir/$name.$ext\"" >> defs_bg.rpy
    done
}

bg_process bg webp
bg_process effects png
bg_process evcg webp

if [[ $game == "Kinkoi" ]]; then
    bg_process effects webp
    bg_process effects2 png
    bg_process effects2 webp
    bg_process ui png
fi
