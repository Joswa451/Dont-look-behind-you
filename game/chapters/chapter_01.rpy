init python:
    ch1_hotspots = [
        hotspot("ch1_photo", 210, 380, 260, 250, "A photograph turned face-down"),
        hotspot("ch1_closet", 780, 310, 250, 430, "The hall closet"),
        hotspot("ch1_bathroom", 1290, 250, 260, 390, "The bathroom door"),
        hotspot("ch1_kitchen", 520, 600, 310, 210, "The old answering machine"),
    ]

label chapter_01:
    $ current_chapter = 1
    call screen chapter_card("I", "The New Apartment")
    scene bg bedroom day
    with slowfade
    play music audio.ch1 fadein 2.0
    play ambient audio.rain fadein 2.0

    "The cab leaves you on Ashgrove Street with two suitcases and a key that feels older than you do."
    "Apartment 3B. Third floor, last door, the one with the paint worn pale around the handle."
    "The agency called it a bargain. They did not call it anything else."
    "You were four years old the last time you lived here. You remember the shape of the hallway and nothing that happened inside it."

    scene bg livingroom
    with dissolve
    "The rooms smell of dust and cold radiators. Boxes crowd the floor like patient animals."
    "A couch. A television with no signal. A window that looks onto the brick wall of the next building."
    "You tell yourself this is what independence looks like."

    play sound audio.knife
    "Something in the kitchen clicks."
    "You wait. Nothing clicks again."

    "You start unpacking. Your hands know where to put things before you do."
    "The mugs go to the cabinet above the sink. The towels go in the bathroom closet. The photographs go face-down in a drawer."
    "You do not remember deciding to put them face-down."

    play sound audio.footsteps
    "Three knocks at the door. Slow. Polite."
    show maya happy at char_right_in
    with dissolve
    m "Hi. Neighbor. 3A."
    m "I brought coffee. Well. I brought one coffee. The other one is for me, but I'm willing to negotiate."
    e "You always greet new tenants with caffeine?"
    m "Only the ones who look like they slept in a bus station."
    m "I'm Maya."

    menu:
        "Let her help.":
            $ gain_trust(2)
            $ change_sanity(3)
            e "Ethan. And yes. Please."
            show maya happy
            m "Ethan. Good name. Very haunted-house."
            "She steps inside without being invited, which somehow makes the apartment warmer."
            m "I live next door. I make too much coffee and I'm aggressively friendly. You'll get used to it."
            $ maya_stayed = True

        "Keep your distance.":
            $ change_sanity(-2)
            show maya neutral
            e "Thanks. I'm fine."
            m "You're standing in a room full of boxes holding one lamp like it's a weapon."
            e "I'm fine."
            "She studies you for a moment, then sets the coffee on the floor between you."
            m "Okay. I'll be next door if the walls start talking."
            "She smiles like it's a joke. It doesn't sound like one."

        "Ask about 3B.":
            $ gain_trust(1)
            $ change_sanity(-3)
            e "What do you know about this place?"
            show maya neutral at char_right
            m "Ashgrove? Old building. Thin walls. Radiators make this noise like someone clearing their throat."
            m "Previous tenant left in a hurry. Didn't take the furniture. Didn't leave a forwarding address."
            e "Why?"
            m "If I knew that, I'd be charging rent for the story."
            "She looks at the closed bedroom door a little too long."
            m "One thing. If the phone rings at three in the morning, don't answer it."
            e "That's a strange thing to say."
            m "It's a strange building."

    "The coffee is bitter and too hot. You drink it anyway."
    if maya_stayed:
        m "I'll leave you to the boxes. Shout if you need a human being."
        "She pauses at the door."
        m "Ethan. The phone thing. I wasn't joking."
    else:
        "Maya leaves. The apartment gets larger by exactly one person."

    hide maya
    with dissolve

    "By late afternoon, the light has gone the color of weak tea."
    "You should finish unpacking. Instead you walk through the rooms, touching the walls."

    scene bg livingroom
    with fade
    call ch1_explore

    if not has_clue("old_photo"):
        "Before the light disappears, you find a photograph under the window."
        "You do not remember putting it there."
        $ add_clue("old_photo")
        $ change_sanity(-4)
        "You turn it over before you can stop yourself."

    "The apartment is quiet in the way a held breath is quiet."
    "You make the bed. You check the lock twice. You put your phone on the nightstand and tell yourself you will sleep."

    scene bg bedroom
    with slowfade
    stop ambient fadeout 2.0
    play ambient audio.rain fadein 2.0
    stop music fadeout 4.0
    play pulse audio.heartbeat fadein 2.0 volume 0.5

    "At 2:58 AM, you are awake."
    "At 2:59 AM, the rain stops."
    "At 3:00 AM, your phone lights up."

    $ push_message("UNKNOWN", "You're home.", alert=True, delay=2.4)
    $ push_message("UNKNOWN", "I can see your light.", alert=True, delay=2.0)

    "The number is not a number. The screen shows seven zeroes and nothing else."
    "A photograph arrives."

    $ push_message("UNKNOWN", "This was taken four minutes ago.", stamp="3:04 AM", alert=True, delay=2.4, kind="photo")

    "You do not want to open it. You open it anyway."

    show screen phone_app(tab="photos")
    $ renpy.pause()
    hide screen phone_app

    "The photograph is of you."
    "You are asleep in this bed. Your mouth is open. One hand hangs off the mattress."
    "The camera is somewhere above the pillow."
    "There is no one in the room."

    $ change_sanity(-10)

    menu:
        "Look at the hallway through the peephole.":
            $ change_sanity(-4)
            "You cross the room without turning on a light."
            "The peephole gives you a small, warped circle of hallway."
            "The hallway is empty."
            "Then the circle goes dark. Someone is standing on the other side."
            "You do not hear them breathing. You hear yourself breathing, too loud, too fast."
            "The darkness steps away."
            "When you look again, the hallway is empty."

        "Call the number back.":
            $ change_sanity(-7)
            "You press call. The line connects before the first ring finishes."
            stranger "..."
            e "Who is this?"
            stranger "You promised you would come back."
            e "I don't know you."
            stranger "You will."
            stranger "You have seven days."
            $ add_call("UNKNOWN", answered=True)
            "The call ends. The screen goes black."
            "In the dark, your reflection in the window is still holding the phone to its ear."

        "Turn the phone off and close your eyes.":
            $ change_sanity(-5)
            "You hold the power button until the screen dies."
            "You lie down. You count your breaths."
            "Somewhere in the apartment, a phone rings."
            "It is not your phone. Yours is dead in your hand."
            "It rings seven times, then stops."
            $ add_call("UNKNOWN", answered=False)

    if trust_maya >= 2:
        menu:
            "Text Maya.":
                $ gain_trust(1)
                $ change_sanity(4)
                "You type: Something is wrong. The phone. My room."
                "Three dots appear. Then stay."
                m "Don't open the door."
                m "I'm serious, Ethan. Don't open it."
                "You look at the door. The handle is turning, slowly, one degree at a time."
                "Then it stops."
                "You do not sleep."

            "Don't involve her.":
                $ change_sanity(-3)
                "You put the phone face-down on the nightstand."
                "You do not sleep."

    else:
        $ change_sanity(-3)
        "You sit against the headboard until the numbers on your phone turn to 4:00."
        "You do not sleep."

    "At 3:07 AM, a message arrives from the number with seven zeroes."
    $ push_message("UNKNOWN", "Day one.", stamp="3:07 AM", alert=False)
    "You read it six times."
    "Then, very softly, from inside the wall behind your bed, someone knocks back."

    play sound audio.door_slam
    with vpunch
    scene black
    with slowfade
    stop pulse fadeout 2.0
    stop ambient fadeout 2.0
    stop music fadeout 2.0

    $ ch1_finished = True
    return

label ch1_explore:
    $ ch1_leave = False
    while not ch1_leave:
        call screen investigate(hotspots=ch1_hotspots, prompt="The apartment is full of things you almost remember.")
        if _return == "leave":
            $ ch1_leave = True
        else:
            $ ch1_spot = ch1_hotspots[_return]
            call expression ch1_spot["label"]
    return

label ch1_photo:
    scene bg livingroom
    with dissolve
    if has_clue("old_photo"):
        "The photograph is still in your pocket. You can feel the corner of it against your leg."
        return
    play sound audio.paper
    "The photograph is face-down on the windowsill. The paper is warm."
    "You turn it over."
    "Your parents are standing in front of this building. Your father is laughing at something outside the frame."
    "Your mother has her hand on your shoulder. You are six, maybe seven, missing a front tooth."
    "A girl stands beside you. Her face has been scratched away with something sharp."
    "On the back, in your mother's handwriting: Ethan, Iris, 3B. Don't forget."
    $ add_clue("old_photo")
    $ change_sanity(-5)
    "You do not remember a girl."
    "You remember the shape of her hand in yours."
    return

label ch1_closet:
    scene bg hallway
    with dissolve
    "The hall closet is narrow and smells of cedar and old rain."
    "You find a coat that is not yours. A box of Christmas ornaments. A child's shoe."
    "Then you see the marks on the inside of the door."
    play sound audio.knife
    "Scratches. Hundreds of them. Low down, at the height of a small hand."
    "Someone has carved three words into the wood, over and over."
    "{i}I'M SORRY. I'M SORRY. I'M SORRY.{/i}"
    scene bg livingroom
    with dissolve
    $ add_clue("scratches")
    $ change_sanity(-7)
    play sound audio.whisper
    "Behind you, something exhales."
    "You turn around. The living room is empty."
    return

label ch1_bathroom:
    scene bg bathroom
    with dissolve
    "The bathroom mirror is fogged at the edges even though the shower has not run in days."
    "You wipe a stripe through the condensation."
    "Your reflection wipes a stripe from the other side."
    "You stop moving."
    "It does not."
    play sound audio.drip
    "A handprint blooms on the inside of the glass. Small. Fingers spread."
    scene bg livingroom
    with dissolve
    $ add_clue("handprint")
    $ change_sanity(-6)
    "You close the bathroom door and do not look back at it."
    return

label ch1_kitchen:
    scene bg kitchen
    with dissolve
    "The old answering machine sits under the wall phone, unplugged."
    "You plug it in. The tape inside begins to turn."
    play sound audio.tape
    mom "Ethan. If you're hearing this, you're already home."
    mom "Don't answer the phone at three. Don't look at the photographs. And don't go into the closet."
    dad "We're sorry. We did what we could."
    mom "We love you. Remember that part."
    "The tape clicks. The message begins again."
    mom "Ethan. If you're hearing this, you're already home."
    scene bg livingroom
    with dissolve
    $ add_clue("answering_machine")
    $ change_sanity(-5)
    "You unplug the machine. The tape keeps turning for another full minute."
    return
