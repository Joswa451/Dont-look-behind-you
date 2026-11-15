init python:
    ch6_forest_hotspots = [
        hotspot("ch6_forest_carving", 220, 300, 340, 330, "An eye carved into a tree"),
        hotspot("ch6_forest_thread", 760, 250, 310, 310, "Red thread around a black branch"),
        hotspot("ch6_forest_footprints", 1150, 520, 330, 260, "Bare footprints in the mud"),
        hotspot("ch6_forest_hollow", 480, 640, 340, 230, "A hollow under the roots"),
    ]

label chapter_06:
    $ current_chapter = 6
    call screen chapter_card("VI", "Seven Days Later")
    scene bg bedroom day
    with slowfade
    play music audio.ch6 fadein 2.0
    play ambient audio.wind fadein 2.0

    "You lose a day."
    "There is no transition. No dream. You close your eyes on day five and open them on day seven."
    "The clock says 9:00 AM. The date on your phone says you have been asleep for thirty-one hours."
    "There are forty-one messages."

    $ add_message("UNKNOWN", "Six days down. One to go.", "3:00 AM")
    $ add_message("UNKNOWN", "You missed a day. I kept it for you.", "3:01 AM")
    $ add_message("MAYA", "Ethan. Call me.", "7:42 AM")
    $ add_message("MAYA", "I'm at my place. The door is open.", "7:43 AM")
    $ add_message("MAYA", "Please don't come alone.", "7:43 AM")
    $ add_voicemail("MAYA", "Ethan. If you get this, don't come alone. And don't trust the hallway. I'm sorry. I should have told you what I found.", audio.voicemail_maya, stamp="7:44 AM", duration="0:19")

    "The last message was sent from Maya's phone."
    "The text is typed in your handwriting."

    $ change_sanity(-8)

    "Before you can stand, the bedroom folds inward."
    call ch6_forest_dream
    scene bg bedroom day
    with slowfade

    "You get up. The apartment is wrong."
    "The furniture is arranged the way it was when you moved in. The boxes are packed again."
    "The photograph is face-down on the windowsill. The key is gone from the nightstand."
    "On the kitchen table, someone has set out two cups of coffee."
    "One is cold. One is still steaming."

    menu:
        "Go to Maya's apartment.":
            $ change_sanity(-3)
            "You take the steaming cup with you. You do not know why."
            "The hallway is longer than it was yesterday."
            "You count doors. 3B. 3A. Then 3B again."
            "You turn around. 3A is behind you, where it should be."

        "Search your apartment first.":
            $ change_sanity(-5)
            $ key_hidden_room = True
            "You check the bedroom. The wardrobe is gone."
            "In its place is a smooth stretch of wall with a small brass key taped to it."
            "You take the key. The wall is warm."
            "Then you hear Maya's voice through it, saying your name."

        "Call Maya back.":
            $ change_sanity(-4)
            "You press call."
            "It rings once."
            m "Ethan."
            e "Where are you?"
            m "I'm where you left me."
            e "I didn't leave you anywhere."
            m "You did. You just don't remember yet."
            "The call drops."
            "A message arrives."
            $ push_message("MAYA", "3A. The door is open. Hurry.", stamp="9:08 AM", alert=False)

    $ ch6_attempts = 0
    $ ch6_path = False
    call ch6_hallway

    scene bg livingroom
    with slowfade
    stop ambient fadeout 2.0
    play ambient audio.drip fadein 2.0
    "Maya's apartment is dark."
    "The plants are dead. The red string has been pulled off the wall and piled in the middle of the floor."
    "The pile is shaped like a person."
    "The phone on her kitchen counter is off the hook. A voice is coming out of it, very small."

    m "Ethan."
    m "Ethan, can you hear me?"
    e "Maya?"
    m "Don't trust the hallway. Don't trust the door. Don't trust me."
    e "What?"
    m "I'm in the room behind the wall. The one with the circle."
    m "He's using my voice. He's been using it since you got here."
    "The line clicks."

    play sound audio.phone_ring
    "Her phone rings again."
    "The screen says MAYA."
    "You answer."

    stranger "Ethan."
    "It is Maya's voice, but the words are too slow, as if they are being read from a page."
    stranger "Come to the basement. I'm waiting."
    stranger "Come alone."

    menu:
        "Ask about the hammer.":
            $ change_sanity(-4)
            e "What did you bring to my apartment on day four?"
            stranger "What?"
            e "The hammer, Maya. What did you bring?"
            "The voice on the other end is silent for a long time."
            stranger "I brought you coffee."
            "You hang up."
            "The real Maya would have said the hammer."
            "You hope she would have said the hammer."

        "Stay on the line.":
            $ change_sanity(-9)
            "You keep the phone to your ear."
            "The fake Maya breathes. Then stops breathing."
            "Then starts again, closer."
            stranger "You're standing in my kitchen."
            stranger "You're touching my table."
            stranger "You're so close I can almost wear you."
            "You drop the phone. It lands face-up. The screen shows your own face."

        "Hang up and find her.":
            $ change_sanity(-3)
            "You end the call."
            "The apartment settles around you. Somewhere below the floor, a door opens."

    "The wall behind the couch is breathing."

    scene cg parents
    with slowfade
    play music audio.entity fadein 2.0
    "Two figures are sitting on the couch."
    "Your mother. Your father."
    "They are burned. Their faces are the way they looked in the last photograph, before the fire took the details."
    "They are holding hands."
    mom "Ethan."
    dad "You've grown so much."
    e "You're not real."
    mom "We're as real as you are."
    dad "Which is to say: not very."
    mom "We did a terrible thing. We made a hole and poured you into it."
    dad "We thought love was the same as keeping."
    mom "It isn't."
    dad "The box is the lock. Your blood is the key."
    mom "The girl is the door."
    dad "When he calls tonight, don't answer with words."
    mom "Answer with her name."
    "The figures begin to come apart, like ash in a draft."
    e "Wait—"
    mom "We love you. Remember that part."
    dad "Don't look behind you."
    "They are gone."
    scene bg livingroom
    with blackout
    $ change_sanity(-10)
    $ add_clue("bargain_tape", silent=True)
    "The room smells of smoke and rain."

    "The floor beneath the couch is open."
    "A staircase goes down into the dark. It was not there a minute ago."

    scene bg underground
    with slowfade
    "You go down."
    "The stairs are wet. The walls are closer than they were before."
    "Halfway down, you hear someone counting."
    "One. Two. Three. Four. Five. Six."
    "Then silence."

    play sound audio.heartbeat
    "Your heart answers seven."
    call ch6_survival

    scene bg hiddenroom
    with slowfade
    play music audio.ch6 fadein 2.0
    "The hidden room is lit by the red phone."
    "Maya is lying inside the circle. Her eyes are open. She is not blinking."
    "Iris stands over her, one hand held out like she is keeping something back."

    show girl scared at char_left_in
    with dissolve
    i "You came."
    e "Is she alive?"
    i "Yes. He's using her to listen."
    i "If you take her out of the circle, he'll have to let go of her."
    i "If you answer the phone, he'll have you instead."
    i "If you break the circle, he'll be angry."
    e "What happens when he's angry?"
    i "I don't know. I've never seen anyone survive it."

    "The red phone rings."
    "Maya's lips move, but the voice comes from the receiver."

    m "Ethan. Pick up."
    m "I'm not afraid. Are you?"

    menu:
        "Pull Maya out of the circle.":
            $ saved_maya = True
            $ gain_trust(2)
            $ change_sanity(-9)
            $ change_iris_bond(2)
            $ change_attention(1)
            play sound audio.door_slam
            with vpunch
            "You step into the circle and take Maya's wrists."
            "She is cold. Too cold. But she is breathing."
            "You drag her across the red paint."
            "The phone screams."
            "The sound goes through your teeth and out the back of your skull."
            "When it stops, Maya is coughing in your arms."
            m "Ethan?"
            m "You look terrible."
            e "You're welcome."
            show girl surprised
            i "You chose her."
            i "He didn't think you would."
            "The red phone stops ringing."

        "Answer the red phone.":
            $ answered_seventh = True
            $ saved_maya = False
            $ change_sanity(-15)
            $ change_iris_bond(-1)
            $ change_attention(3)
            play sound audio.heartbeat
            "You pick up the red phone."
            listener "There you are."
            e "Let her go."
            listener "Say please."
            e "Let her go."
            listener "You can have her back when you come to me."
            listener "Tonight. Three o'clock. The seventh call."
            "The line goes dead."
            "Maya's eyes close."
            "Iris kneels beside her and puts a hand on her chest."
            i "She's still here."
            i "But she's very far away."
            "You cannot tell if that is mercy or a threat."

        "Break the circle.":
            $ saved_maya = True
            $ gain_trust(1)
            $ change_sanity(-12)
            $ change_iris_bond(1)
            $ change_attention(2)
            play sound audio.knife
            with vpunch
            "You drag your heel through the red paint."
            "The circle breaks with a sound like a bone snapping."
            "Maya gasps. Iris flickers."
            "The red phone rings and rings and rings."
            play sound audio.glitch
            "The room tilts. You fall to your knees."
            "When you look up, Maya is sitting beside you, holding her head."
            m "What happened?"
            e "I broke something."
            m "Did it help?"
            "The phone stops ringing."
            "Somewhere above you, a door opens."
            i "He's coming."
            i "You have until three."

    show girl sad at char_left
    i "The seventh call is not a phone call."
    i "It's a choice. He'll make it look like a phone. He'll make it look like me."
    i "Don't answer with words. Answer with my name."
    "Iris begins to fade."
    e "Wait. What's your name?"
    i "You know it."
    e "Iris."
    show girl happy
    i "Again."
    e "Iris Vale."
    "She smiles. For a second, she is just a girl."
    i "I'll see you at three."

    hide girl
    with slowfade
    scene bg bedroom
    with blackout
    stop ambient fadeout 2.0
    stop music fadeout 3.0

    if saved_maya:
        show maya scared at char_right_in
        with dissolve
        m "What time is it?"
        e "Almost midnight."
        m "Good. We have three hours."
        m "I'm not leaving you alone with him."
        "She takes the hammer out of her bag. You do not ask how she got it back."
        $ gain_trust(1)
    else:
        "You leave Maya in the hidden room because you cannot carry her and climb at the same time."
        "You tell yourself you will come back."
        "You do not know if it is true."

    if answered_seventh:
        $ push_message("UNKNOWN", "You already said yes.", stamp="11:58 PM", alert=False)
        "Your phone shows seven zeroes."
        "The seventh call is already waiting."
    else:
        $ push_message("UNKNOWN", "One night left.", stamp="11:58 PM", alert=False)
        $ push_message("UNKNOWN", "Come alone. Or don't. I like surprises.", stamp="11:59 PM", alert=False)

    if not any(v["from"] == "UNKNOWN" for v in phone_voicemails):
        $ add_voicemail("UNKNOWN", "One night left. Bring the box. Bring the girl. Bring whoever you want to lose. I will be waiting where the wall is thinnest.", audio.voicemail_unknown, stamp="11:59 PM", duration="0:12")

    scene black
    with slowfade
    $ ch6_finished = True
    return

label ch6_forest_dream:
    scene bg forest
    with slowfade
    play ambient audio.wind fadein 2.0
    "You are standing behind St. Agnes. The trees are bare and very straight."
    "The burned children's home is a black shape through the branches. Its windows are lit."
    "A red thread runs between the trees, low enough to follow."
    "Somewhere ahead, a child is counting."

    call ch6_forest_explore

    if not has_clue("forest_thread"):
        "Before you wake, the red thread wraps once around your wrist and pulls tight."
        $ add_clue("forest_thread")
    $ add_item("red_thread", silent=True)
    $ change_sanity(-5)
    $ change_attention(1)
    "The thread tugs toward the apartment."
    "You follow it until the forest folds into the shape of your bedroom."
    play sound audio.heartbeat
    scene black
    with slowfade
    $ renpy.pause(0.6)
    return

label ch6_forest_explore:
    $ ch6_forest_leave = False
    while not ch6_forest_leave:
        call screen investigate(hotspots=ch6_forest_hotspots, prompt="The forest is dreaming you back toward the house.")
        if _return == "leave":
            $ ch6_forest_leave = True
        else:
            $ ch6_spot = ch6_forest_hotspots[_return]
            call expression ch6_spot["label"]
    return

label ch6_forest_carving:
    scene bg forest
    with dissolve
    if has_clue("forest_carving"):
        "The carved eye is still open. It follows you when you turn away."
        return
    "An eye is carved into the trunk of a black tree. The cuts are old and child-sized."
    "Inside the pupil, someone has scratched your initials."
    $ add_clue("forest_carving")
    $ change_sanity(-4)
    $ change_attention(1)
    return

label ch6_forest_thread:
    scene bg forest
    with dissolve
    if has_clue("forest_thread"):
        "The red thread is still tied around the branch. It is shorter than it was."
        return
    "A length of red thread is tied around a black branch."
    "It runs between the trees and disappears toward Ashgrove Street."
    "When you touch it, the thread is warm."
    $ add_clue("forest_thread")
    $ add_item("red_thread", silent=True)
    $ change_iris_bond(1)
    return

label ch6_forest_footprints:
    scene bg forest
    with dissolve
    if has_clue("forest_footprints"):
        "The footprints are still there. They still do not lead away."
        return
    "Small bare footprints cross the mud."
    "They circle the tree, stop at the hollow, and never come out again."
    $ add_clue("forest_footprints")
    $ change_sanity(-4)
    $ change_iris_bond(1)
    return

label ch6_forest_hollow:
    scene bg forest
    with dissolve
    if has_clue("forest_hollow"):
        "The hollow smells of oranges. Something inside it is breathing very slowly."
        return
    "A hollow beneath the roots is just large enough for a child."
    "The wood inside is warm. It smells faintly of oranges."
    "You do not put your hand inside. You are not sure you could pull it back out."
    $ add_clue("forest_hollow")
    $ change_sanity(-5)
    $ change_iris_bond(1)
    return

label ch6_survival:
    $ ch6_survival_failures = 0
    $ ch6_hide_round = 0
    while ch6_hide_round < 3:
        $ ch6_hide_round += 1
        $ ch6_hide_round_data = ch6_hide_rounds[ch6_hide_round - 1]
        $ ch6_hide_result = renpy.call_screen("survival_hide", cue=ch6_hide_round_data["cue"], round_number=ch6_hide_round, limit=8.0)
        if ch6_hide_result == ch6_hide_round_data["correct"]:
            $ change_sanity(2)
            "You keep still. It passes close enough to stir the dust."
        else:
            $ ch6_survival_failures += 1
            $ change_sanity(-7)
            $ change_attention(2)
            play sound audio.breathing
            "It stops beside you. You hear it deciding."
            "Then it moves on."

    if ch6_survival_failures == 0:
        $ survived_entity = True
        $ add_clue("survived_stalker")
        $ change_sanity(4)
        "You wait until the basement is completely silent. Then you breathe."
    elif ch6_survival_failures == 1:
        $ change_sanity(-4)
        "It finds the edge of your hiding place. It does not find you."
        "When it leaves, you count to one hundred before moving."
    else:
        $ change_attention(3)
        play sound audio.jumpscare
        with vpunch
        "It finds you. For one long second, it wears your face."
        "Then it is gone, and you are on the stairs with your hands over your mouth."
    return

label ch6_hallway:
    while not ch6_path:
        $ ch6_attempts += 1
        menu:
            "Knock on 3A.":
                $ ch6_path = True
                "You knock on Maya's door."
                "It opens inward before your knuckles touch the wood."

            "Take the stairs.":
                $ change_sanity(-6)
                "You go down."
                "The stairs bring you back to the third floor."
                "The hallway is exactly as it was. The coffee cup in your hand is hotter than before."
                "You have not taken a single step."

            "Press the elevator button.":
                $ change_sanity(-7)
                "The elevator arrives immediately."
                "The doors open onto a concrete corridor that smells of smoke."
                "A girl in a hospital gown stands at the far end with her back to you."
                "She does not turn around."
                "The doors close."
                "When they open again, you are back in the third-floor hallway."

            "Stand still and listen.":
                $ change_sanity(-5)
                "You stand still."
                "Somewhere behind the wallpaper, someone is counting your breaths."
                "You can hear your own name being practiced."
                "You knock on 3A to make it stop."
                $ ch6_path = True

    return
