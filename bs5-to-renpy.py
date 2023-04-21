#!/usr/bin/env python3

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
res = [1920,1080] # set to 960,540 for half size
inputname = os.path.splitext(os.path.basename(inputFile))[0]
outputFile = inputname+".rpy"
sprite_q = [{'b':'','f':'','char':'','char_next':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','char_next':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','char_next':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','char_next':'','x':0.5,'y':0.5,'order':1},
           {'b':'','f':'','char':'','char_next':'','x':0.5,'y':0.5,'order':1},
           ]
spritetran = 0
spritemove = 0

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

def sprite_process(sprite, sprite_q, index, time):
    sprite_ret = ''

    try:
        if sprite[1]:
            sprite_q[index]['f_next'] = sprite[1].replace('.','_')
        if sprite[0]:
            sprite_q[index]['b'] = sprite[0].replace('f_','')
    except:
        pass

    #print('yes')
    print(sprite_q[index]['f'])
    #input()

    if (sprite_q[index]['f_next'] != sprite_q[index]['f']):
        sprite_f = sprite_q[index]['f_next'][:14]
        sprite_ret += "    $ "+sprite_f+" = \""+sprite_q[index]['f_next'][15:]+"\"\n"
        sprite_q[index]['f'] = sprite_q[index]['f_next']

    sprite_q[index]['char_next'] = sprite_q[index]['b'][4:-9]

    if (sprite_q[index]['char'] != '' and sprite_q[index]['char_next'] != sprite_q[index]['char']):
        sprite_ret += "    hide "+sprite_q[(index)]['char']+" with Dissolve("+str(time)+")\n"

    sprite_q[index]['char'] = sprite_q[index]['char_next']
    sprite_ret += "    show "+sprite_q[index]['char']+' '+sprite_q[index]['b']+' '+sprite_q[index]['f'][:14]
    return sprite_ret

with open(inputFile, 'r+') as filedata:
    # Iterate through the file
    for i in filedata:
        if debug == 1:
            print("processing line:", i)

        if spritetran == 1 and not '.sprite' in i:
            spritetran = 0
            with open(outputFile, 'a') as f:
                f.write("    with Dissolve("+str(spritetime)+")\n")

        # background music
        if i.startswith('bgm0'):
            newline = i.split()
            bgm_file = "audio/bgm/"+newline[1]+".ogg"
            time = 0
            print(newline)

            for j in newline:
                if 'TIME:' in j:
                    newline2 = j.split(':')
                    time = int(newline2[1])/1000

            if 'fadeout' in bgm_file or 'stop' in bgm_file:
                bgm = "    stop music fadeout "+str(time)+"\n"
            else:
                bgm = "    play music \""+bgm_file+"\"\n"

            #with open(bgmfilelist, 'a') as f:
            #    f.write(bgmfile+"\n")

            with open(outputFile, 'a') as f:
                f.write(bgm)

        elif 'SoundStopAll' in i:
            newline = i.split()
            time = int(newline[1])/1000

            with open(outputFile, 'a') as f:
                f.write("    stop music fadeout "+str(time)+"\n")

        # wait -> pause in renpy
        elif i.startswith('wait'):
            newline = i.split()
            wait = int(newline[1])/1000
            with open(outputFile, 'a') as f:
                f.write("    pause "+str(wait)+"\n")

        # disablewindow -> scenetoggle
        elif 'DisableWindow' in i:
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
            zoox = res[0]
            zooy = res[1]
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

            zoox = res[0]/zoom
            zooy = res[1]/zoom
            zoox2 = res[0]/zoom2
            zooy2 = res[1]/zoom2

            if zoom > 1:
                xpos = ((res[0]-(res[0]/zoom))/2)-(xpos*(res[0]/1920))
                ypos = ((res[1]-(res[1]/zoom))/2)-(ypos*(res[1]/1080))

            if zoom2 > 1:
                xpan = ((res[0]-(res[0]/zoom2))/2)-(xpan*(res[0]/1920))
                ypan = ((res[1]-(res[1]/zoom2))/2)-(ypan*(res[1]/1080))

            scene += " with Dissolve("+str(time)+"):\n"
            scene += "        size("+str(res[0])+","+str(res[1])+") crop ("+str(xpos)+","+str(ypos)+","+str(zoox)+","+str(zooy)+")"

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
            spritetime = 0.2
            sprite = ''
            spriteerase = 0
            spritemove = 0
            spritetran = 1
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
                    spritetime = int(newline2[1])/1000

                elif j.startswith('X:'):
                    newline2 = j.split(':')
                    sprite_q[index]['x'] = newline2[1]
                    if newline2[1].lstrip("-").isdigit():
                        if res[0] == 960:
                            spritex = (res[0]/4)+(res[0]/3)
                        else:
                            spritex = (res[0]/4)+(res[0]/12)
                        sprite_q[index]['x'] = ((spritex/2)+int(newline2[1]))/spritex
                    else:
                        sprite_q[index]['x'] = 0.5

                elif j.startswith('Y:'):
                    newline2 = j.split(':')
                    sprite_q[index]['y'] = newline2[1]
                    if newline2[1].lstrip("-").isdigit():
                        sprite_q[index]['y'] = int(newline2[1])+100
                    else:
                        sprite_q[index]['y'] = 0.5

                elif j.startswith('ORDER:'):
                    newline2 = j.split(':')
                    sprite_q[index]['order'] = int(newline2[1])/10
                elif j.startswith('erase'):
                    spriteerase = 1

            if spriteerase == 1:
                sprite = "    hide "+str(sprite_q[index]['char'])
                sprite_q[index]['char'] = ''

            else:
                sprite = sprite.split('+')
                sprite = sprite_process(sprite, sprite_q, index, spritetime)
                sprite += " zorder "+str(sprite_q[index]['order'])+":\n"
                if spritemove == 1:
                    sprite += "        easein "+str(spritetime)+" xalign "+str(sprite_q[index]['x'])+" yalign 0.5"
                else:
                    sprite += "        xalign "+str(sprite_q[index]['x'])+" yalign 0.5"

            with open(outputFile, 'a') as f:
                f.write(sprite+"\n")

        else:
            pass

    with open(outputFile, 'a') as f:
        f.write("    return\n")

filedata.close()
