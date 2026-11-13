define slowfade = Fade(1.0, 0.4, 1.0, color="#000")
define blackout = Fade(0.35, 0.5, 0.35, color="#000")
define whiteflash = Fade(0.04, 0.0, 0.35, color="#fff")
define redflash = Fade(0.05, 0.0, 0.3, color="#3a0505")
define coldfade = Fade(0.8, 0.2, 0.8, color="#0a1420")

transform char_left:
    xalign 0.18
    yalign 1.0
    zoom 0.72

transform char_left_in:
    xalign 0.18
    yalign 1.0
    zoom 0.72
    alpha 0.0
    yoffset 35
    ease 0.45 alpha 1.0 yoffset 0

transform char_center:
    xalign 0.5
    yalign 1.0
    zoom 0.72

transform char_center_in:
    xalign 0.5
    yalign 1.0
    zoom 0.72
    alpha 0.0
    yoffset 35
    ease 0.45 alpha 1.0 yoffset 0

transform char_right:
    xalign 0.82
    yalign 1.0
    zoom 0.72

transform char_right_in:
    xalign 0.82
    yalign 1.0
    zoom 0.72
    alpha 0.0
    yoffset 35
    ease 0.45 alpha 1.0 yoffset 0

transform girl_close:
    xalign 0.5
    yalign 1.0
    zoom 0.88
    alpha 0.0
    ease 0.8 alpha 1.0

transform entity_flicker:
    xalign 0.5
    yalign 1.0
    zoom 0.82
    alpha 0.9
    block:
        ease 0.08 alpha 1.0
        ease 0.12 alpha 0.86
        pause 0.2
        repeat

transform entity_emerge:
    xalign 0.5
    yalign 1.0
    zoom 0.75
    alpha 0.0
    yoffset 80
    ease 2.0 alpha 1.0 yoffset 0 zoom 0.86

transform logo_float:
    xalign 0.5
    ypos 70
    zoom 0.74
    alpha 0.0
    yoffset -30
    ease 1.2 alpha 1.0 yoffset 0
    block:
        ease 3.5 yoffset 8
        ease 3.5 yoffset 0
        repeat

transform notify_appear:
    xalign 0.5
    ypos 42
    alpha 0.0
    yoffset -22
    ease 0.25 alpha 1.0 yoffset 0

transform phone_alert_appear:
    xalign 1.0
    xoffset 40
    ypos 60
    alpha 0.0
    ease 0.3 xoffset 0 alpha 1.0

transform hotspot_pulse:
    zoom 0.45
    alpha 0.0
    block:
        ease 1.1 zoom 1.1 alpha 0.65
        ease 0.0 zoom 0.45 alpha 0.0
        pause 0.25
        repeat

transform ctc_blink:
    alpha 1.0
    linear 0.55 alpha 0.15
    linear 0.55 alpha 1.0
    repeat

transform low_sanity_pulse:
    alpha 0.0
    linear 1.6 alpha 0.55
    linear 1.6 alpha 0.0
    repeat

transform glitch_flash:
    alpha 0.0
    linear 0.04 alpha 0.85
    linear 0.09 alpha 0.0
    pause 0.04
    linear 0.03 alpha 0.45
    linear 0.12 alpha 0.0

transform slow_zoom:
    xalign 0.5
    yalign 0.5
    zoom 1.0
    linear 26.0 zoom 1.06

transform ending_cg:
    xalign 0.5
    yalign 0.5
    zoom 1.0
    linear 18.0 zoom 1.05

transform ending_title_in:
    alpha 0.0
    yoffset 22
    ease 1.0 alpha 1.0 yoffset 0

transform credits_scroll:
    ypos 1100
    linear 42.0 ypos -1200

transform ghost_fade:
    alpha 0.0
    ease 2.0 alpha 0.7
    pause 1.0
    ease 2.0 alpha 0.35
