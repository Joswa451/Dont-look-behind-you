style bag_item_button is button:
    xfill True
    background Solid("#121821dd")
    hover_background Solid("#25303dff")
    selected_background Solid("#3a3328ff")
    padding (14, 9)

style bag_item_button_text is button_text:
    font "fonts/EBGaramond.ttf"
    size 27
    color "#cfc5b3"
    hover_color "#f3e0b4"
    selected_color "#f3e0b4"
    xalign 0.0

style journal_item_button is button:
    xfill True
    background Solid("#111720dd")
    hover_background Solid("#202a36ff")
    selected_background Solid("#373126ff")
    padding (12, 8)

style journal_item_button_text is button_text:
    font "fonts/EBGaramond.ttf"
    size 24
    color "#c9beab"
    hover_color "#f1dfb5"
    selected_color "#f1dfb5"
    xalign 0.0


screen inventory_screen():
    modal True
    zorder 95
    default selected = next((k for k in ITEM_ORDER if k in inventory), None)
    add Solid("#000000b8")
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1500, 930)
        background Solid("#080b10f4")
        padding (32, 24)
        vbox:
            spacing 14
            hbox:
                xfill True
                text "BAG" style "ending_title" size 46
                text "ITEMS [len(inventory)]" style "pref_label" size 22 xalign 1.0 yalign 0.5 color "#8f826d"
            hbox:
                spacing 22
                frame:
                    xsize 430
                    yfill True
                    background Solid("#05080ccc")
                    padding (14, 12)
                    viewport:
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True
                        vbox:
                            spacing 7
                            for item_key in ITEM_ORDER:
                                if item_key in inventory:
                                    textbutton ITEMS[item_key]["name"]:
                                        style "bag_item_button"
                                        text_style "bag_item_button_text"
                                        action SetScreenVariable("selected", item_key)
                frame:
                    xfill True
                    yfill True
                    background Solid("#0b1017dd")
                    padding (24, 20)
                    if selected:
                        vbox:
                            spacing 12
                            text ITEMS[selected]["name"] style "ending_title" size 34
                            text ITEMS[selected]["desc"] style "default" size 29 xsize 900
                            text "USE" style "pref_label" size 20 color "#8f826d"
                            text ITEMS[selected]["use"] style "default" size 27 xsize 900 color "#c9c0b0"
                            null height 8
                            if selected == "phone":
                                textbutton "OPEN PHONE" action [Hide("inventory_screen"), Show("phone_app", tab="messages")] style "phone_close_button" text_style "phone_close_button_text"
                            elif selected == "photograph":
                                textbutton "STUDY THE PHOTOGRAPH" action [Hide("inventory_screen"), Show("evidence_journal", start="old_photo")] style "phone_close_button" text_style "phone_close_button_text"
                            elif selected == "iris_diary":
                                textbutton "READ THE DIARY" action [Hide("inventory_screen"), Show("evidence_journal", start="iris_diary")] style "phone_close_button" text_style "phone_close_button_text"
                            elif selected == "bargain_tape":
                                textbutton "PLAY THE TAPE" action Function(use_item, selected) style "phone_close_button" text_style "phone_close_button_text"
                            elif selected == "flashlight":
                                textbutton ("TURN OFF" if flashlight_on else "TURN ON") action Function(use_item, selected) style "phone_close_button" text_style "phone_close_button_text"
                            else:
                                textbutton "USE" action Function(use_item, selected) style "phone_close_button" text_style "phone_close_button_text"
                    else:
                        text "Your bag is empty." style "pref_label" size 28 xalign 0.5 yalign 0.5
            textbutton "CLOSE" action Hide("inventory_screen") style "phone_close_button" text_style "phone_close_button_text" xalign 0.5
    key "game_menu" action Hide("inventory_screen")
    key "i" action Hide("inventory_screen")


screen evidence_journal(start=None):
    modal True
    zorder 96
    default selected = start if start in clues else next((k for k in EVIDENCE_ORDER if k in clues), None)
    add Solid("#000000b8")
    frame:
        xalign 0.5
        yalign 0.5
        xysize (1580, 950)
        background Solid("#080b10f4")
        padding (32, 24)
        vbox:
            spacing 14
            hbox:
                xfill True
                text "EVIDENCE JOURNAL" style "ending_title" size 44
                text "REVIEWED [len(evidence_reviewed)] / [len(clues)]" style "pref_label" size 21 xalign 1.0 yalign 0.5 color "#8f826d"
            hbox:
                spacing 20
                frame:
                    xsize 450
                    yfill True
                    background Solid("#05080ccc")
                    padding (14, 12)
                    viewport:
                        mousewheel True
                        draggable True
                        xfill True
                        yfill True
                        vbox:
                            spacing 6
                            if not clues:
                                text "Nothing collected yet." style "pref_label" size 24
                            for evidence_key in EVIDENCE_ORDER:
                                if evidence_key in clues:
                                    textbutton CLUE_NAMES[evidence_key]:
                                        style "journal_item_button"
                                        text_style "journal_item_button_text"
                                        action [SetScreenVariable("selected", evidence_key), Function(review_evidence, evidence_key)]
                frame:
                    xfill True
                    yfill True
                    background Solid("#0b1017dd")
                    padding (24, 20)
                    if selected and selected in clues:
                        $ meta = EVIDENCE_META.get(selected, {"chapter": "?", "source": "Unknown", "note": CLUE_NAMES[selected]})
                        vbox:
                            spacing 12
                            text CLUE_NAMES[selected] style "ending_title" size 32
                            text "CHAPTER [meta['chapter']]  //  [meta['source']]" style "pref_label" size 20 color "#8f826d"
                            text meta["note"] style "default" size 28 xsize 940 line_spacing 7
                            null height 8
                            if selected in evidence_reviewed:
                                text "REVIEWED" style "pref_label" size 19 color "#8d9c86"
                            else:
                                textbutton "MARK AS REVIEWED" action Function(review_evidence, selected) style "phone_close_button" text_style "phone_close_button_text"
                            null height 6
                            text "MAYA  [maya_relationship().upper()]" style "pref_label" size 19 color "#b58f8f"
                            text "IRIS  [iris_relationship().upper()]" style "pref_label" size 19 color "#8fa9b8"
                            text "LISTENER  [listener_relationship().upper()]" style "pref_label" size 19 color "#8a8274"
                    else:
                        text "Choose an entry to read." style "pref_label" size 26 xalign 0.5 yalign 0.5
            hbox:
                xalign 0.5
                spacing 16
                if deduction_unlocked:
                    text "DEDUCTION: The seventh name was always yours." style "pref_label" size 20 color "#b9a77f"
                else:
                    text "Review eight entries to form a deduction." style "pref_label" size 19 color "#6f675a"
            textbutton "CLOSE" action Hide("evidence_journal") style "phone_close_button" text_style "phone_close_button_text" xalign 0.5
    key "game_menu" action Hide("evidence_journal")
    key "j" action Hide("evidence_journal")


screen phone_reply(prompt, replies):
    modal True
    zorder 145
    add Solid("#000000c4")
    frame:
        xalign 0.5
        yalign 0.5
        xysize (720, 760)
        background Frame("images/ui/phone_frame.png", 44, 110)
        padding (52, 130, 52, 76)
        vbox:
            spacing 18
            xfill True
            text "MESSAGES" style "pref_label" size 22 xalign 0.5 color "#8c7b5d"
            text prompt style "default" size 29 xsize 600 xalign 0.5 text_align 0.5
            null height 12
            for caption, value in replies:
                textbutton caption action Return(value) style "choice_button" text_style "choice_button_text" xalign 0.5
    key "game_menu" action NullAction()


screen survival_hide(cue, round_number, limit=8.0):
    modal True
    zorder 160
    add Solid("#010204f2")
    add "images/effects/scanlines.png" alpha 0.3
    add "images/effects/vignette.png" alpha 0.7
    vbox:
        xalign 0.5
        yalign 0.23
        spacing 12
        text "DON'T LET IT HEAR YOU" style "pref_label" size 24 xalign 0.5 color "#8a5b5b"
        text "[round_number] OF 3" style "ending_title" size 42 xalign 0.5
        text cue style "ending_quote" size 30 xsize 1100 xalign 0.5 text_align 0.5
    vbox:
        xalign 0.5
        yalign 0.7
        spacing 16
        textbutton "UNDER THE STAIRS" action Return("stairs") style "choice_button" text_style "choice_button_text" xalign 0.5
        textbutton "BEHIND THE BOILER" action Return("boiler") style "choice_button" text_style "choice_button_text" xalign 0.5
        textbutton "INSIDE THE LAUNDRY ROOM" action Return("laundry") style "choice_button" text_style "choice_button_text" xalign 0.5
    frame:
        xalign 0.5
        yalign 0.94
        background Solid("#160607dd")
        padding (18, 8)
        text "MOVE. IT IS ALREADY LISTENING." style "pref_label" size 20 color "#b18a8a"
    timer limit action Return("timeout")
    key "game_menu" action NullAction()


screen horror_flash():
    zorder 65
    add "images/effects/glitch_1.png" alpha 0.22
    add "images/effects/glitch_2.png" alpha 0.12
    timer 0.18 action Hide("horror_flash")


screen sanity_ambience():
    zorder 60
    if current_chapter > 0 and not renpy.get_screen("main_menu"):
        if sanity < 35:
            add "images/effects/scanlines.png" alpha 0.12
        timer 13.0 repeat True action Function(horror_tick)

init python:
    config.overlay_screens.append("sanity_ambience")
