init python:
    ch2_hotspots = [
        hotspot("ch2_newspaper", 250, 430, 320, 230, "A newspaper on the reading table"),
        hotspot("ch2_blueprint", 760, 350, 300, 260, "A rolled-up building plan"),
        hotspot("ch2_casefile", 1220, 470, 300, 240, "A grey archive box"),
        hotspot("ch2_computer", 560, 720, 320, 220, "A library terminal"),
    ]
    ch2_school_hotspots = [
        hotspot("ch2_trophy", 220, 350, 300, 300, "The trophy case"),
        hotspot("ch2_poster", 720, 330, 300, 300, "A noticeboard"),
        hotspot("ch2_locker", 1260, 350, 300, 360, "A dented locker"),
    ]

label chapter_02:
    $ current_chapter = 2
    call screen chapter_card("II", "3:00 AM")
    scene bg bedroom day
    with slowfade
    play music audio.ch2 fadein 2.0
    play ambient audio.rain fadein 2.0

    "Morning arrives without asking permission."
    "You have not slept. Your eyes feel like they have been rolled in sand."
    "The phone is on the nightstand, face-up, battery at forty percent. You did not charge it."
    "There are three new messages."

    $ add_message("UNKNOWN", "You didn't open the door.", "3:11 AM")
    $ add_message("UNKNOWN", "That's all right. She can wait.", "3:12 AM")
    $ add_message("UNKNOWN", "Can you?", "3:13 AM")

    "You do not open the phone. You get dressed instead."
    "The photograph from yesterday is still in your pocket. Iris. 3B. Don't forget."
    "You need to know who she is."

    scene bg school
    with slowfade
    stop ambient fadeout 2.0
    "Ashgrove Community College is almost empty on a Saturday."
    "The library occupies the basement of the humanities building. The lights buzz. The air smells of paper and old coffee."
    "You tell the librarian you are looking for local history. She points you toward the archives without looking up."

    scene bg school
    with dissolve
    call ch2_school_explore
    scene bg classroom
    with dissolve
    "You sit at a reading table with a stack of folders and no idea where to begin."
    "Then someone pulls out the chair across from you."

    show maya neutral at char_right_in
    with dissolve
    m "You look worse than yesterday."
    e "You're following me."
    m "I'm researching a building. You're researching a building. It's called a coincidence."
    m "Also, you left your door unlocked. I checked."

    menu:
        "Tell her why you're here.":
            $ gain_trust(2)
            $ told_maya_truth = True
            e "Something is happening in 3B. Messages. Photographs. A girl in the hallway."
            e "I found a picture of my parents and a girl I don't remember."
            show maya surprised
            m "Okay. That's not the answer I expected."
            m "I've been researching Ashgrove for six months. I thought I was the only one who thought it was wrong."
            e "Wrong how?"
            m "Wrong like a word you keep misreading."
            $ change_sanity(4)

        "Tell her to leave it alone.":
            $ gain_trust(-1)
            $ change_sanity(-3)
            e "It's nothing. Family stuff."
            show maya sad
            m "Family stuff that made you look like a ghost in a cardigan."
            m "Fine. I'll leave it alone."
            "She does not leave."

        "Ask what she knows.":
            $ gain_trust(1)
            $ add_clue("maya_notes")
            $ change_sanity(-2)
            e "What do you know about 3B?"
            show maya neutral
            m "I know the previous tenant left in the middle of the night. I know the landlord won't show the apartment after dark."
            m "I know there are seven names in the building records with no move-out dates."
            m "And I know you're the first person to ask about them who looks like they're on the list."
            "She slides a folder across the table. It is warm from her hands."

    "The archive is smaller than it looks."
    "You open folders until the words stop making sense."
    "Maya works beside you. She does not ask questions. She does not stop looking at the door."

    call ch2_explore

    if not has_clue("fire_record"):
        "Near the bottom of the stack, a photocopied newspaper page slides free."
        $ add_clue("fire_record")
        $ change_sanity(-3)
        "The headline is small. The photograph is smaller."

    if not has_clue("blueprint"):
        show maya neutral
        m "There's a room here that doesn't appear on the lease."
        m "The 3B floor plan has a service corridor that was sealed in 1998. Nobody ever removed it from the building."
        $ add_clue("blueprint")
        $ change_sanity(-3)

    "When you look up, the library has gone quiet."
    "Not empty. Quiet. The way a room goes quiet when everyone is listening to someone else."

    show maya scared
    m "Ethan."
    m "The clock says three."
    "You look at your phone. It says 3:00 PM."
    "The lights go out, one row at a time, from the back of the room toward you."
    play sound audio.flicker
    "Then they come back on."
    "Maya is holding your sleeve."

    menu:
        "Show her the photograph.":
            $ gain_trust(2)
            $ change_sanity(-4)
            "You take the photograph out of your pocket and place it between you."
            "Maya looks at it for a long time."
            m "That's my building. That's your mother."
            m "I've seen the girl before. In the hallway. In my dreams."
            m "She never has a face."
            "You turn the photo over. The words are still there. Don't forget."
            m "I don't think that's a suggestion."

        "Keep the photograph to yourself.":
            $ gain_trust(-1)
            $ change_sanity(-2)
            "You put your hand over your pocket."
            "Maya notices. She does not push."
            m "Whatever it is, it's already in the room with us."
            "You do not ask what she means."

    "The archivist appears at the end of the aisle. She does not look at either of you."
    "She says the library is closing. Her mouth moves a half second after the words."

    scene bg street
    with slowfade
    stop ambient fadeout 2.0
    play ambient audio.wind fadein 2.0
    "Outside, the street is the wrong color. Too blue. Too still."

    show maya neutral at char_right
    m "Come back to mine. We can order something terrible and look at the files."
    e "I should go home."
    m "That's what he wants you to do."
    e "Who?"
    m "I don't know. But he's patient."

    menu:
        "Go back to 3B alone.":
            $ change_sanity(-4)
            hide maya
            with dissolve
            "You walk home by yourself."
            "The city is full of windows. In every one, someone is standing very still."

        "Go to Maya's apartment.":
            $ gain_trust(2)
            $ change_sanity(4)
            $ maya_stayed = True
            hide maya
            with dissolve
            "Maya's apartment is full of plants and half-finished craft projects and a wall of red string."
            "It smells like cinnamon. You sit on her floor and eat noodles out of a paper carton and, for an hour, the phone does not ring."

    scene bg livingroom
    with slowfade
    stop ambient fadeout 2.0
    play music audio.ch1 fadein 2.0
    play ambient audio.rain fadein 2.0
    "By the time you get back to 3B, it is dark."
    "You lock the door. You check the closet. You leave the bathroom light on."
    "At 2:59 AM, someone knocks."

    play sound audio.footsteps
    "Three knocks. From the hallway."
    "Then three more. From inside the apartment."

    $ push_message("UNKNOWN", "The girl in the hallway wants to meet you.", stamp="3:00 AM", alert=True, delay=2.2)
    $ push_message("UNKNOWN", "She's been waiting a long time.", stamp="3:00 AM", alert=True, delay=2.0)

    "Your phone rings."
    $ add_call("UNKNOWN", answered=False)
    "You do not answer it. It rings seven times and stops."

    menu:
        "Open the door.":
            $ change_sanity(-12)
            $ knows_iris = True
            $ add_clue("iris_name")
            play sound audio.door_creak
            "You turn the deadbolt. The door swings inward before your hand touches the handle."
            scene cg girl first
            with slowfade
            play music audio.entity fadein 3.0
            $ renpy.pause(1.0)
            "She stands in the hallway with her hands folded in front of her."
            "She is twelve. She has been twelve for a long time."
            i "You left me in the dark."
            e "I don't know you."
            i "Yes, you do."
            i "You used to bring me oranges. You said they were the sun, cut into pieces."
            "Something in your chest folds open. A memory with no pictures."
            i "My name is Iris. You promised you would come back for me."
            e "I'm sorry."
            i "Don't be sorry. Be careful."
            i "He hears apologies. They taste like invitations."
            scene bg hallway
            with dissolve
            play music audio.ch2 fadein 3.0
            i "Ask Maya what she isn't telling you."
            "When you blink, the hallway is empty."
            "There is a small, wet handprint on the doorframe."

        "Look through the peephole.":
            $ change_sanity(-8)
            $ add_clue("girl_in_hall")
            "You press your eye to the cold brass circle."
            scene cg girl first
            with Dissolve(0.7)
            play sound audio.whisper
            "She is standing on the other side, close enough that her face fills the whole circle."
            "Her eyes are not looking at the peephole. They are looking at you through the wall."
            "She raises one hand and places it against the door."
            "The door moves inward half an inch. The chain holds."
            scene bg livingroom
            with dissolve
            "You stumble back. The hallway light flickers under the door."
            "Then goes out."

        "Put your hands over your ears and wait.":
            $ change_sanity(-6)
            "You sit on the floor with your back against the couch and your hands over your ears."
            "The knocking stops."
            "A message arrives."
            $ push_message("UNKNOWN", "I can wait. I've had practice.", stamp="3:09 AM", alert=False)
            "You stay on the floor until the sky turns grey."

    "At 3:10 AM, the phone lights up one last time."
    $ push_message("UNKNOWN", "She remembers you even if you don't.", stamp="3:10 AM", alert=False)
    "You read it until the words stop meaning anything."

    scene black
    with slowfade
    stop ambient fadeout 2.5
    stop music fadeout 3.0
    stop pulse fadeout 2.0
    $ ch2_finished = True
    return

label ch2_explore:
    $ ch2_leave = False
    while not ch2_leave:
        call screen investigate(hotspots=ch2_hotspots, prompt="The archive smells like dust and something sweeter underneath.")
        if _return == "leave":
            $ ch2_leave = True
        else:
            $ ch2_spot = ch2_hotspots[_return]
            call expression ch2_spot["label"]
    return

label ch2_school_explore:
    $ ch2_school_leave = False
    while not ch2_school_leave:
        call screen investigate(hotspots=ch2_school_hotspots, prompt="The school keeps its oldest memories in the basement, but some have climbed upstairs.")
        if _return == "leave":
            $ ch2_school_leave = True
        else:
            $ ch2_spot = ch2_school_hotspots[_return]
            call expression ch2_spot["label"]
    return

label ch2_trophy:
    scene bg school
    with dissolve
    if has_clue("st_agnes_photo"):
        "The children in the photograph are still arranged in two neat rows. Iris is still at the edge."
        return
    "The trophy case is cloudy with fingerprints. Behind the brass cups, a photograph has been taped to the glass."
    "Two rows of children in front of St. Agnes. Iris Vale stands at the edge, holding a music box."
    "Beside her, a boy's face has been scratched out."
    "You recognize your own shirt."
    $ add_clue("st_agnes_photo")
    $ change_sanity(-4)
    $ change_iris_bond(1)
    return

label ch2_poster:
    scene bg school
    with dissolve
    if has_clue("iris_missing_poster"):
        "The poster is still hidden behind the newer notices. The red words have not faded."
        return
    play sound audio.paper
    "A missing-child poster is buried under six layers of club announcements."
    "IRIS VALE. AGE 12. LAST SEEN AT ST. AGNES HOME."
    "The date is the day after the fire."
    "Someone has written across the bottom in red ink: SHE WAS NEVER MISSING."
    $ add_clue("iris_missing_poster")
    $ change_sanity(-5)
    $ change_iris_bond(1)
    return

label ch2_locker:
    scene bg school
    with dissolve
    if has_clue("locker_names"):
        "The locker is still open. The names are still fresh."
        return
    play sound audio.knife
    "The locker door is dented and hanging open. The inside is empty except for the scratches."
    "Seven names. Six have dates beside them."
    "The seventh is yours. The scratches are fresh."
    $ add_clue("locker_names")
    $ change_sanity(-5)
    $ change_attention(1)
    return

label ch2_newspaper:
    scene bg classroom
    with dissolve
    if has_clue("fire_record"):
        "The photocopy is already in your bag. You can still see the headline when you close your eyes."
        return
    play sound audio.paper
    "The newspaper is brittle at the edges. The date is eleven years old."
    "{i}ST. AGNES HOME FOR CHILDREN — FIRE KILLS ONE, ONE MISSING.{/i}"
    "The building on Ashgrove Street was a children's home until 2009. The fire started in the basement."
    "A girl named Iris Vale, age twelve, was never found."
    "The article says the building was scheduled for demolition. It does not say why it wasn't."
    $ add_clue("fire_record")
    $ change_sanity(-5)
    "Iris. The name from the photograph."
    return

label ch2_blueprint:
    scene bg classroom
    with dissolve
    if has_clue("blueprint"):
        "You have already memorized the crooked little room behind the wardrobe."
        return
    "The blueprint is wrapped around a cardboard tube. The paper is soft with age."
    "Apartment 3B is laid out in clean blue lines: bedroom, bathroom, kitchen, living room."
    "And then, behind the bedroom wall, a narrow rectangle with no windows and no door."
    "A service corridor. Sealed in 1998."
    "Somebody has drawn a question mark inside it in red ink."
    $ add_clue("blueprint")
    $ change_sanity(-4)
    return

label ch2_casefile:
    scene bg classroom
    with dissolve
    if has_clue("case_file"):
        "You wish the case file had been empty."
        return
    "The grey box is labeled with an apartment number. 3B."
    "Inside is a fire marshal's report, a death certificate, and a photograph of a burned room."
    "The report lists one casualty."
    "Ethan Mercer. Age thirteen."
    "You read your own name on the certificate. Then you read it again."
    "The date of death is seven years ago."
    $ add_clue("case_file")
    $ change_sanity(-9)
    play sound audio.heartbeat
    "Your heart is beating. You can feel it in your teeth."
    "The certificate is warm. The ink is fresh."
    return

label ch2_computer:
    scene bg classroom
    with dissolve
    if has_clue("mom_email"):
        "You can still see the email in your head. You wish you couldn't."
        return
    "The terminal is old enough to hum. You log into the archive guest account."
    "There is one saved message in the local history folder. It is addressed to you."
    "{i}Ethan. If you are reading this, you have started to remember. We are sorry we could not tell you in person. The arrangement was not meant to last this long. Do not let him see you look behind you. — Mom{/i}"
    "The timestamp is six years ago. The sender address no longer exists."
    $ add_clue("mom_email")
    $ change_sanity(-5)
    "You print the email. The printer produces a blank page."
    "When you look back at the screen, the message is gone."
    return
