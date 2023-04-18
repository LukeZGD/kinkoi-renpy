#!/bin/bash

printf '' > defs_bg.rpy

for i in $(ls Kinkoi_extract/bg/*.webp); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"images/bg/$name.webp\"" >> defs_bg.rpy
done

for i in $(ls Kinkoi_extract/effects/*.png); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"images/effects/$name.png\"" >> defs_bg.rpy
done


for i in $(ls Kinkoi_processed/evcg/*.webp); do
    name=$(basename $i)
    name=${name%%.*}
    echo "image bg $name = \"images/evcg/$name.webp\"" >> defs_bg.rpy
done
