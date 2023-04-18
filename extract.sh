#!/bin/bash
set -x

# This uses Aokana-Extractor: https://github.com/hktkqj/Aokana-Extractor

# NekoNyanDatTool can also be used: https://forums.fuwanovel.net/topic/4887-data-extraction-thread/page/46/#comment-532569
# https://www.mediafire.com/file/0cw55ccjp2c77cn/NekoNyanDatTool.exe/file
# https://www.mediafire.com/file/3cdhkgijn56t4tn/NekoNyanDatTool_26052022.7z/file

if [[ ! -d Kinkoi_Data ]]; then
    echo "Kinkoi_Data folder not found"
    exit 1
fi

for i in $(ls Kinkoi_Data/*.dat); do
    if [[ $i == *"voice"* ]]; then
        continue
    fi
    echo "Extracting $i"
    #wine NekoNyanDatTool.exe --input=$i --output=output/ --unpack --format kinkoi_pc
    python extractor/extract.py $i Kinkoi_extract
done

echo "Extracting voice"
#wine NekoNyanDatTool.exe --input=Kinkoi_Data/voice.dat --output=voice/ --unpack --format kinkoi_pc
python extractor/extract.py Kinkoi_Data/voice.dat Kinkoi_voice

# UABE helped a bit in figuring out the video extraction: https://github.com/SeriousCache/UABE

echo "Extracting video"
xxd -s +4747 -l 6820319 -c 10 -p Kinkoi_Data/video | xxd -r -p - > sagaplanets.webm

echo "Extracting video_en"
xxd -s +5053 -l 75473080 -c 10 -p Kinkoi_Data/video_en | xxd -r -p - > op_en.mp4
xxd -s +75478134 -l 138390743 -c 10 -p Kinkoi_Data/video_en | xxd -r -p - > ed_en.mp4

#rm game/images/* game/audio/*
#mv Kinkoi_extract/bg Kinkoi_extract/effects Kinkoi_extract/evcg Kinkoi_extract/sprite game/images
#mv Kinkoi_extract/bgm Kinkoi_extract/sfx game/audio
#mv Kinkoi_voice game/audio
