#!/bin/bash
#set -x
trap 'exit' INT TERM EXIT

crop() {
    magick convert ${1}0.webp -crop $2 +repage +adjoin -scene 1 crop/$1%02d.webp
}

sprite() {
    char=$(echo $1 | cut -c 5- | cut -c -2)
    base=$(basename $1)
    base=${base%%.*}
    face="$(echo $1 | cut -c -8)_face1_"
    defs="$(tr -d "\r" < defs.txt)"

    for i in $defs; do
        #echo $i
        if [[ ${i:0:1} == '>' ]]; then
            prop=${i:1}
            IFS=',' read -ra props <<< "$prop"
            basex=${props[1]}
            basey=${props[2]}
            facex=${props[3]}
            facey=${props[4]}
            cropx=${props[5]}
            cropy=${props[6]}
            continue
        fi

        if [[ ${props[0]} != "${face}0" ]]; then
            continue
        fi

        i=$(echo $i | tr '.' '_')

        #echo crop/$i
        #read -s
        if [[ ! -e crop/$i.webp ]]; then
            echo "cropping"
            crop $face ${cropx}x${cropy}
        fi

        imagest="image $char $base $i = im.Composite(($basex,$basey),(0,0),\"images/sprite/$base.webp\",($facex,$facey),\"images/sprite/crop/$i.webp\")"

        echo "$imagest" >> defs_sprite.rpy
    done
}

mkdir -p Kinkoi_processed 2>/dev/null
if [[ ! -d Kinkoi_processed/sprite ]]; then
    cp -r Kinkoi_extract/sprite Kinkoi_processed
fi

pushd Kinkoi_processed/sprite

printf '' > defs_sprite.rpy
mkdir crop

for i in $(ls *.webp); do
    name=$(basename $i)
    name=${name%%.*}
    if [[ $i != *"base"* ]]; then
        continue
    fi
    echo $name
    sprite $i
done

mv defs_sprite.rpy ../..
popd
