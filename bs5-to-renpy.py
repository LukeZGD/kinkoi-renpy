import re
import sys
import os

if len(sys.argv) == 2:
    inputFile = sys.argv[1]
    #outputFile = sys.argv[2]
else:
    print("Invalid arguments. pass 1 file as argument")
    print("example: python3 bs5-to-renpy.py inputfile")
    exit()

debug = 1
scene = ''
scenetoggle = 1
inputname = os.path.splitext(os.path.basename(inputFile))[0]
outputFile = inputname+".rpy"
spriteb = [{'b':'','f':'','char':'','chart':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','chart':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','chart':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','chart':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','chart':'','x':0.5,'y':0.5,'order':1},
           ]

voicefilelist = "voicefilelist.txt"
bgmfilelist = "bgmfilelist.txt"
sfxfilelist = "sfxfilelist.txt"
#with open(voicefilelist, 'w') as f:
#    f.write('')
#with open(bgmfilelist, 'w') as f:
#    f.write('')
#with open(sfxfilelist, 'w') as f:
#    f.write('')

with open(outputFile, 'w') as f:
    f.write('')

def scene_conv(scene):
    if (scene == "#000000") or (scene == "erase"):
        scene = "black"
    elif (scene == "#FFFFFF"):
        scene = "white"
    return scene

def sprite_process(sprite, spriteb, sindex):
    spritea = ''

    if sprite[0]:
        spriteb[index]['b'] = sprite[0].replace('f_','')

    spriteb[index]['chart'] = spriteb[index]['b'][4:-9]
    if (spriteb[index]['char'] != '' and spriteb[index]['chart'] != spriteb[index]['char']):
        spritea += "    hide "+spriteb[index]['char']+" with Dissolve(0.35)\n"

    spriteb[index]['char'] = spriteb[index]['chart']
    spriteb[index]['f'] = sprite[1].replace('.','_')
    spritea += "    show "+spriteb[index]['char']+' '+spriteb[index]['b']+' '+spriteb[index]['f']
    return spritea

with open(inputFile, 'r+') as filedata:
    # Iterate through the file
    for i in filedata:
        if debug == 1:
            print("processing line:", i)

        # background music
        if i.startswith('bgm0'):
            newline = i.split()
            bgm = newline[1]
            time = 0

            for j in newline:
                if 'TIME:' in j:
                    newline2 = i.split(':')
                    time = int(newline2[1])/1000

            if 'fadeout' in bgm:
                bgm = "    stop music fadeout "+str(time)+"\n"
            elif 'stop' in bgm:
                bgm = "    stop music\n"
            else:
                bgmfile = "audio/bgm/"+bgm+".ogg"
                bgm = "    play music \""+bgmfile+"\"\n"

            #with open(bgmfilelist, 'a') as f:
            #    f.write(bgmfile+"\n")

            with open(outputFile, 'a') as f:
                f.write(bgm)

        elif i.startswith('@SoundStopAll'):
            newline = i.split()
            time = newline[1]

            with open(outputFile, 'a') as f:
                f.write("    stop music fadeout "+str(time)+"\n")

        # wait -> pause in renpy
        elif i.startswith('wait'):
            newline = i.split()
            wait = int(newline[1])/1000
            with open(outputFile, 'a') as f:
                f.write("    pause "+str(wait)+"\n")

        # disablewindow -> scenetoggle
        elif i.startswith('@DisableWindow'):
            scenetoggle = 1

        # jump to label
        elif i.startswith('jump'):
            newline = i.split()
            jump = "jump s"+inputname+"_"+newline[1].replace(':','')+"\n"
            print(jump)
            #input()
            with open(outputFile, 'a') as f:
                f.write('    '+jump)

        # labels
        elif ':\n' in i:
            label = ''
            if not 'Z00' in i:
                label += '    return\n'
            label += "label s"+inputname+"_"+i
            print(label)
            #input()
            with open(outputFile, 'a') as f:
                f.write(label)

        # backgrounds and cgs
        elif i.startswith('.scene') or i.startswith('scene'):
            newline = i.split()
            scenep = scene_conv(newline[1])
            if scenetoggle == 1:
                scene = "    scene bg "+scenep
                scenetoggle = 0
            else:
                scene = "    show bg "+scenep

            time = 0
            time2 = 0
            xpos = 0
            ypos = 0
            xpan = 0
            ypan = 0
            zoom = 1
            resx = 1920
            resy = 1080
            zoox = resx
            zooy = resy
            zoox2 = zoox
            zooy2 = zooy
            easeyes = 0
            nextline = ''

            print(newline)

            for j in newline:
                if 'TIME:' in j:
                    newline2 = j.split(':')
                    print(newline2)
                    time = int(newline2[1])/1000
                elif 'X:' in j:
                    newline2 = j.split(':')
                    xpos = int(newline2[1])
                elif 'Y:' in j:
                    newline2 = j.split(':')
                    ypos = int(newline2[1])
                elif 'Z:' in j:
                    newline2 = j.split(':')
                    zoom = int(newline2[1])/100
                    print(zoom)

            zoom2 = zoom
            if i.startswith('.scene'):
                nextline = next(filedata)

            if nextline.startswith('.bg'):
                newline2 = nextline.split()
                easeyes = 1
                print(newline2)
                for j in newline2:
                    if 'TIME:' in j:
                        newline2 = j.split(':')
                        print(newline2)
                        time2 = int(newline2[1])/1000
                    elif 'X:' in j:
                        newline2 = j.split(':')
                        xpan = int(newline2[1])
                    elif 'Y:' in j:
                        newline2 = j.split(':')
                        ypan = int(newline2[1])
                    elif 'Z:' in j:
                        newline2 = j.split(':')
                        zoom2 = int(newline2[1])/100

            zoox = resx/zoom
            zooy = resy/zoom
            zoox2 = resx/zoom2
            zooy2 = resy/zoom2

            if zoom > 1:
                xpos = ((resx-(resx/zoom))/2)-xpos
                ypos = ((resy-(resy/zoom))/2)-ypos

            if zoom2 > 1:
                xpan = ((resx-(resx/zoom))/2)-xpan
                ypan = ((resy-(resy/zoom))/2)-ypan

            scene += " with Dissolve("+str(time)+"):\n"
            scene += "        size("+str(resx)+","+str(resy)+") crop ("+str(xpos)+","+str(ypos)+","+str(zoox)+","+str(zooy)+")"

            if easeyes == 1:
                scene += "\n        easein "+str(time2)+" crop ("+str(xpan)+","+str(ypan)+","+str(zoox2)+","+str(zooy2)+")"

            print(scene)
            #input()
            with open(outputFile, 'a') as f:
                f.write(scene+"\n")

        # screen shake
        elif i.startswith('quake'):
            if not scenep:
                continue

        # whiteout background
        elif i.startswith('@WhiteoutBySA'):
            newline = i.split()
            time = newline[1]
            time = int(time[:-1])/1000
            scene = "    scene white with Dissolve("+str(time)+")\n"

            with open(outputFile, 'a') as f:
                if newline[2] != "false":
                    f.write(scene)

        # voices
        elif i.startswith('voice0'):
            newline = i.split()
            voice = newline[1]

            if 'stop' in voice:
                continue

            voicefile = "audio/voice/z"+voice+".ogg"

            #with open(voicefilelist, 'a') as f:
            #    f.write(voicefile+"\n")

            with open(outputFile, 'a') as f:
                f.write("    play voice2 \""+voicefile+"\"\n")

        # sound effects
        elif i.startswith('se'):
            j = i[2]
            if not j.isdigit():
                continue

            newline = i.split()
            sfx = newline[1]

            if 'fadeout' in sfx or 'stop' in sfx:
                continue

            sfxfile = "audio/sfx/"+sfx+".ogg"

            #with open(sfxfilelist, 'a') as f:
            #    f.write(sfxfile+"\n")

            with open(outputFile, 'a') as f:
                f.write("    play sound \""+sfxfile+"\"\n")

        # dialogue
        elif '␂' in i:
            newline = i.split('␂')
            en = newline[1].split('：')
            en_speaker = ''
            if '【' in en[0]:
                en_speaker = en[0].replace('【','').replace('】','')

            if en_speaker:
                en = en[-1].replace('"', '\\"')
                en_line = '    "'+en_speaker+'" "'+en+"\"\n"
            else:
                en = en[0][1:].replace('"', '\\"')
                en_line = '    "'+en+"\"\n"

            en_line = en_line.replace('<i>','{i}').replace('</i>','{/i}')

            # prologue 1 fixes
            en_line = en_line.replace('{/i}do{/i}','{i}do{/i}').replace('<I>','{i}')

            with open(outputFile, 'a') as f:
                f.write(en_line)

        # choices
        elif i.startswith('␅select'):
            print('choice')

        # sprites
        elif '.sprite' in i:
            newline = i.split()
            time = 0
            sprite = ''
            spriteerase = 0
            if i.startswith('.sprite'):
                index = int(i[7])
            elif i.startswith('sprite'):
                index = int(i[6])
            else:
                continue
            print(newline)
            #input()

            if index >= 5:
                continue

            for j in newline:
                if j.startswith('bs') or j.startswith('f_bs') or j.startswith('+'):
                    sprite = j
                elif j.startswith('TIME:'):
                    newline2 = j.split(':')
                    print(newline2)
                    time = int(newline2[1])/1000
                elif j.startswith('X:'):
                    newline2 = j.split(':')
                    spriteb[index]['x'] = newline2[1]
                    if newline2[1].lstrip("-").isdigit():
                        spritd=560
                        spriteb[index]['x'] = ((spritd/2)+int(newline2[1]))/spritd
                    else:
                        spriteb[index]['x'] = 0.5
                elif j.startswith('Y:'):
                    newline2 = j.split(':')
                    spriteb[index]['y'] = newline2[1]
                    if newline2[1].lstrip("-").isdigit():
                        spriteb[index]['y'] = int(newline2[1])+100
                    else:
                        spriteb[index]['y'] = 0.5
                elif j.startswith('ORDER:'):
                    newline2 = j.split(':')
                    spriteb[index]['order'] = int(newline2[1])/10
                elif j.startswith('erase'):
                    spriteerase = 1

            if spriteerase == 1:
                sprite = "    hide "+str(spriteb[index]['char'])+" with Dissolve(0.35)"
                spriteb[index]['char'] = ''

            elif sprite:
                sprite = sprite.split('+')
                sprite = sprite_process(sprite, spriteb, i)
                sprite += " zorder "+str(spriteb[index]['order'])
                sprite += " with Dissolve("+str(time)+"):\n        xalign "+str(spriteb[index]['x'])+" yalign 0.5"

            else:
                continue

            with open(outputFile, 'a') as f:
                f.write(sprite+"\n")

        else:
            pass

    with open(outputFile, 'a') as f:
        f.write("    return\n")

filedata.close()
