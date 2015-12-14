# ShooterSpam 0.1 by [Ozuru](http://www.malware.cat/)

## What is ShooterSpam?

ShooterSpam is a project that interfaces with CS:GO's gamestate API. Every time the user fires a bullet, they play a sound through their microphone to all the other players in the game.

## Quickstart Guide

1. Download and extract the files somewhere. It doesn't matter where.
2. Copy "gamestate_integration.cfg" to your CS:GO's cfg directory. This is normally in:
> Program Files/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/cfg

3. Run shotsfired_server.py through an elevated terminal. If you're on Windows, this probably looks something like:
> python shotsfired_server.py

4. In CS:GO, open the developer console (by pressing `) and type "exec shotsfired_gameint" (without the quotes). Hit enter. You'll be all ready then.
5. Congratulations. Go annoy everyone in your match!

## Configuring

```python
HOTKEY_STEAM = "capslock"
HOTKEY_AUTOIT = "{CAPSLOCK}"
CSGO_DIR = "P:\Program Files\Steam\steamapps\common\Counter-Strike Global Offensive"
SOUND_NAME = "sound.wav"
REMAKE_CONFIG = True
```

###### HOTKEY_STEAM
This value is how Steam refers to that key. To view a list of all possible keys you can use, check out [this link from Valve](https://developer.valvesoftware.com/wiki/Bind).
###### HOTKEY_AUTOIT
This value is how Autoit refers to that key. Scroll down towards the bottom of [this page](https://www.autoitscript.com/autoit3/docs/appendix/SendKeys.htm) for a listing of keys.
###### CSGO_DIR
This variable is the path to your CS:GO directory. Yours will probably be on the C drive and will normally be something like:
> C:/Program Files/Steam/steamapps/common/Counter-Strike Global Offensive

Make sure that the last character is not a slash (no trailing slashes!). For example, if I did
```python
CSGO_DIR = "P:\Program Files\Steam\steamapps\common\Counter-Strike Global Offensive\"
```
instead of
```python
CSGO_DIR = "P:\Program Files\Steam\steamapps\common\Counter-Strike Global Offensive"
```
the script would break and give you an error. Don't do that!
###### SOUND_NAME
This is the name of the file that your sound is. Make sure that you are using a .WAV file, as it is the only extension that Steam will like.
###### REMAKE_CONFIG
If this boolean is set to true, it will automatically delete and create a new configuration file every time it runs. Set this flag to true if you've changed any of the hotkeys and want it to regenerate a new configuration file.
It's generally safe to leave this on all the time, I wouldn't set this to false. If you do change it, remember that Python is case-sensitive with it's booleans and the first letter is always capital.

## I'm a nerd. How does this work?
Yay, someone finally asked!

CS:GO's gamestate integration POSTs information to a webserver specified in a configuration file (gamestate_integration.cfg). Through Flask, we setup a local webserver (on port 6969) and have the configuration file POST its information there. Whenever we detect a change in the ammo clip for any of the weapons, we know that it's our time to transmit a sound.

Transmitting the sound through the microphone is where it started to get weird. Without writing a driver in C/C++, I couldn't really do much until I found out about voice_input. voice_input is a flag in CS:GO that causes the microphone to switch its source to a file named voice_input.wav in the root CS:GO directory.

If you set voice_input to 1 and execute +voicerecord, you play that file. What the script does is simply set a hotkey up so that when you press a key, it executes those commands (and shuts off). The script then presses those hotkeys for you once it determines a bullet has been fired. This activates the CS:GO keybind, which opens and plays the voice_input.wav file in the root CS:GO directory. When it finishes, it stops.

## Credits

I worked on CS:GO's gamestate integration with [BumbleMan](http://www.github.com/BumbleMan), check him out!
