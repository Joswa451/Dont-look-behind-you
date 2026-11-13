label start:
    $ current_chapter = 1
    $ sanity = 80
    $ trust_maya = 0
    $ clues = set()
    $ phone_messages = []
    $ phone_calls = []
    $ phone_unread = 0
    $ phone_photo_unlocked = False
    $ remembered = False
    $ destroyed_box = False
    $ kept_box = False
    $ answered_seventh = False
    $ saved_maya = False
    $ knows_iris = False
    $ told_maya_truth = False
    $ maya_stayed = False
    $ key_hidden_room = False
    $ ch1_finished = False
    $ ch2_finished = False
    $ ch3_finished = False
    $ ch4_finished = False
    $ ch5_finished = False
    $ ch6_finished = False

    call chapter_01
    call chapter_02
    call chapter_03
    call chapter_04
    call chapter_05
    call chapter_06
    call chapter_07

    jump ending_call
