#!/bin/bash

#mkdir output output2

pushd Kinkoi_extract/ui
magick _menu_bg.06.png _menu_bg.05.png _menu_bg.04.png _menu_bg.03.png _menu_bg.02.png _menu_bg.01.png _menu_character.01.png _menu_character.03.png _menu_character.04.png _menu_character.02.webp \( -page +0+915 _menu_btn_filter.png \) \( -page +20+720 en/_menu_title_logo.png \) -layers flatten ../../game/gui/main_menu.png
popd

magic() {
    base=ev_0$1_0$2
    diff=ev_0$1_0$3
    if [[ -e $2.webp ]]; then
        return
    fi
    echo "magic $1 $2"
    magick $1.webp diff/$2.webp -layers flatten diff2/$2.webp
    #rm diff/$2.webp
}

mkdir -p Kinkoi_processed 2>/dev/null
if [[ ! -d Kinkoi_processed/evcg ]]; then
    cp Kinkoi_data/evcg Kinkoi_processed
fi

pushd Kinkoi_processed/evcg

# orohora
magic ri11 101 201

# --- akane
magic ak01 101 201

magic ak02 101 102
magic ak02 101 103
magic ak02 101 104
magic ak02 101 105

magic ak02 101 201

magic ak02 401 403
magic ak02 401 404
magic ak02 401 405

magic ak03 101 102
magic ak03 101 103
magic ak03 101 104

magic ak04 101 102
magic ak04 101 103
magic ak04 101 104
magic ak04 101 105

magic ak05 101 102
magic ak05 101 103
magic ak05 101 104
magic ak05 101 105

magic ak06 101 102
magic ak06 101 103
magic ak06 201 202

# --- elle
magic er01 101 102
magic er01 101 103
magic er01 101 104
magic er01 101 201
magic er01 101 202
magic er01 101 301

magic er03 201 101
magic er03 201 202
magic er03 301 302
magic er03 301 303
magic er03 201 403
magic er03 201 404

magic er04 101 102
magic er04 201 202

magic er05 101 102
magic er05 101 103
magic er05 101 201
magic er05 101 202
magic er05 101 203
magic er05 101 204
magic er05 101 301
magic er05 101 302
magic er05 101 303

magic er06 101 102
magic er06 101 103

magic er07 101 102
magic er07 101 201
magic er07 101 202

magic er08 101 102

magic er09 101 102
magic er09 101 103

magic er10 101 102
magic er10 101 103

# --- reina
magic re01 101 102

magic re02 101 102
magic re02 101 103
magic re02 101 104
magic re02 101 201
magic re02 101 202
magic re02 101 203
magic re02 101 204

magic re03 101 102

magic re05 101 102
magic re05 101 103
magic re05 101 104
magic re05 101 105
magic re05 101 106

magic re07 101 102
magic re07 101 103
magic re07 101 104
magic re07 101 105

magic re08 101 102
magic re08 101 103

magic re09 101 102

magic re15 101 102
magic re15 101 103

# --- ria
magic ri02 101 102
magic ri02 101 103

magic ri02 201 202
magic ri02 201 203
magic ri02 201 204
magic ri02 201 205

magic ri02 101 301
magic ri02 101 302
magic ri02 101 303

magic ri02 201 401
magic ri02 201 402
magic ri02 201 403
magic ri02 201 404
magic ri02 201 405

magic ri02 201 402

# --- sylvie
magic sy01 101 102
magic sy01 101 103

magic sy01 201 202
magic sy01 201 203

magic sy02 101 102
magic sy02 101 103
magic sy02 101 104
magic sy02 101 105
magic sy02 101 106
magic sy02 101 107
magic sy02 101 108

magic sy02 201 202
magic sy02 201 203
magic sy02 201 204
magic sy02 201 205
magic sy02 201 206
magic sy02 201 207

magic sy02 201 301
magic sy02 201 302
magic sy02 201 303
magic sy02 201 304
magic sy02 201 306
magic sy02 201 307

magic sy02 201 401

magic sy03 101 102
magic sy03 101 103
magic sy03 101 104
magic sy03 201 202
magic sy03 201 203
magic sy03 201 204
magic sy03 301 302
magic sy03 301 305
magic sy03 301 306

magic sy04 101 102
magic sy04 101 103
magic sy04 101 104
magic sy04 101 105
magic sy04 101 201
magic sy04 101 202
magic sy04 101 203
magic sy04 101 204
magic sy04 101 205

magic sy05 101 102
magic sy05 101 103
magic sy05 101 104
magic sy05 101 105
magic sy05 101 106
magic sy05 101 107
magic sy05 101 108
magic sy05 101 109

magic sy06 102 101
magic sy06 101 103

# --- loveriche
magic yy01 103 101
magic yy01 103 102

rm -r diff
popd
