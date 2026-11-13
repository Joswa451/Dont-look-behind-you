image bg bedroom = "images/backgrounds/bg_bedroom.png"
image bg bedroom day = "images/backgrounds/bg_bedroom_day.jpg"
image bg livingroom = "images/backgrounds/bg_livingroom.jpg"
image bg hallway = "images/backgrounds/bg_hallway.jpg"
image bg bathroom = "images/backgrounds/bg_bathroom.jpg"
image bg kitchen = "images/backgrounds/bg_kitchen.jpg"
image bg school = "images/backgrounds/bg_school.jpg"
image bg classroom = "images/backgrounds/bg_classroom.jpg"
image bg street = "images/backgrounds/bg_street.jpg"
image bg underground = "images/backgrounds/bg_underground.jpg"
image bg basement = "images/backgrounds/bg_basement.jpg"
image bg hiddenroom = "images/backgrounds/bg_hiddenroom.jpg"
image bg void = "images/backgrounds/bg_void.jpg"
image bg menu = "images/backgrounds/bg_menu.jpg"

image cg phone photo = "images/cg/cg_phone_photo.jpg"
image cg girl first = "images/cg/cg_girl_first.jpg"
image cg jumpscare = "images/cg/cg_jumpscare.jpg"
image cg mirror = "images/cg/cg_mirror.jpg"
image cg hidden room = "images/cg/cg_hidden_room.jpg"
image cg parents = "images/cg/cg_parents.jpg"
image cg bargain flashback = "images/cg/cg_bargain_flashback.jpg"
image cg confrontation = "images/cg/cg_confrontation.jpg"
image cg ending truth = "images/cg/cg_ending_truth.jpg"
image cg ending alone = "images/cg/cg_ending_alone.jpg"
image cg ending call = "images/cg/cg_ending_call.jpg"
image cg ending newgame = "images/cg/cg_ending_newgame.jpg"

init python:
    config.side_image_only_not_showing = True

    for _char in ("ethan", "maya", "girl", "entity", "mom", "dad"):
        for _expr in ("neutral", "happy", "sad", "angry", "scared", "crying",
                      "surprised", "evil", "shocked"):
            renpy.image(
                _char + " " + _expr,
                "images/characters/%s_%s.png" % (_char, _expr),
            )

    # Dialogue portraits use the cast's established art and color language.
    # The parental portraits are cropped from their existing spectral CG.
    for _char, _asset in (("ethan", "ethan_neutral"),
                          ("maya", "maya_neutral"),
                          ("girl", "girl_neutral"),
                          ("entity", "entity_evil"),
                          ("mom", "mom_neutral"),
                          ("dad", "dad_neutral")):
        renpy.image(("side", _char), Transform(
            "images/characters/%s.png" % _asset,
            xysize=(500, 834),
        ))

    CG_ENTRIES = [
        {"image": "cg phone photo", "file": "images/cg/cg_phone_photo.jpg",
         "title": "3:00 AM", "persistent": "cg_phone_photo"},
        {"image": "cg girl first", "file": "images/cg/cg_girl_first.jpg",
         "title": "The Girl in the Hallway", "persistent": None},
        {"image": "cg jumpscare", "file": "images/cg/cg_jumpscare.jpg",
         "title": "Don't Open the Door", "persistent": None},
        {"image": "cg mirror", "file": "images/cg/cg_mirror.jpg",
         "title": "Let Me Out", "persistent": None},
        {"image": "cg hidden room", "file": "images/cg/cg_hidden_room.jpg",
         "title": "The Hidden Room", "persistent": None},
        {"image": "cg parents", "file": "images/cg/cg_parents.jpg",
         "title": "What We Did", "persistent": None},
        {"image": "cg bargain flashback", "file": "images/cg/cg_bargain_flashback.jpg",
         "title": "The Bargain", "persistent": None},
        {"image": "cg confrontation", "file": "images/cg/cg_confrontation.jpg",
         "title": "The Listener", "persistent": None},
        {"image": "cg ending truth", "file": "images/cg/cg_ending_truth.jpg",
         "title": "Ending I — The Truth", "persistent": None},
        {"image": "cg ending alone", "file": "images/cg/cg_ending_alone.jpg",
         "title": "Ending II — You Were Never Alone", "persistent": None},
        {"image": "cg ending call", "file": "images/cg/cg_ending_call.jpg",
         "title": "Ending III — The Seventh Call", "persistent": None},
        {"image": "cg ending newgame", "file": "images/cg/cg_ending_newgame.jpg",
         "title": "Ending IV — New Game", "persistent": None},
    ]
