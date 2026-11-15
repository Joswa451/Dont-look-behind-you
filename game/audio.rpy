init -100 python:
    if not renpy.music.channel_defined("charvoice"):
        renpy.music.register_channel("charvoice", mixer="voice", loop=False)
    if not renpy.music.channel_defined("narrvoice"):
        renpy.music.register_channel("narrvoice", mixer="voice", loop=False)
    if not renpy.music.channel_defined("voicemail"):
        renpy.music.register_channel("voicemail", mixer="voice", loop=False)

init python:
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)
    renpy.music.register_channel("pulse", mixer="sfx", loop=True)

define audio.menu = "audio/music/music_menu.ogg"
define audio.ch1 = "audio/music/music_ch1.ogg"
define audio.ch2 = "audio/music/music_ch2.ogg"
define audio.ch3 = "audio/music/music_ch3.ogg"
define audio.ch4 = "audio/music/music_ch4.ogg"
define audio.ch5 = "audio/music/music_ch5.ogg"
define audio.ch6 = "audio/music/music_ch6.ogg"
define audio.ch7 = "audio/music/music_ch7.ogg"
define audio.entity = "audio/music/music_entity.ogg"
define audio.ending_truth = "audio/music/music_ending_truth.ogg"
define audio.ending_alone = "audio/music/music_ending_alone.ogg"
define audio.ending_call = "audio/music/music_ending_call.ogg"
define audio.ending_newgame = "audio/music/music_ending_newgame.ogg"

define audio.rain = "audio/sfx/rain_loop.ogg"
define audio.thunder = "audio/sfx/thunder.ogg"
define audio.footsteps = "audio/sfx/footsteps.ogg"
define audio.door_creak = "audio/sfx/door_creak.ogg"
define audio.door_slam = "audio/sfx/door_slam.ogg"
define audio.phone_ring = "audio/sfx/phone_ring.ogg"
define audio.phone_vibrate = "audio/sfx/phone_vibrate.ogg"
define audio.whisper = "audio/sfx/whisper.ogg"
define audio.breathing = "audio/sfx/breathing.ogg"
define audio.heartbeat = "audio/sfx/heartbeat.ogg"
define audio.glitch = "audio/sfx/glitch.ogg"
define audio.jumpscare = "audio/sfx/jumpscare.ogg"
define audio.static = "audio/sfx/static.ogg"
define audio.flicker = "audio/sfx/light_flicker.ogg"
define audio.hover = "audio/sfx/ui_hover.ogg"
define audio.click = "audio/sfx/ui_click.ogg"
define audio.notify = "audio/sfx/phone_notify.ogg"
define audio.tape = "audio/sfx/tape.ogg"
define audio.music_box = "audio/sfx/music_box.ogg"
define audio.clock = "audio/sfx/clock_tick.ogg"
define audio.drip = "audio/sfx/water_drip.ogg"
define audio.knife = "audio/sfx/knife.ogg"
define audio.paper = "audio/sfx/paper.ogg"
define audio.wind = "audio/sfx/wind.ogg"
define audio.unlock = "audio/sfx/door_unlock.ogg"
define audio.drawer = "audio/sfx/drawer.ogg"
define audio.scream = "audio/sfx/scream.ogg"

define audio.voicemail_unknown = "audio/voice/voicemail_unknown.ogg"
define audio.voicemail_mom = "audio/voice/voicemail_mom.ogg"
define audio.voicemail_maya = "audio/voice/voicemail_maya.ogg"

init python:
    def silence_scene(fade=1.5):
        renpy.music.stop(channel="music", fadeout=fade)
        renpy.music.stop(channel="ambient", fadeout=fade)
        renpy.music.stop(channel="pulse", fadeout=fade)
        renpy.sound.stop(channel="charvoice", fadeout=fade)
        renpy.sound.stop(channel="narrvoice", fadeout=fade)
        renpy.sound.stop(channel="voicemail", fadeout=fade)
