init python:
    ch5_hotspots = [
        hotspot("ch5_tape", 240, 610, 330, 250, "A tape recorder"),
        hotspot("ch5_diary", 760, 620, 300, 250, "A small red diary"),
        hotspot("ch5_photo", 1140, 300, 300, 250, "A photograph on the wall"),
        hotspot("ch5_altar", 1400, 540, 320, 280, "The altar"),
        hotspot("ch5_names", 480, 280, 300, 260, "Seven names in the plaster"),
    ]

label chapter_05:
    $ current_chapter = 5
    call screen chapter_card("V", "The Hidden Room")
    scene bg bedroom
    with slowfade
    play music audio.ch5 fadein 2.0
    play ambient audio.wind fadein 2.0

    "The key fits the wardrobe lock."
    "You turn it, and the lock opens with a sound like a small animal waking."
    "Behind the coats, the back panel swings inward."

    if maya_stayed:
        show maya scared at char_right_in
        with dissolve
        m "I want to say something reassuring."
        e "Go ahead."
        m "I've got nothing."
        "She takes your hand. Her palm is sweating. So is yours."
    else:
        "You look at the empty apartment behind you."
        "Then you step through alone."

    play sound audio.door_creak
    scene cg hidden room
    with slowfade
    "The hidden room is narrow enough to touch both walls at once."
    "It has no windows. The air is cold and completely still."
    "Someone has drawn a circle on the floor in faded red paint. Inside the circle, seven small handprints."
    "On the far wall, a wooden shelf holds a tape recorder, a red diary, a row of photographs, and the music box."
    "Above the shelf, seven names are carved into the plaster."
    "The seventh is yours."

    scene bg hiddenroom
    with dissolve
    $ change_sanity(-7)

    "You have the feeling of stepping into a photograph that has been waiting for you."
    "The room is smaller than the blueprint said. The walls are closer."
    "The music box is on a low table in the center of the circle. Its lid is closed."
    "The tape recorder is already running."

    call ch5_explore

    if not has_clue("bargain_tape"):
        "The tape recorder clicks. Your father's voice fills the room."
        $ add_clue("bargain_tape")
        $ change_sanity(-6)
        "You cannot make yourself stop listening."

    if not has_clue("iris_diary"):
        "The red diary falls open at your feet."
        $ add_clue("iris_diary")
        $ change_sanity(-5)
        "The last page is written in careful, looping letters."

    "When the tape ends, the room is so quiet you can hear the house settling around you."
    "Then the music box opens by itself."
    play sound audio.music_box
    "Three notes. Three more. The same melody from the basement."
    "Iris is standing inside the circle. You did not see her arrive."

    show girl sad at char_center_in
    with Dissolve(0.7)
    i "You found it."
    e "The hidden room?"
    i "The part of the story where you stop pretending."

    "She looks at the music box."
    i "That was mine. The matron took it when she locked me in here."
    i "She said music made me selfish."
    i "I only wanted to hear something besides the pipes."

    "Maya makes a small sound behind you. Iris does not look at her."
    i "He's been using your parents' voices. He's been using mine."
    i "He can't make a voice of his own. That's why he needs you."
    e "Why me?"
    i "Because you came back."
    i "The others he takes. You he keeps."

    play sound audio.phone_ring
    "The telephone on the altar rings."
    "It is an old rotary phone, covered in dust. It has no cord."
    "You pick it up."

    play music audio.entity fadein 2.0
    listener "Hello, Ethan."
    listener "You've grown."
    e "What are you?"
    listener "I am the thing that was already in the room when you were born."
    listener "The listening. The waiting. The shape behind the door."
    listener "Your parents gave you to me for seven years. They thought they could buy you a life."
    listener "They bought you a delay."
    e "Where are they?"
    listener "Gone. Mostly."
    listener "They are in the walls. In the phone lines. In the part of you that still expects them to come home."
    listener "If you want to see them, answer the seventh call."
    listener "Tomorrow. Three in the morning. I'll be waiting."

    "The line goes dead. The dial tone is the sound of someone breathing."

    show girl sad
    i "Don't listen to him."
    i "He tells the truth the way a hook tells the truth about water."
    i "The box is the lock. Your blood is the key. My name is the door."
    i "If you play it, you'll remember everything."
    i "If you break it, you'll close the door."
    i "But a door that closes can't be opened again."

    menu:
        "Play the music box.":
            $ remembered = True
            $ change_sanity(-8)
            play sound audio.music_box
            scene cg hidden room
            with slowfade
            "You wind the box. The dancer turns."
            "The room changes around you."
            "You are seven years old. The wall is open. Iris is on the other side, crying."
            "You can hear the fire above you. You can hear your mother screaming your name."
            "You put your hand through the gap. Iris reaches for it."
            "The door slams shut."
            "You run."
            "You tell yourself you went for help. You tell yourself the door was locked."
            "You know both things are lies."
            scene bg hiddenroom
            with slowfade
            $ add_clue("iris_diary", silent=True)
            "You come back to the hidden room with your face wet."
            i "There you are."
            i "I've been waiting for you to look at that."
            show girl sad
            i "You were a child. He was already here. None of it was your fault."
            i "But he uses the not-your-fault like a door."
            "Maya's hand finds yours. She does not let go."

        "Destroy the music box.":
            $ destroyed_box = True
            $ change_sanity(-5)
            play sound audio.knife
            "You bring the music box down against the floor."
            play sound audio.glitch
            with vpunch
            "The wood splits. The dancer snaps in half."
            "Something screams inside the walls. Not a person. A room."
            i "No—"
            "Iris flickers like a bad signal."
            "The phone on the altar rings once, very loud, and then melts."
            show girl scared
            i "You closed it. You closed it before you remembered."
            i "That's all right. That's all right."
            "She is crying. You do not know if ghosts can cry."
            "The room goes dark."

        "Take the music box and leave.":
            $ kept_box = True
            $ change_sanity(-2)
            "You pick up the music box. It is warm, as if someone has been holding it."
            i "You're going to have to choose eventually."
            e "I know."
            i "No. You don't."
            i "He'll make you think you have more time."
            "She steps aside. The circle on the floor remains unbroken."

    if remembered:
        "The memory sits in you like a swallowed stone."
        "You can feel Iris through the wall. You can feel the fire. You can feel the exact moment you decided to run."
    elif destroyed_box:
        "The broken music box is still in your hands. The melody is gone."
        "You can still hear it in your teeth."
    else:
        "The music box is a small, heavy weight under your arm."
        "You can feel it ticking, very faintly, like a second heart."

    listener "One night left."
    "The voice comes from everywhere. From the walls. From the floor. From the inside of your own mouth."
    listener "Bring the box. Bring the girl. Bring whoever you want to lose."

    "Maya pulls you toward the wardrobe."
    if not maya_stayed:
        show maya scared at char_right_in
        with dissolve
        m "Ethan?"
        m "Your door was open. I heard voices."
        m "What is this room?"
        $ maya_stayed = True
        $ gain_trust(1)
    m "We need to go."
    m "Ethan. Look at me. We need to go now."
    "You look at her."
    "For a moment, you are almost sure she is real."

    hide girl
    hide maya
    with slowfade
    scene bg bedroom
    with blackout
    stop ambient fadeout 2.0
    stop music fadeout 3.0

    $ push_message("UNKNOWN", "Five days down. Two to go.", stamp="5:59 AM", alert=False)
    "You sit on the bedroom floor with the music box between you and Maya until the sun comes up."
    "Neither of you says anything."
    "The wardrobe door stands open behind you. It is not dark inside. It is waiting."

    scene black
    with slowfade
    $ ch5_finished = True
    return

label ch5_explore:
    $ ch5_leave = False
    while not ch5_leave:
        call screen investigate(hotspots=ch5_hotspots, prompt="The hidden room is full of things that were kept from you.")
        if _return == "leave":
            $ ch5_leave = True
        else:
            $ ch5_spot = ch5_hotspots[_return]
            call expression ch5_spot["label"]
    return

label ch5_tape:
    scene bg hiddenroom
    with dissolve
    if has_clue("bargain_tape"):
        "The tape has stopped. You can still hear your father clearing his throat."
        return
    play sound audio.tape
    scene cg bargain flashback
    with slowfade
    "You press play. The tape hisses for a long time."
    dad "We know what it costs."
    mom "We've read the books. We've made the calls. We know."
    dad "Take us instead. Let him have the years. Let him grow up."
    "A third voice answers. It is not a voice so much as a room with a mouth."
    listener "Seven years."
    mom "Seven."
    listener "And when he remembers, he belongs to me."
    "Your mother begins to cry. Your father says her name, over and over, like a prayer that has stopped working."
    "The tape clicks off."
    scene bg hiddenroom
    with dissolve
    $ add_clue("bargain_tape")
    $ change_sanity(-8)
    "Seven years ago, you were thirteen."
    "You are twenty now."
    "The math is a hand closing around your throat."
    return

label ch5_diary:
    scene bg hiddenroom
    with dissolve
    if has_clue("iris_diary"):
        "The diary is still open. The pages have started to curl at the corners."
        return
    play sound audio.paper
    "The diary is small enough to fit in a coat pocket. The cover is soft with handling."
    "Most of the pages are drawings. A girl with a music box. A boy in a window. A door with no handle."
    "The last page is written in careful, looping letters."
    "{i}The lady says if I am very quiet, the listening man will bring me a friend.{/i}"
    "{i}I heard a boy through the wall. He said his name is Ethan. He said he would open the door.{/i}"
    "{i}I am still waiting. I am not angry. I am just very tired of the dark.{/i}"
    $ add_clue("iris_diary")
    $ change_sanity(-6)
    "You close the diary. The room feels smaller than it did before."
    return

label ch5_photo:
    scene bg hiddenroom
    with dissolve
    if has_clue("photo_iris"):
        "The photograph is still pinned to the wall. You and Iris, side by side."
        return
    "A photograph is pinned to the plaster with a rusted nail."
    "You are six years old, standing in front of a birthday cake. Iris is beside you, holding a paper crown."
    "You are both laughing. Her face is not scratched out."
    "On the back, in a child's handwriting: {i}ETHAN + IRIS. BEST FRIENDS. DO NOT FORGET.{/i}"
    $ add_clue("photo_iris")
    $ change_sanity(-5)
    "You do not remember the birthday. You remember the paper crown."
    "You remember wanting to give it to someone."
    return

label ch5_altar:
    scene bg hiddenroom
    with dissolve
    if has_clue("altar"):
        "The altar is still there. The phones are still ringing, one after another, very softly."
        return
    "The altar is a low table covered with a stained white cloth."
    "On it: seven old telephones. Six are black. The seventh is red."
    "Each phone has a name written on the handset in silver ink."
    "The red phone has your name."
    "Beside it, a candle burns with a flame that gives off no heat."
    $ add_clue("altar")
    $ change_sanity(-6)
    "The red phone rings once. You do not answer it."
    "The candle flame leans toward you."
    return

label ch5_names:
    scene bg hiddenroom
    with dissolve
    if has_clue("name_list_hidden"):
        "The names are still there. Yours is still last."
        return
    "The names in the plaster are deeper than the ones in the basement."
    "Six names, with dates. The seventh name has no date."
    "Under your name, someone has carved a sentence in a different hand."
    "{i}HE WAS THE ONLY ONE WHO HEARD ME.{/i}"
    $ add_clue("name_list_hidden")
    $ change_sanity(-5)
    "You touch the words. The plaster is warm."
    return
