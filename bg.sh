#!/bin/bash

printf '' > defs_bg.rpy

for i in $(ls images/bg/*.webp); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"$i\"" >> defs_bg.rpy
done

for i in $(ls images/effects/*.png); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"$i\"" >> defs_bg.rpy
done


for i in $(ls images/evcg/*.webp); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"$i\"" >> defs_bg.rpy
done
