label chapter_04:
    $ current_chapter = 4
    call screen chapter_card("IV", "Don't Open the Door")
    scene bg livingroom
    with slowfade
    play music audio.ch4 fadein 2.0
    play ambient audio.rain fadein 2.0

    "Day four begins with the sound of someone moving furniture in the apartment above you."
    "You lie still and listen. The scraping goes from one end of the ceiling to the other."
    "Then it stops directly above your head."
    "There is no apartment above 3B. The building ends at the roof."

    $ push_message("UNKNOWN", "Did you sleep?", stamp="9:02 AM", alert=False)
    $ push_message("UNKNOWN", "You look tired.", stamp="9:03 AM", alert=False)
    $ push_message("UNKNOWN", "I'm inside your room.", stamp="9:04 AM", alert=True, delay=2.4)
    $ change_sanity(-5)

    "You sit up."
    "The bedroom is empty. The closet door is closed. The window is closed."
    "Your phone vibrates in your hand."

    $ push_message("UNKNOWN", "Not yet.", stamp="9:05 AM", alert=False)
    "You do not understand why that is worse."

    "Maya knocks at noon. She is carrying a paper bag, a hammer, and a look you have not seen on her before."
    $ add_item("hammer", silent=True)
    show maya scared at char_right_in
    with dissolve
    m "I brought food. And a weapon. The food is for me. The weapon is for the door."
    e "You think a hammer will help?"
    m "It helps me."
    m "I didn't sleep either. Every time I closed my eyes, I heard your parents' voices."
    e "You heard them?"
    m "I found a tape in the trash. I thought it was music. It wasn't."
    show maya sad
    m "They kept saying your name. They kept saying 'take us instead.'"

    menu:
        "Ask her to stay.":
            $ gain_trust(2)
            $ maya_stayed = True
            $ change_sanity(5)
            e "Stay. Please."
            m "I was hoping you'd ask."
            "She puts the hammer on the kitchen counter and takes off her coat."
            m "We're going to be fine."
            "Neither of you believes it. It helps anyway."

        "Tell her to go home.":
            $ gain_trust(-2)
            $ maya_stayed = False
            $ change_sanity(-5)
            e "You should go. This isn't your problem."
            show maya angry
            m "It became my problem when I found a box of tapes with your name on them."
            m "But fine. If you want to be alone, be alone."
            "She leaves the hammer on the counter."
            "The apartment feels smaller after she goes."

        "Ask her about the tape.":
            $ gain_trust(1)
            $ add_clue("bargain_tape")
            $ change_sanity(-4)
            e "What exactly did they say?"
            m "Your mother said they knew what it would cost. Your father said they'd pay it."
            m "Then a voice that wasn't either of them said: 'Seven years. Then he remembers.'"
            e "Seven years."
            m "Today is the fourth day."
            "She does not say the rest. She does not have to."

    if maya_stayed:
        "Maya sleeps on the couch with the hammer on the floor beside her."
        "You sit in the armchair and watch the hallway door until the light changes."
    else:
        "You are alone when the light changes."
        "The apartment makes its evening noises: pipes, radiators, the soft tick of the building settling."
        "Tonight, it sounds like someone practicing your voice."

    scene bg bathroom
    with slowfade
    stop ambient fadeout 2.0
    "At 2:57 AM, you go into the bathroom to splash water on your face."
    "The bulb above the mirror buzzes. The tap runs brown for a second, then clear."
    "You look at yourself."

    scene cg mirror
    with slowfade
    play music audio.entity fadein 2.0
    play sound audio.flicker
    "Your reflection is a half second behind you."
    "You raise your hand. It raises its hand."
    "You lower it. It keeps its hand in the air."
    "Then it smiles."
    "You are not smiling."

    $ change_sanity(-10)
    $ add_clue("mirror")
    play sound audio.knife
    "The glass fogs from the inside."
    "A finger draws letters in the condensation, backward, so you can read them."
    "{i}LET ME OUT.{/i}"
    "The finger keeps moving. It writes the same three words again, smaller, underneath."
    "And again."
    "And again."
    "Until the whole mirror is full of them."

    scene bg bathroom
    with Dissolve(0.5)
    $ renpy.pause(0.4)
    play sound audio.glitch
    "You stumble back. The mirror is clear."
    "On the edge of the sink, where there was nothing a moment ago, sits a small brass key."
    "A paper tag is tied to it with red thread."
    "{i}3B — SERVICE.{/i}"
    $ key_hidden_room = True
    $ add_clue("key")
    $ add_item("brass_key", silent=True)
    $ change_sanity(-3)

    show maya scared at char_right_in
    with dissolve
    if maya_stayed:
        m "Ethan?"
        m "I heard glass."
        e "It's fine. I'm fine."
        m "You're holding a key and staring at a mirror."
        m "That's not fine."
    else:
        "From the living room, the hammer falls off the counter."
        "You are still alone."

    play sound audio.footsteps
    "Three knocks."
    "Not at the front door."
    "From inside the wardrobe in the bedroom."

    $ push_message("UNKNOWN", "I'm inside your room.", stamp="3:00 AM", alert=True, delay=2.4)
    $ change_sanity(-4)
    "The knocking becomes a slow, patient drumming. The wardrobe door jumps in its frame."

    menu:
        "Open the wardrobe.":
            $ change_sanity(-17)
            $ add_clue("entity_saw_you")
            play sound audio.door_creak
            "You cross the bedroom and take the handle."
            "The wardrobe is cold. The door opens before you pull."
            scene cg jumpscare
            with redflash
            play sound audio.jumpscare
            with vpunch
            $ renpy.pause(1.4)
            "It is not a coat."
            "It is a face made of every face you have ever seen in a mirror."
            "It has your eyes. It has Iris's small hands. It has your mother's mouth."
            "The mouth opens and says your name in your own voice."
            scene bg bedroom
            with blackout
            play sound audio.glitch
            "You are on the floor. The wardrobe is closed."
            "There is a handprint on the ceiling above your bed."
            "It is still warm."

        "Barricade the wardrobe.":
            $ change_sanity(-8)
            "You drag the armchair across the room and wedge it under the wardrobe handle."
            "The drumming stops."
            "The wardrobe breathes in. The wood bulges outward, once, like a chest."
            "Then it settles."
            "A message arrives."
            $ push_message("UNKNOWN", "Wrong door.", stamp="3:02 AM", alert=False)
            "You do not move until the sun comes up."

        "Wake Maya.":
            if maya_stayed:
                $ gain_trust(2)
                $ change_sanity(-5)
                "You shake Maya awake. She is already standing before you finish saying her name."
                m "Where?"
                e "The wardrobe."
                "She looks at it for a long time. Then she picks up the hammer."
                m "Okay."
                m "If it comes out, I hit it. If it says something clever, you hit it."
                "The wardrobe stops knocking."
                "From inside, very softly, something laughs."
                "Maya does not lower the hammer."
            else:
                $ change_sanity(-9)
                "You call Maya. It rings and rings."
                "Then she answers, breathless."
                m "Ethan? What's wrong?"
                e "The wardrobe. It's knocking."
                "There is a long pause."
                m "Ethan. I'm standing outside your door."
                "The line goes dead."
                play sound audio.footsteps
                "Three knocks. From the front door this time."
                "You do not open it."

        "Sit on the bed and do nothing.":
            $ change_sanity(-11)
            "You sit on the edge of the bed with your hands in your lap."
            "The wardrobe knocks for six minutes. Then it stops."
            "A message arrives."
            $ push_message("UNKNOWN", "I can be patient too.", stamp="3:06 AM", alert=False)
            "You do not sleep."
            "Neither does the wardrobe."

    "Your phone lights up before either of you can speak."
    $ push_message("UNKNOWN", "Ask her what she heard on the tape.", stamp="3:04 AM", alert=False)
    call screen phone_reply("An unknown number is waiting for an answer.", [("Who is this?", "demand"), ("Leave her out of this.", "protect"), ("I'm not afraid of you.", "defy")])
    $ phone_choice = _return
    if phone_choice == "demand":
        $ change_attention(1)
        $ change_sanity(-2)
        $ push_message("UNKNOWN", "Wrong question. You already know.", stamp="3:05 AM", alert=False)
        "The screen goes dark before you can type anything else."
    elif phone_choice == "protect":
        $ change_attention(-1)
        $ change_sanity(2)
        if maya_stayed:
            $ gain_trust(1)
        $ push_message("UNKNOWN", "How sweet. She cannot hear you from where she is going.", stamp="3:05 AM", alert=False)
        "The message is a promise. You do not know which of you it is for."
    else:
        $ change_attention(2)
        $ change_sanity(-3)
        $ push_message("UNKNOWN", "Good. Then look behind you.", stamp="3:05 AM", alert=False)
        play sound audio.whisper
        "Something breathes against the back of your neck."
        $ renpy.pause(0.8)

    if maya_stayed and trust_maya >= 4:
        show maya sad at char_right
        m "Ethan."
        m "The tape. Your parents. The death certificate. The key."
        m "I think you know what this is."
        e "Say it."
        m "I think you died seven years ago."
        "The words hang in the air. The apartment does not contradict her."
        menu:
            "Admit it.":
                $ gain_trust(2)
                $ change_sanity(4)
                $ told_maya_truth = True
                e "I think you're right."
                m "Okay."
                m "Okay. Then we're going to figure out what kept you here, and we're going to unkeep it."
                "She sits beside you on the bed. Her shoulder is warm."

            "Deny it.":
                $ gain_trust(-1)
                $ change_sanity(-5)
                e "I'm right here. I'm alive."
                show maya sad
                m "I know."
                m "That's what scares me."
                "She does not move away, but something behind her eyes closes."

    "At 6:00 AM, the key on the nightstand is warm."
    "The wardrobe door is open a finger's width. Inside, there is a seam of darkness that is too straight to be a shadow."
    "The hidden room from the blueprint."

    scene black
    with slowfade
    stop ambient fadeout 2.0
    stop music fadeout 3.0
    $ ch4_finished = True
    return
