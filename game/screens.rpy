default quick_menu = True

style default:
    font "fonts/EBGaramond.ttf"
    size 38
    color "#e8e2d6"
    outlines [(2, "#00000099", 0, 0)]
    line_spacing 6

style say_window is window:
    background "images/ui/textbox.png"
    xsize 1920
    ysize 380
    xalign 0.5
    yalign 1.0
    padding (0, 0)

style namebox is window:
    background "images/ui/namebox.png"
    xsize 640
    ysize 92
    xpos 585
    ypos -14
    padding (20, 6)

style say_label is default:
    font "fonts/Cinzel.ttf"
    size 34
    color "#d8c49a"
    xalign 0.5
    yalign 0.5
    outlines [(2, "#000000cc", 0, 0)]

style say_dialogue is default:
    xpos 610
    ypos 92
    xsize 1190
    color "#ece6da"
    size 39
    line_spacing 10
    outlines [(2, "#000000bb", 0, 0)]

style menu_button is button:
    xsize 560
    ysize 68
    background "images/ui/button_idle.png"
    hover_background "images/ui/button_hover.png"
    hover_sound "audio/sfx/ui_hover.ogg"
    activate_sound "audio/sfx/ui_click.ogg"
    padding (20, 8)

style menu_button_text is button_text:
    font "fonts/Cinzel.ttf"
    size 31
    color "#cfc6b4"
    hover_color "#f0dfb6"
    insensitive_color "#5d584f"
    xalign 0.5
    yalign 0.5
    outlines [(1, "#00000099", 0, 0)]

style choice_button is button:
    xsize 1240
    ysize 96
    background "images/ui/choice_idle.png"
    hover_background "images/ui/choice_hover.png"
    hover_sound "audio/sfx/ui_hover.ogg"
    activate_sound "audio/sfx/ui_click.ogg"
    padding (30, 10)

style choice_button_text is button_text:
    font "fonts/EBGaramond.ttf"
    size 32
    color "#d8d0c1"
    hover_color "#f4e4bb"
    xalign 0.5
    yalign 0.5
    text_align 0.5
    xsize 1120
    outlines [(1, "#000000aa", 0, 0)]

style quick_button is button:
    background Solid("#0a0d12cc")
    hover_background Solid("#252b35ee")
    padding (10, 5)
    hover_sound "audio/sfx/ui_hover.ogg"
    activate_sound "audio/sfx/ui_click.ogg"

style quick_button_text is button_text:
    font "fonts/Cinzel.ttf"
    size 20
    color "#a8a08f"
    hover_color "#e7d7ac"
    outlines [(1, "#000000aa", 0, 0)]

style phone_tab_button is button:
    background Solid("#11161dcc")
    hover_background Solid("#28313cee")
    selected_background Solid("#3a3328ee")
    padding (8, 4)

style phone_tab_button_text is button_text:
    font "fonts/Cinzel.ttf"
    size 18
    color "#9b9487"
    hover_color "#e5d5ad"
    selected_color "#e5d5ad"

style phone_close_button is button:
    background "images/ui/button_idle.png"
    hover_background "images/ui/button_hover.png"
    xsize 430
    ysize 68
    padding (10, 4)

style phone_close_button_text is button_text:
    font "fonts/Cinzel.ttf"
    size 22
    color "#cfc6b4"
    hover_color "#f0dfb6"
    xalign 0.5
    yalign 0.5

style pref_bar is bar:
    xsize 540
    ysize 22
    left_bar Solid("#8c6f4a")
    right_bar Solid("#262b33")
    thumb None
    thumb_shadow None

style pref_label is default:
    font "fonts/Cinzel.ttf"
    size 26
    color "#b9ae9a"

style ending_title is default:
    font "fonts/Cinzel.ttf"
    size 76
    color "#e5d8bb"
    outlines [(3, "#000000cc", 0, 0)]
    text_align 0.5

style ending_quote is default:
    font "fonts/EBGaramond.ttf"
    size 34
    italic True
    color "#b8b0a2"
    text_align 0.5


screen say(who, what):
    add SideImage() xpos 72 ypos 150 xsize 500 ysize 834
    window:
        id "window"
        style "say_window"
        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who" style "say_label"
        text what id "what" style "say_dialogue"
        imagebutton:
            idle "images/ui/arrow.png"
            xpos 1810
            ypos 322
            at ctc_blink
            action Return()


screen choice(items):
    modal True
    zorder 50
    add Solid("#00000044")
    vbox:
        xalign 0.5
        yalign 0.58
        spacing 16
        for item in items:
            button:
                style "choice_button"
                action item.action
                text item.caption style "choice_button_text"


screen quick_menu():
    zorder 100
    if quick_menu:
        hbox:
            xalign 0.985
            ypos 1018
            spacing 6
            textbutton "PHONE [phone_unread]" action Show("phone_app", tab="messages") style "quick_button" text_style "quick_button_text"
            textbutton "LOG" action ShowMenu("history") style "quick_button" text_style "quick_button_text"
            textbutton "SAVE" action ShowMenu("save") style "quick_button" text_style "quick_button_text"
            textbutton "LOAD" action ShowMenu("load") style "quick_button" text_style "quick_button_text"
            textbutton "SKIP" action Skip() style "quick_button" text_style "quick_button_text"
            textbutton "AUTO" action Preference("auto-forward", "toggle") style "quick_button" text_style "quick_button_text"
            textbutton "SETTINGS" action ShowMenu("preferences") style "quick_button" text_style "quick_button_text"


screen status_hud():
    zorder 80
    if current_chapter > 0 and not renpy.get_screen("main_menu"):
        if sanity < 35:
            add "images/effects/vignette.png" at low_sanity_pulse
        frame:
            xalign 0.992
            ypos 18
            background Solid("#080a0ed9")
            padding (12, 9)
            hbox:
                spacing 10
                add "images/ui/sanity_icon.png" zoom 0.46 yalign 0.5
                vbox:
                    spacing 4
                    hbox:
                        spacing 8
                        text "SANITY" style "pref_label" size 20
                        text sanity_state().upper() style "pref_label" size 20 color "#9e8d72"
                    frame:
                        xsize 238
                        ysize 12
                        background Solid("#242a34")
                        frame:
                            xsize max(2, int(238 * sanity / 100.0))
                            ysize 12
                            background Solid("#8f3030")


screen chapter_card(number, title):
    zorder 130
    add Solid("#050607")
    add "images/effects/vignette.png" alpha 0.55
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 16
        text "CHAPTER [number]" style "pref_label" size 28 xalign 0.5 color "#8e7c5d"
        text title style "ending_title" xalign 0.5
        text "DON'T LOOK BEHIND YOU" style "pref_label" size 20 xalign 0.5 color "#665d4e"
    key "dismiss" action Return()
    timer 3.6 action Return()


screen investigate(hotspots, prompt="Something here is waiting to be noticed."):
    modal True
    zorder 45
    default hover_name = ""
    for idx, spot in enumerate(hotspots):
        button:
            xpos spot["x"]
            ypos spot["y"]
            xysize (spot["w"], spot["h"])
            background None
            hover_background Solid("#e8d9b018")
            action Return(idx)
            hovered SetScreenVariable("hover_name", spot["name"])
            unhovered SetScreenVariable("hover_name", "")
            add "images/effects/particle_big.png" at hotspot_pulse xalign 0.5 yalign 0.5
    frame:
        xalign 0.5
        ypos 24
        background Solid("#080a0ed0")
        padding (24, 10)
        text "INVESTIGATE" style "pref_label" size 22
    frame:
        xalign 0.5
        yalign 0.965
        xsize 1200
        background Solid("#080a0ed9")
        padding (24, 12)
        text (hover_name if hover_name else prompt) style "default" size 28 xalign 0.5 text_align 0.5
    textbutton "STEP AWAY":
        xalign 0.985
        yalign 0.88
        style "phone_close_button"
        text_style "phone_close_button_text"
        action Return("leave")
    key "game_menu" action Return("leave")


screen phone_app(tab="messages"):
    modal True
    zorder 90
    default phone_tab = tab
    on "show" action Function(mark_phone_read)
    add Solid("#000000aa")
    frame:
        xalign 0.5
        yalign 0.5
        xysize (566, 922)
        background Frame("images/ui/phone_frame.png", 44, 110)
        padding (42, 118, 42, 72)
        vbox:
            xfill True
            yfill True
            spacing 10
            hbox:
                xfill True
                text "3:00" style "pref_label" size 30 color "#c9b88f"
                text "NO SERVICE" style "pref_label" size 17 color "#675f52" xalign 1.0
            hbox:
                spacing 5
                textbutton "MESSAGES" action SetScreenVariable("phone_tab", "messages") style "phone_tab_button" text_style "phone_tab_button_text"
                textbutton "CALLS" action SetScreenVariable("phone_tab", "calls") style "phone_tab_button" text_style "phone_tab_button_text"
                textbutton "PHOTOS" action SetScreenVariable("phone_tab", "photos") style "phone_tab_button" text_style "phone_tab_button_text"
            frame:
                xfill True
                yfill True
                background Solid("#080c11cc")
                padding (12, 12)
                if phone_tab == "messages":
                    use phone_messages
                elif phone_tab == "calls":
                    use phone_calls
                else:
                    use phone_photos
            textbutton "PUT IT AWAY" action Hide("phone_app") style "phone_close_button" text_style "phone_close_button_text" xalign 0.5


screen phone_messages():
    viewport:
        mousewheel True
        draggable True
        xfill True
        yfill True
        vbox:
            spacing 9
            xfill True
            if not phone_messages:
                text "No messages yet." style "pref_label" size 24
            for msg in phone_messages[::-1]:
                frame:
                    xfill True
                    background Solid("#161d27e8")
                    padding (13, 9)
                    vbox:
                        spacing 2
                        hbox:
                            xfill True
                            text msg["from"] style "pref_label" size 19 color ("#c7a7a7" if msg["from"] == "MAYA" else "#9fb6bd")
                            text msg["time"] style "pref_label" size 16 color "#6e6658" xalign 1.0
                        text msg["text"] style "default" size 25 xsize 410 line_spacing 3


screen phone_calls():
    viewport:
        mousewheel True
        draggable True
        xfill True
        yfill True
        vbox:
            spacing 9
            xfill True
            if not phone_calls:
                text "No calls." style "pref_label" size 24
            for call in phone_calls[::-1]:
                frame:
                    xfill True
                    background Solid("#161d27e8")
                    padding (13, 10)
                    hbox:
                        xfill True
                        vbox:
                            text call["from"] style "pref_label" size 21
                            text call["time"] style "default" size 19 color "#7e7668"
                        text ("ANSWERED" if call["answered"] else "MISSED") style "pref_label" size 17 xalign 1.0 color ("#7f9f8f" if call["answered"] else "#9d5a5a")


screen phone_photos():
    viewport:
        mousewheel True
        draggable True
        xfill True
        yfill True
        vbox:
            spacing 12
            if not persistent.cg_phone_photo and not renpy.seen_image("cg girl first") and not renpy.seen_image("cg mirror"):
                text "No photos." style "pref_label" size 24
            if persistent.cg_phone_photo:
                add im.Scale("images/cg/cg_phone_photo.jpg", 260, 346) xalign 0.5
                text "3:00 AM — taken from inside your room." style "default" size 22 xalign 0.5 text_align 0.5
            if renpy.seen_image("cg girl first"):
                add im.Scale("images/cg/cg_girl_first.jpg", 420, 236) xalign 0.5
                text "The hallway. She was not there when you looked again." style "default" size 22 xalign 0.5 text_align 0.5
            if renpy.seen_image("cg mirror"):
                add im.Scale("images/cg/cg_mirror.jpg", 420, 236) xalign 0.5
                text "The bathroom mirror." style "default" size 22 xalign 0.5 text_align 0.5
            if renpy.seen_image("cg hidden room"):
                add im.Scale("images/cg/cg_hidden_room.jpg", 420, 236) xalign 0.5
                text "Behind the wardrobe." style "default" size 22 xalign 0.5 text_align 0.5


screen phone_alert(sender, body, kind="text"):
    zorder 150
    frame at phone_alert_appear:
        xalign 0.99
        ypos 64
        xsize 560
        background Solid("#0b1118ee")
        padding (24, 16)
        vbox:
            spacing 4
            hbox:
                xfill True
                text "NEW MESSAGE" style "pref_label" size 18 color "#8c7b5d"
                text sender style "pref_label" size 18 color "#a9bfc5" xalign 1.0
            text body style "default" size 25 xsize 500 line_spacing 3


screen incoming_call(caller="UNKNOWN", subtitle="3:00 AM"):
    modal True
    zorder 140
    add Solid("#020406f2")
    add "images/effects/scanlines.png" alpha 0.3
    vbox:
        xalign 0.5
        yalign 0.36
        spacing 12
        text subtitle style "pref_label" size 26 xalign 0.5 color "#7e7464"
        text "INCOMING CALL" style "pref_label" size 24 xalign 0.5 color "#8a5b5b"
        text caller style "ending_title" size 62 xalign 0.5
        text "........................" style "pref_label" size 22 xalign 0.5 at ctc_blink
    hbox:
        xalign 0.5
        yalign 0.68
        spacing 42
        textbutton "ANSWER" action Return("answer") style "menu_button" text_style "menu_button_text"
        textbutton "IGNORE" action Return("ignore") style "menu_button" text_style "menu_button_text"
    on "show" action Play("sound", "audio/sfx/phone_ring.ogg", loop=True)
    on "hide" action Stop("sound", fadeout=0.3)


screen ending_stamp(number, title, quote):
    modal True
    zorder 140
    add Solid("#000000e0")
    add "images/effects/vignette.png" alpha 0.7
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 18
        text "ENDING [number] OF 4" style "pref_label" size 25 xalign 0.5 color "#7d715c"
        add im.Scale("images/ui/ending_seal.png", 560, 192) xalign 0.5
        text title style "ending_title" xalign 0.5
        text quote style "ending_quote" xsize 1200 xalign 0.5
        textbutton "CONTINUE" action Return() style "menu_button" text_style "menu_button_text" xalign 0.5


screen main_menu():
    tag menu
    add "images/backgrounds/bg_menu.jpg"
    add "images/effects/vignette.png"
    add "images/effects/scanlines.png" alpha 0.18
    add Solid("#03050966")
    add "images/ui/logo.png" at logo_float
    if persistent.secret_seen:
        text "YOU LOOKED BACK." style "pref_label" size 24 xalign 0.5 ypos 512 color "#8e3f3f"
    vbox:
        xalign 0.5
        ypos 560
        spacing 8
        style_prefix "menu"
        textbutton "NEW GAME" action Start()
        textbutton "CONTINUE" action ShowMenu("load")
        textbutton "GALLERY" action ShowMenu("gallery")
        textbutton "SETTINGS" action ShowMenu("preferences")
        textbutton "CREDITS" action ShowMenu("credits")
        textbutton "QUIT" action Quit(confirm=True)
    text "A short horror story in seven nights." style "pref_label" size 20 xalign 0.5 yalign 0.965 color "#6e6658"


screen save():
    tag menu
    use file_slots("SAVE", "save")


screen load():
    tag menu
    use file_slots("LOAD", "load")


screen file_slots(title, mode):
    add "images/backgrounds/bg_menu.jpg"
    add Solid("#030509cc")
    add "images/effects/vignette.png" alpha 0.5
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1580, 900)
        background Solid("#080b10ee")
        padding (36, 26)
        vbox:
            spacing 16
            hbox:
                xfill True
                text title style "ending_title" size 48
                textbutton "BACK" action Return() style "quick_button" text_style "quick_button_text" xalign 1.0 yalign 0.5
            grid 3 2:
                spacing 18
                for i in range(1, 7):
                    button:
                        xysize (480, 360)
                        background Solid("#121821")
                        hover_background Solid("#1f2834")
                        action (FileSave(i, confirm=False) if mode == "save" else FileLoad(i, confirm=False))
                        padding (10, 8)
                        vbox:
                            spacing 3
                            add FileScreenshot(i) size (456, 257)
                            hbox:
                                xfill True
                                text "SLOT [i]" style "pref_label" size 20
                                text FileTime(i, format="%b %d  %H:%M", empty="EMPTY") style "pref_label" size 16 xalign 1.0 color "#7e7668"
                            text FileSaveName(i, empty="—") style "default" size 20


screen preferences():
    tag menu
    add "images/backgrounds/bg_menu.jpg"
    add Solid("#030509cc")
    add "images/effects/vignette.png" alpha 0.5
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1080, 880)
        background Solid("#080b10ee")
        padding (48, 36)
        vbox:
            spacing 22
            hbox:
                xfill True
                text "SETTINGS" style "ending_title" size 48
                textbutton "BACK" action Return() style "quick_button" text_style "quick_button_text" xalign 1.0 yalign 0.5
            text "MUSIC" style "pref_label"
            bar value Preference("music volume") style "pref_bar"
            text "SOUND" style "pref_label"
            bar value Preference("sound volume") style "pref_bar"
            text "TEXT SPEED" style "pref_label"
            bar value Preference("text speed") style "pref_bar"
            text "AUTO-FORWARD" style "pref_label"
            bar value Preference("auto-forward time") style "pref_bar"
            hbox:
                spacing 14
                textbutton "WINDOW" action Preference("display", "window") style "quick_button" text_style "quick_button_text"
                textbutton "FULLSCREEN" action Preference("display", "fullscreen") style "quick_button" text_style "quick_button_text"
                textbutton "SKIP UNSEEN" action Preference("skip", "toggle") style "quick_button" text_style "quick_button_text"
                textbutton "TRANSITIONS" action Preference("transitions", "toggle") style "quick_button" text_style "quick_button_text"


screen history():
    tag menu
    add "images/backgrounds/bg_menu.jpg"
    add Solid("#030509e6")
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1500, 900)
        background Solid("#080b10ee")
        padding (36, 26)
        vbox:
            spacing 14
            hbox:
                xfill True
                text "HISTORY" style "ending_title" size 46
                textbutton "BACK" action Return() style "quick_button" text_style "quick_button_text" xalign 1.0 yalign 0.5
            viewport:
                mousewheel True
                draggable True
                xfill True
                yfill True
                vbox:
                    spacing 12
                    for h in _history_list:
                        vbox:
                            spacing 2
                            if h.who:
                                text h.who style "pref_label" size 22 color "#c7b28a"
                            text h.what style "default" size 27 xsize 1360


screen gallery():
    tag menu
    add "images/backgrounds/bg_menu.jpg"
    add Solid("#030509cc")
    add "images/effects/vignette.png" alpha 0.5
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1760, 980)
        background Solid("#080b10ee")
        padding (30, 22)
        vbox:
            spacing 12
            hbox:
                xfill True
                text "GALLERY" style "ending_title" size 46
                textbutton "BACK" action ShowMenu("main_menu") style "quick_button" text_style "quick_button_text" xalign 1.0 yalign 0.5
            vpgrid:
                cols 4
                spacing 14
                xalign 0.5
                yfill True
                for entry in CG_ENTRIES:
                    $ unlocked = renpy.seen_image(entry["image"]) or (entry["persistent"] is not None and getattr(persistent, entry["persistent"], False))
                    button:
                        xysize (410, 252)
                        background Solid("#0d1218")
                        hover_background Solid("#1b2430")
                        action (Show("cg_view", entry=entry) if unlocked else NullAction())
                        padding (8, 6)
                        vbox:
                            spacing 3
                            if unlocked:
                                add im.Scale(entry["file"], 394, 222) xalign 0.5
                                text entry["title"] style "pref_label" size 19 xalign 0.5 text_align 0.5
                            else:
                                add im.Scale("images/ui/gallery_locked.png", 394, 222) xalign 0.5
                                text "LOCKED" style "pref_label" size 19 xalign 0.5 color "#554f46"
            hbox:
                xalign 0.5
                spacing 22
                text "ENDINGS" style "pref_label" size 20
                text ("I  THE TRUTH" if persistent.ending_truth else "I  —") style "pref_label" size 19 color ("#b7a57f" if persistent.ending_truth else "#4f4a42")
                text ("II  YOU WERE NEVER ALONE" if persistent.ending_alone else "II  —") style "pref_label" size 19 color ("#b7a57f" if persistent.ending_alone else "#4f4a42")
                text ("III  THE SEVENTH CALL" if persistent.ending_call else "III  —") style "pref_label" size 19 color ("#b7a57f" if persistent.ending_call else "#4f4a42")
                text ("IV  NEW GAME" if persistent.ending_newgame else "IV  —") style "pref_label" size 19 color ("#b7a57f" if persistent.ending_newgame else "#4f4a42")


screen cg_view(entry):
    modal True
    zorder 110
    add Solid("#000000")
    add entry["file"] at ending_cg
    add "images/effects/vignette.png" alpha 0.5
    frame:
        xalign 0.5
        yalign 0.965
        background Solid("#000000c0")
        padding (30, 12)
        text entry["title"] style "pref_label" size 24
    textbutton "CLOSE" action Hide("cg_view") style "quick_button" text_style "quick_button_text" xalign 0.98 yalign 0.04


screen credits():
    tag menu
    add "images/backgrounds/bg_menu.jpg"
    add Solid("#030509dd")
    add "images/effects/vignette.png" alpha 0.5
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1200, 900)
        background Solid("#080b10ee")
        padding (48, 32)
        vbox:
            spacing 18
            text "CREDITS" style "ending_title" size 50 xalign 0.5
            viewport:
                mousewheel True
                draggable True
                xfill True
                yfill True
                vbox:
                    spacing 14
                    xfill True
                    text "DON'T LOOK BEHIND YOU" style "pref_label" size 30 xalign 0.5
                    text "A short horror visual novel in seven nights." style "ending_quote" size 27 xalign 0.5
                    text "STORY, ART, AND MUSIC\nCreated procedurally for this game." style "pref_label" size 22 xalign 0.5 text_align 0.5
                    text "ENGINE\nRen'Py 8.3.7" style "pref_label" size 22 xalign 0.5 text_align 0.5
                    text "TYPEFACES\nCinzel — Cormorant Garamond — EB Garamond\nLicensed under the SIL Open Font License." style "pref_label" size 22 xalign 0.5 text_align 0.5
                    text "All characters and events in this work are fictional.\nAny resemblance to real persons or places is coincidental." style "ending_quote" size 23 xalign 0.5 text_align 0.5
                    text "Thank you for listening." style "pref_label" size 24 xalign 0.5
            textbutton "BACK" action ShowMenu("main_menu") style "menu_button" text_style "menu_button_text" xalign 0.5


screen credits_end():
    modal True
    zorder 150
    add Solid("#020304")
    add "images/effects/vignette.png" alpha 0.6
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1200, 900)
        background Solid("#080b10ee")
        padding (48, 32)
        vbox:
            spacing 18
            text "CREDITS" style "ending_title" size 50 xalign 0.5
            viewport:
                mousewheel True
                draggable True
                xfill True
                yfill True
                vbox:
                    spacing 14
                    xfill True
                    text "DON'T LOOK BEHIND YOU" style "pref_label" size 30 xalign 0.5
                    text "Thank you for staying until the end." style "ending_quote" size 28 xalign 0.5
                    text "STORY, ART, AND MUSIC\nCreated procedurally for this game." style "pref_label" size 22 xalign 0.5 text_align 0.5
                    text "ENGINE\nRen'Py 8.3.7" style "pref_label" size 22 xalign 0.5 text_align 0.5
                    text "TYPEFACES\nCinzel — Cormorant Garamond — EB Garamond\nLicensed under the SIL Open Font License." style "pref_label" size 22 xalign 0.5 text_align 0.5
                    text "All characters and events in this work are fictional." style "ending_quote" size 23 xalign 0.5
                    text "The phone is still ringing." style "pref_label" size 22 xalign 0.5 color "#795d5d"
            textbutton "RETURN TO TITLE" action Return() style "menu_button" text_style "menu_button_text" xalign 0.5

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#000000d8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        background Solid("#0b0f15f2")
        padding (40, 30)
        vbox:
            spacing 22
            text message style "default" size 30 xalign 0.5 text_align 0.5
            hbox:
                xalign 0.5
                spacing 24
                textbutton "YES" action yes_action style "menu_button" text_style "menu_button_text"
                textbutton "NO" action no_action style "menu_button" text_style "menu_button_text"

screen notify(message):
    zorder 200
    frame at notify_appear:
        xalign 0.5
        ypos 42
        background Solid("#0a0e14ee")
        padding (26, 12)
        text message style "default" size 25
    timer 3.0 action Hide("notify")

init python:
    config.overlay_screens.append("quick_menu")
    config.overlay_screens.append("status_hud")
