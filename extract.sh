#!/bin/bash
set -x

# This uses Aokana-Extractor: https://github.com/hktkqj/Aokana-Extractor

# NekoNyanDatTool can also be used: https://forums.fuwanovel.net/topic/4887-data-extraction-thread/page/46/#comment-532569
# https://www.mediafire.com/file/0cw55ccjp2c77cn/NekoNyanDatTool.exe/file
# https://www.mediafire.com/file/3cdhkgijn56t4tn/NekoNyanDatTool_26052022.7z/file

if [[ -z $1 ]]; then
    echo "Usage: ./extract.sh [Aokana|AokanaEXTRA1|Kinkoi]"
    exit 1
fi

game="$1"

if [[ ! -d ${game}_Data ]]; then
    echo "${game}_Data folder not found"
    exit 1
fi

for i in $(ls ${game}_Data/*.dat); do
    if [[ $i == *"voice"* ]]; then
        continue
    fi
    echo "Extracting $i"
    #wine NekoNyanDatTool.exe --input=$i --output=output/ --unpack --format kinkoi_pc
    python extractor/extract.py $i ${game}_extract
done

echo "Extracting voice"
#wine NekoNyanDatTool.exe --input=${game}_Data/voice.dat --output=voice/ --unpack --format kinkoi_pc
python extractor/extract.py ${game}_Data/voice.dat ${game}_extract/voice

# UABE helped a bit in figuring out the video extraction: https://github.com/SeriousCache/UABE

if [[ $game == "Kinkoi" ]]; then
    mkdir ${game}_extract/video
    echo "Extracting video"
    xxd -s +4747 -l 6820319 -c 10 -p ${game}_Data/video | xxd -r -p - > ${game}_extract/video/sagaplanets.webm

    echo "Extracting video_en"
    xxd -s +5053 -l 75473080 -c 10 -p ${game}_Data/video_en | xxd -r -p - > ${game}_extract/video/op_en.mp4
    xxd -s +75478134 -l 138390743 -c 10 -p ${game}_Data/video_en | xxd -r -p - > ${game}_extract/video/ed_en.mp4
fi

#rm game/images/* game/audio/*
#mv ${game}_extract/bg ${game}_extract/effects ${game}_extract/evcg ${game}_extract/sprite game/images
#mv ${game}_extract/bgm ${game}_extract/sfx game/audio
#mv ${game}_voice game/audio
