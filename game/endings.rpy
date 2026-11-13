label ending_truth:
    $ unlock_ending(1)
    scene cg ending truth
    with slowfade
    stop ambient fadeout 2.0
    stop pulse fadeout 2.0
    play music audio.ending_truth fadein 3.0

    "You do not turn around."
    "You say her name."
    e "Iris Vale."
    e "I heard you. I'm sorry. I'm not leaving you in the dark."
    "The room goes very still."
    listener "Again."
    e "Iris Vale."
    "You say it until it doesn't hurt."
    "You say it until it does."
    e "I heard you. I was scared. I left you. I'm sorry."
    "The circle on the floor begins to fade."
    i "I know."
    "Iris steps out of the red paint. For the first time, she looks twelve and tired and free."
    i "I waited a long time."
    e "I know."
    i "I'm not angry anymore."
    e "You should be."
    i "Maybe. But I'm not."
    "Your parents are standing by the wardrobe. They are not burned. They are just your parents, in the clothes they wore in the photograph."
    mom "Ethan."
    dad "We're sorry."
    mom "We loved you too much to let you go."
    dad "We should have let you go."
    e "I know."
    "You do not know if you forgive them. You know that you are tired of carrying it."
    "The music box opens in your hands."
    play sound audio.music_box
    "The melody is small and sweet and terribly brave."
    "The Listener makes a sound like a house settling."
    listener "You were mine."
    e "No."
    listener "You were dead."
    e "I was loved."
    "The walls go quiet."
    "The phone goes dead."
    "Your heart slows."

    if saved_maya:
        scene cg ending truth
        with Dissolve(0.8)
        "Maya is holding your hand when it happens."
        "You feel her grip tighten. You feel her decide not to let go."
        "You wish you could tell her it's all right."
        "You hope she knows."
    else:
        "Maya is not here."
        "You hope she is somewhere warm."

    scene bg bedroom day
    with slowfade
    stop music fadeout 4.0
    "At dawn, Maya wakes on the floor of 3B."
    "The apartment is empty. The wardrobe is gone. The walls are smooth and white."
    "On the windowsill, there is a photograph of a boy and a girl at a birthday party. Neither face is scratched out."
    "She leaves a cup of coffee there every morning."
    "She never answers the phone at three."

    "The building is demolished in spring."
    "At the memorial for the children of St. Agnes, there is a new stone with your name on it."
    "Under the date, someone has written three words in careful letters."
    "{i}BELOVED. REMEMBERED. FREE.{/i}"

    "You were here."
    "You were loved."
    "You were not alone at the end."

    call screen ending_stamp(1, "THE TRUTH", "Some doors close only when you stop knocking.")
    jump credits_after_ending

label ending_alone:
    $ unlock_ending(2)
    scene cg ending alone
    with slowfade
    stop ambient fadeout 2.0
    stop pulse fadeout 2.0
    play music audio.ending_alone fadein 3.0

    "You take Maya's hand."
    "You run."
    "The hallway stretches. The doors repeat. The carpet turns to water under your feet."
    "You do not look back."
    "You do not look at the reflections."
    "You do not answer the phone in your pocket, even when it starts to ring."
    "You hit the stairwell. The street. The cold air."
    "Behind you, the window of 3B is dark."

    "You do not stop running until the city is unfamiliar."
    "Months later, you live in a small apartment with too many locks."
    "Maya sleeps with the light on. You sleep with your back to the wall."
    "Neither of you talks about the room behind the wardrobe."
    "Neither of you has to."

    "At 3:00 AM, a phone rings."
    "It is always a phone you do not remember buying."
    "You never answer."
    "But sometimes, when Maya is asleep, you listen to the voicemail."
    "It is always your voice."
    "It says: I'm here."
    "You delete it."
    "It comes back."

    "You are never alone."
    "You were never alone."

    call screen ending_stamp(2, "YOU WERE NEVER ALONE", "He followed you out. He was always the one behind you.")
    jump credits_after_ending

label ending_call:
    $ unlock_ending(3)
    scene cg ending call
    with slowfade
    stop ambient fadeout 2.0
    stop pulse fadeout 2.0
    play music audio.ending_call fadein 3.0

    "You lift the receiver."
    i "Don't—"
    listener "I'm here."
    e "I'm here."
    "The apartment folds inward."
    "The walls become the inside of a mouth. The floor becomes a tongue."
    "The phone cord goes down and down and down."

    if saved_maya:
        "Maya screams your name."
        "You hear it from a long way off, the way you used to hear Iris through the wall."
        "You do not turn around."
    else:
        "There is no one left to scream."

    "The dial tone becomes a lullaby."
    "The lullaby becomes a voice."
    "The voice becomes yours."

    scene bg bedroom day
    with slowfade
    "One year later, a new tenant signs for 3B."
    "He is twenty years old. He has two suitcases and a key that feels older than he does."
    "The apartment is cheap. The agency calls it a bargain."
    "He does not ask what happened to the last tenant."

    "At 2:58 AM, he is awake."
    "At 2:59 AM, the rain stops."
    "At 3:00 AM, his phone rings."

    "The screen shows no number."
    "He answers anyway."

    stranger "You're home."
    "He has seven days."
    "You are patient."
    "You have practice."

    call screen ending_stamp(3, "THE SEVENTH CALL", "The phone is still ringing. This time, it is your turn to wait.")
    jump credits_after_ending

label ending_newgame:
    $ unlock_ending(4)
    scene cg ending newgame
    with slowfade
    stop ambient fadeout 2.0
    stop pulse fadeout 2.0
    play music audio.ending_newgame fadein 2.0

    "You look behind you."
    "There is no one there."
    "Then the room turns inside out."
    "You are looking at yourself from the other side of the glass."
    "You see the apartment. The boxes. The key on the windowsill."
    "You see a new tenant standing in the doorway, holding two cups of coffee."
    "He is younger than you remember being."
    "He is smiling."
    "You try to warn him. Your mouth forms the words. No sound comes out."

    "On his phone, at 3:00 AM, a message appears."
    "{i}DON'T LOOK BEHIND YOU.{/i}"
    "He looks anyway."

    "The title screen flickers."
    "The music starts again."
    "The cursor moves to NEW GAME."

    "There was never an ending."
    "Only another beginning."

    call screen ending_stamp(4, "NEW GAME", "The only way out is to begin again.")
    jump credits_after_ending

label ending_failed_truth:
    stop music fadeout 2.0
    play pulse audio.heartbeat fadein 1.0
    "You open your mouth."
    "The name is not there."
    "You remember a girl. You remember a door. You remember the shape of a hand."
    "It is not enough."
    listener "You don't even know what you're apologizing for."
    "The phone rings in your hand."
    "You answer it."
    $ answered_seventh = True
    jump ending_call

label ending_failed_run:
    stop music fadeout 2.0
    play pulse audio.heartbeat fadein 1.0
    "You run."
    "The hallway folds. The floor tilts. Every door opens onto the bedroom."
    "The wardrobe is waiting at the end of the hall."
    "The phone is still in your hand."
    "It rings."
    "You answer it."
    $ answered_seventh = True
    jump ending_call

label credits_after_ending:
    call screen credits_end
    $ renpy.full_restart()
    return
