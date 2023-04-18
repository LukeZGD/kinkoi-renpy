image black = "#000000"
image white = "#FFFFFF"
image bg black = "#000000"
image bg white = "#FFFFFF"

image _splash_caution = "images/ui/_start_caution.png"

label splashscreen:
    scene black
    with Pause(0.1)

    show _splash_caution with Dissolve(0.8)
    with Pause(5)

    scene black with Dissolve(0.8)
    with Pause(0.1)

    $ renpy.movie_cutscene("sagaplanets.webm")

    scene black
    with Pause(0.1)

    show hf_neko_logo with Dissolve(0.8)
    with Pause(3)

    scene black with Dissolve(0.8)
    with Pause(0.8)

    return

# The game starts here.

label start:
    stop music fadeout 2
    scene bg white with Dissolve(2.0):
        size(1920,1080) crop (0,0,1920.0,1080.0)

    call s00_prologue1_Z00
    call s00_prologue1_z01
    return
