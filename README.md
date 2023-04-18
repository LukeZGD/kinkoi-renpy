# kinkoi-renpy
Project that attempts to port Kinkoi from Unity to Ren'Py.

- Use [Ren'Py 7.4.9](https://www.renpy.org/release/7.4.9).
- `extract.sh` - Extracts all files to `Kinkoi_extract`. This requires `Kinkoi_Data` folder from a copy of [Kinkoi: Golden Loveriche](https://kinkoi.nekonyansoft.com/).
- `evcg.sh` - Creates evcg files from diffs. It will also create `main_menu.png` placed in `game/gui`. This is not a great way of doing CGs, but this will do for now. Output of this script goes to `Kinkoi_processed` folder.
- `sprite.sh` - Crops the face sprites and creates `defs_sprite.rpy`. Also not a great way of doing sprites, but this will do for now. Output sprites go to `Kinkoi_processed` folder. Place the output rpy file in the game folder.
- `bg.sh` - Scans bg, effects, evcg folders to create `defs_bg.rpy`. Run this after `evcg.sh`. Place the output rpy file in the game folder.
- `bs5-to-renpy.py` - The main script converter. Converts bs5 scripts to rpy files. Only tested on `00_prologue1.bs5` for now.