#!/bin/bash

printf '' > defs_bg.rpy

for i in $(ls Kinkoi_extract/bg/*.webp); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"$i\"" >> defs_bg.rpy
done

for i in $(ls Kinkoi_extract/effects/*.png); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"$i\"" >> defs_bg.rpy
done


for i in $(ls Kinkoi_extract/evcg/*.webp); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"$i\"" >> defs_bg.rpy
done
