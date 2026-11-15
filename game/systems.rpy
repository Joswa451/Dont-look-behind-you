default inventory = set(["phone", "apartment_key"])
default item_uses = set()
default evidence_reviewed = set()
default phone_voicemails = []
default maya_suspicion = 0
default iris_bond = 0
default entity_attention = 0
default flashlight_on = False
default hammer_survival_used = False
default survived_entity = False
default deduction_unlocked = False
default phone_choice = None
default last_voice_file = None
default last_voice_role = None
default forest_memory_seen = set()
default bedroom_seen = set()
default school_seen = set()
default ch1_bedroom_visits = 0
default ch2_school_visits = 0
default ch6_forest_visits = 0
default ch6_survival_failures = 0
default ch1_room = "livingroom"
default ch6_hide_round = 0
default ch6_hide_result = None
default ch6_hide_rounds = [
    {"cue": "It stops at the top of the stairs and listens for breathing.", "correct": "stairs"},
    {"cue": "Its fingers drag along the laundry machines, one by one.", "correct": "boiler"},
    {"cue": "The boiler ticks. It turns toward the sound.", "correct": "laundry"},
]

init 1 python:

    ITEM_ORDER = [
        "phone", "apartment_key", "photograph", "flashlight", "hammer",
        "brass_key", "music_box", "iris_diary", "bargain_tape", "red_thread",
    ]

    ITEMS = {
        "phone": {
            "name": "Phone",
            "desc": "The screen shows seven zeroes whenever the unknown number writes. The battery never seems to die.",
            "use": "Open the phone to read messages, calls, voicemail, and photographs.",
        },
        "apartment_key": {
            "name": "Apartment Key",
            "desc": "A cold key for 3B. The metal is worn pale around the teeth, as if it has been turned many times.",
            "use": "It opens the apartment and the wardrobe on the fifth night.",
        },
        "photograph": {
            "name": "Scratched Photograph",
            "desc": "Your parents, a younger you, and a girl whose face has been scratched away. On the back: Ethan, Iris, 3B. Don't forget.",
            "use": "Study the photograph and compare it with the evidence journal.",
        },
        "flashlight": {
            "name": "Maya's Flashlight",
            "desc": "A heavy rubber flashlight with a cracked lens. It still works if you tap it twice.",
            "use": "Turn the beam on or off. Some places in the basement are too dark to search.",
        },
        "hammer": {
            "name": "Maya's Hammer",
            "desc": "The handle is wrapped in faded red tape. It is heavier than it looks.",
            "use": "A hammer is not a weapon. It is a promise that you will make noise.",
        },
        "brass_key": {
            "name": "Brass Service Key",
            "desc": "A small brass key on red thread. The paper tag reads 3B - SERVICE.",
            "use": "It opens the service corridor behind the wardrobe.",
        },
        "music_box": {
            "name": "Iris's Music Box",
            "desc": "Dark wood and brass, engraved I.V. The melody is three notes, then three more. It is warm.",
            "use": "Wind the music box. The melody steadies you, but the Listener hears it too.",
        },
        "iris_diary": {
            "name": "Iris's Diary",
            "desc": "A small red diary filled with drawings and careful looping letters. The last page is about you.",
            "use": "Read Iris's last entries again.",
        },
        "bargain_tape": {
            "name": "Bargain Tape",
            "desc": "A cassette with your name on the label. Your parents' voices are on it. So is the third voice.",
            "use": "Listen to the tape again. Some truths change every time you hear them.",
        },
        "red_thread": {
            "name": "Red Thread",
            "desc": "A length of red thread tied around a black branch. It pulls toward the apartment.",
            "use": "Hold the thread and follow the pull.",
        },
    }

    CLUE_NAMES.update({
        "wall_knock": "Knocking from inside the bedroom wall",
        "window_reflection": "Your reflection outside the bedroom window",
        "wardrobe_lock": "The wardrobe has a service lock",
        "agency_receipt": "A receipt from the agency, dated seven years ago",
        "st_agnes_photo": "A photograph of the St. Agnes children",
        "iris_missing_poster": "A missing-child poster for Iris Vale",
        "locker_names": "Seven names scratched inside a school locker",
        "piano_keys": "A child's fingerprints on the basement piano",
        "forest_carving": "An eye carved into a tree behind St. Agnes",
        "forest_thread": "Red thread tied around a forest branch",
        "forest_footprints": "Small bare footprints in the mud",
        "forest_hollow": "A hollow under the roots, just large enough for a child",
        "survived_stalker": "You hid from the Listener and survived",
    })

    EVIDENCE_META = {
        "old_photo": {
            "chapter": 1, "source": "The living room windowsill",
            "note": "Your parents stand outside Ashgrove with you and a girl whose face has been scratched away. The date and building number match 3B. The girl's hand is still visible on your shoulder.",
        },
        "scratches": {
            "chapter": 1, "source": "Inside the hall closet",
            "note": "Hundreds of child-height scratches repeat I'M SORRY into the wood. Someone was kept close to this door and tried to get out.",
        },
        "handprint": {
            "chapter": 1, "source": "The bathroom mirror",
            "note": "A small handprint appeared on the inside of the glass. The fingers are child-sized and spread wide, as if pressed there during a scream.",
        },
        "answering_machine": {
            "chapter": 1, "source": "The old kitchen answering machine",
            "note": "Your mother warns you not to answer the phone at three, not to look at the photographs, and not to enter the closet. Your father says they did what they could.",
        },
        "wall_knock": {
            "chapter": 1, "source": "The bedroom wall",
            "note": "Three knocks answer from inside the wall behind the bed. The plaster is warm. The sound is patient, not random.",
        },
        "window_reflection": {
            "chapter": 1, "source": "The bedroom window",
            "note": "Your reflection stands in the brick wall outside the window. When you step back, it does not.",
        },
        "wardrobe_lock": {
            "chapter": 1, "source": "The bedroom wardrobe",
            "note": "The wardrobe has a second lock hidden behind the coat rail. Its keyhole is brass and much newer than the wardrobe.",
        },
        "agency_receipt": {
            "chapter": 1, "source": "The bedroom nightstand",
            "note": "A rent receipt made out to E. Mercer, dated seven years ago. The agency stamp is identical to the one on your current lease.",
        },
        "fire_record": {
            "chapter": 2, "source": "The college archive",
            "note": "The St. Agnes Home for Children burned in 2009. One girl, Iris Vale, age twelve, was never found. The building on Ashgrove Street was never demolished.",
        },
        "blueprint": {
            "chapter": 2, "source": "The college archive",
            "note": "A service corridor was sealed behind 3B in 1998. It has no windows and no proper door. Someone marked the room with a red question mark.",
        },
        "case_file": {
            "chapter": 2, "source": "The grey archive box",
            "note": "A death certificate lists Ethan Mercer, age thirteen, dead seven years ago. The ink is fresh. Your heart is still beating.",
        },
        "mom_email": {
            "chapter": 2, "source": "The library terminal",
            "note": "Your mother apologizes for an arrangement that lasted too long. She warns you not to let him see you look behind you. The address no longer exists.",
        },
        "maya_notes": {
            "chapter": 2, "source": "Maya's folder",
            "note": "Maya has been researching Ashgrove for six months. Seven names in the building records have no move-out dates. You are the eighth.",
        },
        "girl_in_hall": {
            "chapter": 2, "source": "The peephole",
            "note": "A girl stood close enough to fill the brass circle. She looked through the wall rather than at the peephole. The chain held.",
        },
        "iris_name": {
            "chapter": 2, "source": "The girl in the hallway",
            "note": "Her name is Iris Vale. She remembers oranges, the wall between your rooms, and a promise you do not remember making.",
        },
        "music_box": {
            "chapter": 3, "source": "The basement",
            "note": "A wooden music box engraved I.V. There is a lock of dark hair under the velvet. The dancer turns to face you when the melody stops.",
        },
        "drawings": {
            "chapter": 3, "source": "The basement pipes",
            "note": "Children's drawings show a faceless figure, a windowless room, and a telephone cord going into the floor. One drawing labels a boy ETHAN and a door IN HERE.",
        },
        "name_list": {
            "chapter": 3, "source": "The basement wall",
            "note": "Seven names are carved beside the boiler. Six have dates. The seventh is ETHAN MERCER, with no date. Below it: HE CAME BACK WRONG.",
        },
        "boiler_handprint": {
            "chapter": 3, "source": "The old boiler",
            "note": "A small handprint is pressed into the rust. When you place your hand beside it, something inside the boiler breathes in time with you.",
        },
        "mom_call": {
            "chapter": 3, "source": "The call from MOM",
            "note": "Your mother says the music box is the lock and your father's blood is the key. She tells you to say the girl's name where he can hear it.",
        },
        "piano_keys": {
            "chapter": 3, "source": "The basement piano",
            "note": "The piano has no keys, but child-sized fingerprints cover the wood above where the keyboard should be. Someone practiced on a silent instrument.",
        },
        "st_agnes_photo": {
            "chapter": 2, "source": "The school trophy case",
            "note": "A faded photograph shows the children of St. Agnes in two rows. Iris Vale stands at the edge, holding a music box. Your face has been scratched out beside her.",
        },
        "iris_missing_poster": {
            "chapter": 2, "source": "The school bulletin board",
            "note": "A missing-child poster for Iris Vale is hidden behind newer notices. The date is the day after the fire. Someone added one line in red: SHE WAS NEVER MISSING.",
        },
        "locker_names": {
            "chapter": 2, "source": "A dented school locker",
            "note": "Seven names are scratched inside the locker door. The last one is yours. The scratches are fresh.",
        },
        "mirror": {
            "chapter": 4, "source": "The bathroom mirror",
            "note": "Your reflection moved half a second late. It wrote LET ME OUT in the condensation, again and again, until the glass was full.",
        },
        "entity_saw_you": {
            "chapter": 4, "source": "The bedroom wardrobe",
            "note": "Something inside the wardrobe wore every face you have ever seen in a mirror. It spoke your name in your own voice.",
        },
        "key": {
            "chapter": 4, "source": "The bathroom sink",
            "note": "A small brass key appeared beside the sink. The tag reads 3B - SERVICE. It is warm.",
        },
        "bargain_tape": {
            "chapter": 5, "source": "The hidden room",
            "note": "Your parents offered themselves in exchange for seven more years of your life. The Listener accepted. When you remember, you belong to him.",
        },
        "iris_diary": {
            "chapter": 5, "source": "The hidden room",
            "note": "Iris wrote that the listening man would bring her a friend if she stayed quiet. She heard you through the wall. She is not angry. She is tired of the dark.",
        },
        "photo_iris": {
            "chapter": 5, "source": "The hidden room wall",
            "note": "You and Iris at a birthday party, both laughing. The back reads ETHAN + IRIS. BEST FRIENDS. DO NOT FORGET. You remember the paper crown.",
        },
        "altar": {
            "chapter": 5, "source": "The hidden room",
            "note": "Seven old telephones sit on a stained cloth. Six are black. The red phone has your name on it. The candle gives off no heat.",
        },
        "name_list_hidden": {
            "chapter": 5, "source": "The hidden room plaster",
            "note": "Seven names are carved deeper than the ones in the basement. Yours is last. Below it: HE WAS THE ONLY ONE WHO HEARD ME.",
        },
        "forest_carving": {
            "chapter": 6, "source": "The dream forest",
            "note": "An eye is carved into a tree behind St. Agnes. The cuts are old and child-sized. Inside the pupil, someone has scratched your initials.",
        },
        "forest_thread": {
            "chapter": 6, "source": "The dream forest",
            "note": "Red thread is tied around a black branch. It runs between the trees and disappears toward Ashgrove Street.",
        },
        "forest_footprints": {
            "chapter": 6, "source": "The dream forest",
            "note": "Small bare footprints cross the mud, circle the tree, and stop at the hollow. They never lead away.",
        },
        "forest_hollow": {
            "chapter": 6, "source": "The dream forest",
            "note": "A hollow beneath the roots is just large enough for a child. The wood inside is warm and smells faintly of oranges.",
        },
        "survived_stalker": {
            "chapter": 6, "source": "The basement stairwell",
            "note": "You kept still while the Listener searched the dark. He passed close enough to breathe against your neck. You did not answer.",
        },
    }

    EVIDENCE_ORDER = list(CLUE_NAMES.keys())

    def add_item(key, silent=False):
        if key not in ITEMS:
            raise Exception("Unknown item: %s" % key)
        if key not in store.inventory:
            store.inventory.add(key)
            if not silent:
                renpy.notify("Added to bag: " + ITEMS[key]["name"])
            return True
        return False

    def remove_item(key, silent=False):
        if key in store.inventory:
            store.inventory.remove(key)
            if not silent:
                renpy.notify("Removed from bag: " + ITEMS[key]["name"])
            return True
        return False

    def has_item(key):
        return key in store.inventory

    def change_attention(amount):
        store.entity_attention = clamp(store.entity_attention + amount, 0, 12)
        return store.entity_attention

    def change_iris_bond(amount):
        store.iris_bond = clamp(store.iris_bond + amount, 0, 10)
        return store.iris_bond

    def change_suspicion(amount):
        store.maya_suspicion = clamp(store.maya_suspicion + amount, 0, 10)
        return store.maya_suspicion

    def maya_relationship():
        if store.trust_maya >= 8:
            return "Devoted"
        if store.trust_maya >= 5:
            return "Trusting"
        if store.trust_maya >= 3:
            return "Careful"
        return "Distant"

    def iris_relationship():
        if store.iris_bond >= 7:
            return "Bonded"
        if store.iris_bond >= 4:
            return "Remembered"
        if store.iris_bond >= 2:
            return "Seen"
        return "Unknown"

    def listener_relationship():
        if store.entity_attention >= 8:
            return "Hunting"
        if store.entity_attention >= 5:
            return "Watching"
        if store.entity_attention >= 2:
            return "Listening"
        return "Waiting"

    def review_evidence(key):
        if key not in store.clues:
            return
        first = key not in store.evidence_reviewed
        store.evidence_reviewed.add(key)
        if first and len(store.evidence_reviewed) >= 8 and not store.deduction_unlocked:
            store.deduction_unlocked = True
            renpy.notify("Deduction unlocked: The seventh name was always yours.")

    def use_item(key):
        if key not in store.inventory:
            return
        first = key not in store.item_uses
        store.item_uses.add(key)

        if key == "phone":
            renpy.notify("Open the phone from the quick menu.")

        elif key == "apartment_key":
            renpy.notify("The key turns easily. It knows the lock.")

        elif key == "photograph":
            if not has_clue("old_photo"):
                add_clue("old_photo", silent=True)
            review_evidence("old_photo")
            if first:
                change_sanity(-1)
                renpy.notify("The scratched-out face seems to turn toward yours.")

        elif key == "flashlight":
            store.flashlight_on = not store.flashlight_on
            renpy.sound.play(audio.click)
            if store.flashlight_on:
                renpy.notify("Flashlight on. Dark corners are easier to search.")
            else:
                renpy.notify("Flashlight off. The dark comes back quickly.")

        elif key == "hammer":
            renpy.notify("You test the weight. It could buy you one safe moment.")

        elif key == "brass_key":
            if not has_clue("key"):
                add_clue("key", silent=True)
            renpy.notify("The brass key is warm. The wardrobe is waiting on the fifth night.")

        elif key == "music_box":
            renpy.sound.play(audio.music_box)
            change_sanity(3)
            change_attention(1)
            if not has_clue("music_box"):
                add_clue("music_box", silent=True)
            if first:
                renpy.notify("The melody steadies your hands. Something else leans closer.")
            else:
                renpy.notify("The melody is louder this time.")

        elif key == "iris_diary":
            if not has_clue("iris_diary"):
                add_clue("iris_diary", silent=True)
            review_evidence("iris_diary")
            change_iris_bond(1)
            if first:
                renpy.notify("Iris's handwriting is careful. It is easier to read than your own thoughts.")

        elif key == "bargain_tape":
            if not has_clue("bargain_tape"):
                add_clue("bargain_tape", silent=True)
            review_evidence("bargain_tape")
            renpy.sound.play(audio.tape)
            if first:
                change_sanity(-3)
                change_attention(1)
                renpy.notify("Your father's voice is thinner than you remember.")

        elif key == "red_thread":
            change_attention(1)
            if store.current_chapter >= 7:
                change_sanity(3)
                renpy.notify("The thread pulls toward the wardrobe. You can feel Iris on the other end.")
            else:
                change_sanity(-2)
                renpy.notify("The thread pulls toward 3B. You do not want to follow it yet.")

    def add_voicemail(sender, transcript, audio_file, stamp="3:00 AM", duration="0:12"):
        store.phone_voicemails.append({
            "from": sender,
            "text": transcript,
            "audio": audio_file,
            "time": stamp,
            "duration": duration,
        })
        store.phone_unread += 1
        return store.phone_voicemails[-1]

    def play_voicemail(index):
        if index < 0 or index >= len(store.phone_voicemails):
            return
        renpy.sound.play(store.phone_voicemails[index]["audio"], channel="voicemail")

    def stop_voicemail():
        renpy.sound.stop(channel="voicemail")

    def horror_tick():
        if store.sanity >= 58 or store.current_chapter <= 0:
            return
        if (renpy.get_screen("main_menu") or renpy.get_screen("preferences")
                or renpy.get_screen("phone_app") or renpy.get_screen("evidence_journal")
                or renpy.get_screen("inventory_screen") or renpy.get_screen("confirm")):
            return
        if renpy.random.random() < 0.42:
            renpy.sound.play(audio.whisper)
            renpy.show_screen("horror_flash")
            renpy.restart_interaction()

    def place_relation_hint():
        if store.maya_suspicion >= 5:
            return "Maya has stopped asking easy questions."
        if store.entity_attention >= 5:
            return "The room is listening more closely than it was."
        return "The apartment is quiet. That is not the same as safe."
