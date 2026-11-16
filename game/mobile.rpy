init 100:
    style say_window:
        variant "small"
        ysize 500

    style say_dialogue:
        variant "small"
        xpos 600
        ypos 100
        xsize 1260
        size 48
        line_spacing 12

    style say_label:
        variant "small"
        size 40

    style menu_button:
        variant "small"
        xsize 740
        ysize 80

    style menu_button_text:
        variant "small"
        size 36

    style choice_button:
        variant "small"
        xsize 1640
        ysize 124

    style choice_button_text:
        variant "small"
        size 46
        xsize 1500

    style quick_button_text:
        variant "small"
        size 26

    style phone_tab_button_text:
        variant "small"
        size 22

    style phone_close_button:
        variant "small"
        xsize 520
        ysize 86

    style phone_close_button_text:
        variant "small"
        size 28

    style pref_bar:
        variant "small"
        ysize 28

    style pref_label:
        variant "small"
        size 32

    style bag_item_button_text:
        variant "small"
        size 36

    style journal_item_button_text:
        variant "small"
        size 32

    style ending_quote:
        variant "small"
        size 38

init 100 python:
    if renpy.variant("android"):
        config.keymap["rollback"] = [
            key for key in config.keymap["rollback"] if key != "K_AC_BACK"
        ]
        if "K_AC_BACK" not in config.keymap["game_menu"]:
            config.keymap["game_menu"].append("K_AC_BACK")
