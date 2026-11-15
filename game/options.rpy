define config.name = _("DON'T LOOK BEHIND YOU")
define config.version = "1.0.1"
define gui.show_name = True

define config.save_directory = "dontlookbehindyou-1"
define config.window_title = "DON'T LOOK BEHIND YOU"

define config.has_sound = True
define config.has_music = True
define config.has_voice = True
define config.main_menu_music = "audio/music/music_menu.ogg"

define config.enter_transition = Dissolve(0.35)
define config.exit_transition = Dissolve(0.35)
define config.intra_transition = Dissolve(0.2)
define config.after_load_transition = Dissolve(0.5)
define config.end_game_transition = Fade(0.8, 0.2, 0.8, color="#000")

define config.window = "auto"
define config.window_show_transition = Dissolve(0.2)
define config.window_hide_transition = Dissolve(0.2)

define config.rollback_enabled = True
define config.hard_rollback_limit = 100
define config.autosave_on_quit = True
define config.autosave_slots = 3
define config.default_text_cps = 38
define config.default_afm_time = 12
define config.check_conflicting_properties = True

default preferences.text_cps = 38
default preferences.afm_time = 12
default preferences.music_volume = 0.75
default preferences.sfx_volume = 0.8

init python:
    build.name = "DontLookBehindYou"
    build.directory_name = "DontLookBehindYou"
    build.executable_name = "DontLookBehindYou"
    build.include_update = False
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)
    build.classify("backups/**", None)
    build.classify("android.keystore", None)
    build.classify("bundle.keystore", None)
    build.classify("game/saves/**", None)
    build.classify("traceback.txt", None)
    build.classify("log.txt", None)
    # Website sources and release artifacts are not part of the game build.
    build.classify("public/**", None)
    build.classify("src/**", None)
    build.classify("dist/**", None)
    build.classify("release/**", None)
    build.classify("node_modules/**", None)
    build.classify("scripts/**", None)
    build.classify("tools/**", None)
    build.classify("README.md", None)
    build.classify("package.json", None)
    build.classify("vite.config.js", None)
    build.classify("index.html", None)
    build.classify("render.yaml", None)
    build.classify(".env.example", None)
    build.classify("icon.ico", None)
    build.classify("game/**.rpy", "archive")
    build.classify("game/**.rpyc", "archive")
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")
    build.classify("game/**.ogg", "archive")
    build.classify("game/**.ttf", "archive")
