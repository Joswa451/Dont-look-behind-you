default sanity = 80
default trust_maya = 0
default clues = set()
default current_chapter = 0
default chapter_title = ""

default phone_messages = []
default phone_calls = []
default phone_unread = 0
default phone_photo_unlocked = False

default remembered = False
default destroyed_box = False
default kept_box = False
default answered_seventh = False
default saved_maya = False
default knows_iris = False
default told_maya_truth = False
default maya_stayed = False
default key_hidden_room = False
default ch1_finished = False
default ch2_finished = False
default ch3_finished = False
default ch4_finished = False
default ch5_finished = False
default ch6_finished = False

default persistent.ending_truth = False
default persistent.ending_alone = False
default persistent.ending_call = False
default persistent.ending_newgame = False
default persistent.secret_seen = False
default persistent.cg_phone_photo = False

init -5 python:
    SANITY_LOSS_MULTIPLIER = 0.55

    CLUE_NAMES = {
        "old_photo": "A photograph with a scratched-out face",
        "scratches": "Child-height scratches in the closet",
        "handprint": "A handprint on the inside of the mirror",
        "answering_machine": "Mom's voice on the old answering machine",
        "fire_record": "The St. Agnes fire, 2009",
        "blueprint": "A hidden room behind the wardrobe",
        "case_file": "A case file with no body",
        "mom_email": "An email from six years ago",
        "maya_notes": "Maya's folder on Ashgrove",
        "girl_in_hall": "The girl in the hallway",
        "iris_name": "Her name is Iris Vale",
        "music_box": "A music box engraved I.V.",
        "drawings": "Children's drawings of the listening room",
        "name_list": "A list of names carved into the wall",
        "boiler_handprint": "Something breathing in the basement",
        "mom_call": "A call from Mom's old number",
        "mirror": "Your reflection wrote LET ME OUT",
        "entity_saw_you": "It has seen you",
        "key": "A small brass key",
        "bargain_tape": "Your parents' bargain on tape",
        "iris_diary": "Iris's diary",
        "photo_iris": "A photograph of you and Iris",
        "altar": "The altar in the hidden room",
        "name_list_hidden": "Seven names. Yours is last.",
    }

    def clamp(value, low, high):
        return max(low, min(high, value))

    def change_sanity(amount, silent=False):
        if amount < 0:
            amount = -max(1, int(-amount * SANITY_LOSS_MULTIPLIER + 0.5))
        store.sanity = clamp(store.sanity + amount, 0, 100)
        if not silent and amount < 0:
            if store.sanity <= 0:
                renpy.notify("Your mind is somewhere else now.")
            elif store.sanity <= 20:
                renpy.notify("You can hear your own heartbeat.")
            elif store.sanity <= 40:
                renpy.notify("The room feels darker than it did.")
        return store.sanity

    def gain_trust(amount, silent=False):
        store.trust_maya = clamp(store.trust_maya + amount, 0, 10)
        if not silent and amount > 0:
            renpy.notify("Maya trusts you a little more.")
        return store.trust_maya

    def add_clue(key, silent=False):
        if key not in CLUE_NAMES:
            raise Exception("Unknown clue: %s" % key)
        if key not in store.clues:
            store.clues.add(key)
            if not silent:
                renpy.notify("New clue: " + CLUE_NAMES[key])

    def has_clue(key):
        return key in store.clues

    def clue_count():
        return len(store.clues)

    def add_message(sender, body, stamp="3:00 AM", kind="text"):
        store.phone_messages.append({
            "from": sender,
            "text": body,
            "time": stamp,
            "kind": kind,
        })
        store.phone_unread += 1
        if kind == "photo":
            store.phone_photo_unlocked = True
            store.persistent.cg_phone_photo = True
        return store.phone_messages[-1]

    def add_call(sender, stamp="3:00 AM", answered=False):
        store.phone_calls.append({
            "from": sender,
            "time": stamp,
            "answered": answered,
        })

    def mark_phone_read():
        store.phone_unread = 0

    def push_message(sender, body, stamp="3:00 AM", alert=True, delay=2.2, kind="text"):
        add_message(sender, body, stamp, kind)
        if alert:
            renpy.sound.play("audio/sfx/phone_notify.ogg")
            renpy.show_screen("phone_alert", sender=sender, body=body, kind=kind)
            renpy.pause(delay)
            renpy.hide_screen("phone_alert")

    def unlock_ending(number):
        if number == 1:
            store.persistent.ending_truth = True
        elif number == 2:
            store.persistent.ending_alone = True
        elif number == 3:
            store.persistent.ending_call = True
        elif number == 4:
            store.persistent.ending_newgame = True
            store.persistent.secret_seen = True
        renpy.save_persistent()

    def all_endings_seen():
        return (store.persistent.ending_truth and store.persistent.ending_alone
                and store.persistent.ending_call)

    def sanity_state():
        if store.sanity >= 65:
            return "steady"
        if store.sanity >= 40:
            return "shaken"
        if store.sanity >= 20:
            return "fraying"
        return "breaking"

    def hotspot(label, x, y, w, h, name):
        return {"label": label, "x": x, "y": y, "w": w, "h": h, "name": name}
