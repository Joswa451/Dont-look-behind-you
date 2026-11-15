init -20 python:
    def stop_voice_channels():
        renpy.sound.stop(channel="charvoice")
        renpy.sound.stop(channel="narrvoice")

    def line_voice(event, interact=True, what=None, voice_role="narrator", **kwargs):
        if event != "begin" or not interact or not config.has_voice:
            return

        stop_voice_channels()

        tlid = renpy.game.context().translate_identifier
        if not tlid:
            source, line = renpy.get_filename_line()
            source = source.replace("\\", "/").rsplit("/", 1)[-1]
            tlid = VOICE_IDS_BY_LOCATION.get((source, line))

        if not tlid:
            store.last_voice_file = None
            store.last_voice_role = None
            renpy.log("Voice identifier missing for dialogue at %s:%s" % renpy.get_filename_line())
            return

        channel = "narrvoice" if voice_role == "narrator" else "charvoice"
        filename = "audio/voice/%s.ogg" % tlid
        if not renpy.loadable(filename):
            store.last_voice_file = None
            store.last_voice_role = None
            renpy.log("Voice audio file is missing: %s" % filename)
            return

        renpy.sound.play(filename, channel=channel)
        store.last_voice_file = filename
        store.last_voice_role = voice_role

    def replay_last_voice():
        if not store.last_voice_file:
            return

        if not renpy.loadable(store.last_voice_file):
            renpy.log("Last voice audio file is missing: %s" % store.last_voice_file)
            return

        stop_voice_channels()
        channel = "narrvoice" if store.last_voice_role == "narrator" else "charvoice"
        renpy.sound.play(store.last_voice_file, channel=channel)