init python:
    ch3_hotspots = [
        hotspot("ch3_musicbox", 250, 560, 330, 250, "A music box on a crate"),
        hotspot("ch3_drawings", 760, 380, 300, 250, "Drawings taped to the pipes"),
        hotspot("ch3_names", 1290, 300, 300, 260, "Names carved into the wall"),
        hotspot("ch3_boiler", 1400, 620, 300, 250, "The old boiler"),
        hotspot("ch3_piano", 620, 620, 340, 230, "The piano with no keys"),
    ]

label chapter_03:
    $ current_chapter = 3
    call screen chapter_card("III", "The Girl in the Hallway")
    scene bg bedroom day
    with slowfade
    play music audio.ch3 fadein 2.0
    play ambient audio.rain fadein 2.0

    "You wake on the floor with your phone clutched to your chest."
    "The apartment is full of grey light. The door is still locked. The chain is still on."
    "There is a message from Maya."

    $ add_message("MAYA", "You alive?", "8:12 AM")
    $ add_message("MAYA", "I found something in the basement. You need to see it.", "8:13 AM")
    $ add_message("MAYA", "Bring the photograph.", "8:13 AM")

    "You check the peephole. The hallway is empty, but the little brass circle is warm."
    "You take the photograph out of your pocket and look at the scratched-out face."
    "Iris."

    if knows_iris:
        "You say the name out loud. The radiator knocks once, like a reply."
        $ change_sanity(2)
    else:
        "The name feels like a stone in your mouth."
        $ change_sanity(-2)

    play sound audio.footsteps
    "Maya is waiting in the hallway with a shoebox and a flashlight."
    $ add_item("flashlight", silent=True)
    show maya neutral at char_right_in
    with dissolve
    m "I went down to the laundry room. The door at the end of the hall was open."
    m "It shouldn't be open. It's been painted shut since before I moved in."
    e "What did you find?"
    m "Tapes. A box of them. They all have your name on the label."
    show maya scared
    m "And a music box. It was playing when I found it."
    e "Playing what?"
    m "I don't know. It stopped when I looked at it."

    menu:
        "Tell her about Iris.":
            $ gain_trust(2)
            $ told_maya_truth = True
            $ knows_iris = True
            $ add_clue("iris_name", silent=True)
            e "There's a girl. Her name is Iris. She was in the hallway last night."
            e "She says I knew her. She says I promised to come back."
            show maya sad
            m "I believe you."
            e "Just like that?"
            m "I've heard her too. I thought I was losing my mind."
            m "It's a relief, honestly. Losing your mind is lonely."
            $ change_sanity(4)

        "Ask her to show you the box.":
            $ gain_trust(1)
            $ change_sanity(-2)
            e "Show me."
            show maya neutral
            m "No questions?"
            e "I'm saving them for the basement."
            m "Good. The basement has better acoustics."

        "Tell her to put it back.":
            $ gain_trust(-2)
            $ change_sanity(-4)
            e "Put it back. Whatever it is, put it back."
            show maya angry
            m "You think I went down there for fun?"
            m "Something is wrong with this building, Ethan. You can pretend it's not happening, but it is."
            "She shoves the shoebox into your hands anyway."

    hide maya
    with dissolve
    "The door at the end of the hall is open."
    "Cold air rises from the stairwell, carrying the smell of wet concrete and something sweet."

    scene bg underground
    with slowfade
    stop ambient fadeout 2.0
    play ambient audio.drip fadein 1.0
    play sound audio.footsteps
    "The stairs go down farther than they should."
    "You count twelve steps. Then twelve more. Then you stop counting."
    "Maya's flashlight beam slides over pipes, old laundry machines, a wall of painted-over doors."
    "At the bottom, there is a room that is not on the blueprint."

    scene bg basement
    with slowfade
    play music audio.ch3 fadein 2.0
    "The basement is full of abandoned things."
    "Chairs stacked like kindling. A piano with no keys. A row of children's coats hanging on a pipe."
    "The music box sits on a wooden crate in the middle of the floor, untouched."

    call ch3_explore

    if not has_clue("music_box"):
        "Before you leave, the music box begins to play by itself."
        play sound audio.music_box
        "A thin, sweet melody. Three notes, then three more."
        $ add_clue("music_box")
        $ change_sanity(-4)

    if not has_clue("drawings"):
        "One of the drawings falls from the wall and lands at your feet."
        "A tall figure with no face. A small room. A telephone."
        $ add_clue("drawings")
        $ change_sanity(-3)

    play sound audio.door_slam
    with vpunch
    "The basement door slams shut."
    "Maya's flashlight goes out."

    show girl neutral at char_center_in
    with slowfade
    play music audio.entity fadein 2.0
    "In the dark, someone small is standing beside the piano."
    i "You came down."
    if knows_iris:
        e "Iris."
        show girl sad
        i "You remember my name."
        i "That's more than you did last time."
    else:
        e "Who are you?"
        i "You know who I am. You just don't want to."
        $ knows_iris = True
        $ add_clue("iris_name")
        $ change_sanity(-4)

    i "I used to live in the walls."
    i "Not this building. The one inside it."
    i "The matron said the listening room was where bad children went to be quiet."
    i "She was wrong. It was where the quiet went to become a person."

    e "The Listener."
    show girl surprised
    i "You know his name."
    e "I've heard it."
    i "He's heard you too. That's how it works."

    "Iris walks around the music box without touching it."
    i "He takes the ones who answer. I answered because I was lonely."
    i "You heard me through the wall. You were little. You promised to open the door."
    i "You didn't."
    "The words land somewhere deep and old."

    menu:
        "Apologize.":
            $ change_sanity(-5)
            e "I'm sorry. I was a child."
            i "I know."
            i "He doesn't."
            m "Ethan."
            "Maya's voice comes from somewhere behind the piano."
            "You cannot see her."
            i "He uses the sorry ones. It makes them easier to wear."

        "Ask how to stop him.":
            $ gain_trust(1)
            $ change_sanity(-2)
            e "How do I stop him?"
            i "You don't."
            i "You remember me. You say my name where he can hear it. You close the door he opened."
            e "What door?"
            i "The one behind you."

        "Run.":
            $ change_sanity(-8)
            "You turn toward the stairs."
            i "Don't."
            "Your legs do not move."
            i "He likes it when you run. It means you still think there's somewhere to go."

    show girl sad
    i "You have four days left."
    i "On the seventh night, he'll call. If you answer, he keeps you."
    i "If you don't, he takes someone else."
    e "Who?"
    i "Whoever is standing closest."
    "From behind the piano, Maya says your name."

    "Your phone rings."
    "The screen says MOM."

    call screen incoming_call(caller="MOM", subtitle="3:03 AM")

    if _return == "answer":
        $ add_call("MOM", answered=True)
        $ add_clue("mom_call")
        $ change_sanity(-7)
        play sound audio.static
        mom "Ethan. Listen to me. Don't look behind you."
        e "Mom?"
        mom "He can only move when you're looking at him. He can only speak when you answer."
        mom "The music box is the lock. Your father's blood is the key."
        mom "Remember the girl. Say her name where he can hear it."
        e "Where are you?"
        mom "We're sorry. We should have—"
        play sound audio.glitch
        stranger "That's enough."
        "The call drops."
        "The screen goes black. Your reflection is not in it."
    else:
        $ add_call("MOM", answered=False)
        $ change_sanity(-3)
        $ push_message("MOM", "I'm sorry. We should have told you. The music box is the lock. Don't let him—", stamp="3:04 AM", alert=False)
        $ add_voicemail("MOM", "I'm sorry. We should have told you. The music box is the lock. Don't let him finish the call.", audio.voicemail_mom, stamp="3:04 AM", duration="0:16")
        "The message ends there."
        "A voicemail notification remains on the screen."
        "You play it again. The last word is different each time."

    show girl sad at char_center
    i "She called you."
    i "She's been calling for six years. You just stopped hearing her."
    "Iris looks at the music box."
    i "When you're ready, come back. Bring the box. Bring Maya."
    i "And whatever you do, don't look behind you."

    hide girl
    with slowfade
    play sound audio.door_creak
    "The basement door opens. The staircase is lit by a single bulb."
    "Maya is standing at the bottom of the stairs, holding her flashlight with both hands."
    show maya scared at char_right
    if trust_maya >= 4:
        m "I heard her."
        m "I heard all of it."
        $ gain_trust(1)
        $ change_sanity(3)
        "You do not have to explain. She takes your hand instead."
    else:
        m "You were talking to someone."
        m "There's no one there, Ethan."
        $ change_sanity(-3)
        "You look at the place where Iris was standing."
        "The floor is dry."

    scene black
    with slowfade
    stop ambient fadeout 2.0
    stop music fadeout 3.0
    $ ch3_finished = True
    return

label ch3_explore:
    $ ch3_leave = False
    while not ch3_leave:
        call screen investigate(hotspots=ch3_hotspots, prompt="The basement is listening.")
        if _return == "leave":
            $ ch3_leave = True
        else:
            $ ch3_spot = ch3_hotspots[_return]
            call expression ch3_spot["label"]
    return

label ch3_musicbox:
    scene bg basement
    with dissolve
    if has_clue("music_box"):
        "The music box is still on the crate. The lid is open now. You are sure you closed it."
        return
    "The music box is smaller than your palm, made of dark wood and brass."
    "Someone has carved three letters into the lid: I.V."
    "You open it."
    play sound audio.music_box
    "A tiny metal dancer turns in a circle. The melody is familiar in a way that has no memory attached."
    "Inside the lid, tucked under the velvet, is a lock of dark hair tied with red thread."
    $ add_clue("music_box")
    $ change_sanity(-6)
    "When the music stops, the dancer is facing you."
    "You close the lid. The melody continues for three more notes."
    return

label ch3_drawings:
    scene bg basement
    with dissolve
    if has_clue("drawings"):
        "The drawings are still taped to the pipes. You have counted them twice. There are more each time."
        return
    play sound audio.paper
    "There are drawings taped to the pipes in a neat row. Children's drawings, done in crayon."
    "A tall figure with no face. A room with no windows. A telephone with a long cord that goes into the floor."
    "One drawing shows a boy standing outside a door. The boy is labeled ETHAN."
    "The door is labeled IN HERE."
    "There are scratch marks drawn over the door. Hundreds of them."
    $ add_clue("drawings")
    $ change_sanity(-6)
    "You take the drawing of the boy. It is warm."
    return

label ch3_names:
    scene bg basement
    with dissolve
    if has_clue("name_list"):
        "You do not want to read the names again. Your eyes find yours anyway."
        return
    play sound audio.knife
    "Someone has carved names into the concrete beside the boiler."
    if not flashlight_on:
        "The corner is too dark to read them clearly. You can barely make out the shape of the letters."
        $ change_attention(1)
    else:
        "The flashlight beam picks the names out of the concrete."
    "Seven names. The first six have dates beside them."
    "The seventh is yours."
    "ETHAN MERCER. No date."
    "Below it, in smaller letters, someone has written: {i}HE CAME BACK WRONG.{/i}"
    $ add_clue("name_list")
    $ change_sanity(-8)
    "You touch the carving. The concrete is warm."
    return

label ch3_piano:
    scene bg basement
    with dissolve
    if has_clue("piano_keys"):
        "The piano is still silent. The fingerprints are still there."
        return
    "The piano has no keys. The wooden strip where they should be is smooth and dustless."
    if flashlight_on:
        "Your flashlight finds child-sized fingerprints pressed into the wood above the missing keyboard."
        "Someone practiced here for a long time. The prints face the wall."
    else:
        "You can only see the shape of the piano. The flashlight would show you more."
        "When you touch the wood, your fingers find small dents arranged like a keyboard."
    $ add_clue("piano_keys")
    $ change_sanity(-4)
    $ change_iris_bond(1)
    return

label ch3_boiler:
    scene bg basement
    with dissolve
    if has_clue("boiler_handprint"):
        "The handprint on the boiler is still there. It has moved six inches to the left."
        return
    "The old boiler is dead, but the metal is warm."
    "A handprint is pressed into the rust, small and delicate, as if someone leaned there for a long time."
    "You put your hand beside it. It fits."
    play sound audio.breathing
    "From inside the boiler, something breathes in."
    "Then out."
    "Then in again, in time with you."
    $ add_clue("boiler_handprint")
    $ change_sanity(-7)
    "You step back. The breathing keeps going."
    return
