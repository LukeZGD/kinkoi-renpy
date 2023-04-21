#!/bin/bash
#set -x
trap 'exit' INT TERM EXIT

defs="$(tr -d "\r" < Kinkoi_extract/sprite/defs.txt)"
resize=0 # set to 1 for half size

crop() {
    if [[ -n $3 ]]; then
        magick convert ${1}_1.webp -crop $2 +repage +adjoin -scene $3 crop/$1%02d.webp
        return
    fi
    magick convert ${1}_0.webp -crop $2 +repage +adjoin -scene 1 crop/$1%02d.webp
}

sprite() {
    char=$(echo $1 | cut -c 5- | cut -c -2)
    base=$(basename $1)
    base=${base%%.*}
    face="$(echo $1 | cut -c -8)_face1"

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

            if [[ $resize == 1 ]]; then
                basex=$((basex/2))
                basey=$((basey/2))
                facex=$((facex/2))
                facey=$((facey/2))
            fi

            if [[ ${props[0]} == "${face}_0" ]]; then
                imagest="image $char $base $face = LiveComposite(($basex,$basey),(0,0),\"images/sprite/$base.webp\",($facex,$facey),\"images/sprite/crop/${face}_[$face].webp\")"
                echo "$imagest" >> defs_sprite.rpy
            fi

            continue
        fi

        if [[ ${props[0]} != "${face}_0" && ${props[0]} != "${face}_1" ]]; then
            continue
        fi

        i=$(echo $i | tr '.' '_')

        case $i in
            "bs3_ak_b"* | "bs3_ma_"* ) scene=25;;&
            "bs3_ay_"* | "bs3_re_"* ) scene=22;;&
            "bs3_ak_b"* | "bs3_ay_"* | "bs3_ma_"*  | "bs3_re_"* )
                if [[ ! -e crop/$i.webp ]]; then
                    echo "cropping"
                    crop $face ${cropx}x${cropy}
                    echo "cropping1"
                    crop $face ${cropx}x${cropy} $scene
                fi
            ;;

            * )
                if [[ ! -e crop/$i.webp ]]; then
                    echo "cropping"
                    crop $face ${cropx}x${cropy}
                fi
            ;;
        esac

        #imagest="image $char $base $i = im.Composite(($basex,$basey),(0,0),\"images/sprite/$base.webp\",($facex,$facey),\"images/sprite/crop/$i.webp\")"
        #echo "$imagest" >> defs_sprite.rpy
    done
}

mkdir -p Kinkoi_processed 2>/dev/null
if [[ ! -d Kinkoi_processed/sprite ]]; then
    cp -r Kinkoi_extract/sprite Kinkoi_processed
fi

pushd Kinkoi_processed/sprite

printf '' > defs_sprite.rpy
mkdir crop

for i in $(ls b*base*.webp); do
    name=$(basename $i)
    name=${name%%.*}
    if [[ $i != *"base"* ]]; then
        continue
    fi
    echo $name
    sprite $i
done

#for i in $(ls bs*_face*0.webp); do
    #face=$(echo $i | cut -c -14)
    #echo "default $face = \"gui/namebox.png\"" >> defs_sprite.rpy
#done

if [[ $resize == 1 ]]; then
    : mogrify -resize 50% *.webp crop/*.webp
fi
mv defs_sprite.rpy ../..
popd
