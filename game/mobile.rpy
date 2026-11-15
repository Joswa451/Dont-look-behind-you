init 100 python:
    if renpy.variant("small"):
        style.say_window.ysize = 500
        style.say_dialogue.xpos = 600
        style.say_dialogue.ypos = 100
        style.say_dialogue.xsize = 1260
        style.say_dialogue.size = 48
        style.say_dialogue.line_spacing = 12
        style.say_label.size = 40
        style.menu_button.xsize = 740
        style.menu_button.ysize = 80
        style.menu_button_text.size = 36
        style.choice_button.xsize = 1640
        style.choice_button.ysize = 124
        style.choice_button_text.size = 46
        style.choice_button_text.xsize = 1500
        style.quick_button_text.size = 26
        style.phone_tab_button_text.size = 22
        style.phone_close_button.xsize = 520
        style.phone_close_button.ysize = 86
        style.phone_close_button_text.size = 28
        style.pref_bar.ysize = 28
        style.pref_label.size = 32
        style.bag_item_button_text.size = 36
        style.journal_item_button_text.size = 32
        style.ending_quote.size = 38

    if renpy.variant("android"):
        config.keymap["rollback"] = [
            key for key in config.keymap["rollback"] if key != "K_AC_BACK"
        ]
        if "K_AC_BACK" not in config.keymap["game_menu"]:
            config.keymap["game_menu"].append("K_AC_BACK")
