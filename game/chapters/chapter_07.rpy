label chapter_07:
    $ current_chapter = 7
    call screen chapter_card("VII", "Don't Look Behind You")
    scene bg bedroom
    with slowfade
    play music audio.ch7 fadein 2.0
    play ambient audio.rain fadein 2.0
    play pulse audio.heartbeat fadein 2.0 volume 0.6

    "At 2:57 AM, the apartment is completely still."
    "The boxes are back. The photographs are face-down. The wardrobe is whole."
    "It is the apartment you moved into, before you knew what it was."
    "You are sitting on the floor with the music box in front of you. You do not remember putting it there."

    if saved_maya:
        show maya scared at char_right_in
        with dissolve
        m "I'm here."
        m "I'm not going anywhere."
        e "You should."
        m "I know."
        m "I'm still here."
        $ gain_trust(1)
    else:
        "Maya is not here."
        "You do not know if she is alive. You do not know if the thing in the hidden room left enough of her to be alive."
        "The apartment feels very large."

    "At 2:58 AM, the rain stops."
    "At 2:59 AM, the wardrobe door opens."
    "At 3:00 AM, the phone rings."

    play sound audio.phone_ring
    "The screen does not show a number. It shows a name."
    "IRIS."

    "You do not answer it. You do not need to."
    "The voice comes through the speaker anyway."

    scene cg confrontation
    with slowfade
    play music audio.entity fadein 2.0
    listener "Hello, Ethan."
    listener "Thank you for coming back."
    e "I never left."
    listener "You did. Seven years ago. Your heart stopped in this room."
    listener "Your parents called it back. They offered me their lives, and I took them."
    listener "I gave you seven years. I only want what I'm owed."
    e "You want me to answer the call."
    listener "I want you to choose."
    listener "That's the part I can't do for you. The choosing."
    listener "It's the only thing that tastes like anything."

    "Behind the voice, you can hear your parents. They are saying your name, very softly, from a long way off."
    "You can hear Iris breathing."
    "You can hear Maya's heart, if she is here, beating a little too fast."
    "And behind you, the room is breathing too."

    listener "You have one call left."
    listener "Answer it, and I will let the others go."
    listener "Refuse, and I will take whoever is closest."
    listener "Or run. I do so enjoy it when they run."

    "The phone is in your hand."
    "The red receiver is warm."
    "The room waits."

    if sanity <= 0:
        "Your thoughts are not yours anymore. They are white noise with a shape."
        "You lift the receiver before you decide to."
        jump ending_call

    menu:
        "Say her name. Face what you did.":
            if remembered and clue_count() >= 6 and sanity >= 25 and not answered_seventh:
                jump ending_truth
            else:
                jump ending_failed_truth

        "Take Maya's hand and run." if saved_maya:
            jump ending_alone

        "Run." if not saved_maya:
            jump ending_failed_run

        "Answer the seventh call.":
            jump ending_call

        "Look behind you." if all_endings_seen():
            jump ending_newgame
