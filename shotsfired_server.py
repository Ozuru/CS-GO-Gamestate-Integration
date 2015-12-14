import json, os.path, autoit, shutil
from flask import Flask, request

HOTKEY_STEAM = "capslock" #the Steam version of your keybind, https://developer.valvesoftware.com/wiki/Bind
HOTKEY_AUTOIT = "{CAPSLOCK}" #the AutoIt version of your keybind, check https://www.autoitscript.com/autoit3/docs/appendix/SendKeys.htm
CSGO_DIR = "P:\Program Files\Steam\steamapps\common\Counter-Strike Global Offensive" #path to your game, no trailing slash
SOUND_NAME = "sound.wav" #sound you want played
REMAKE_CONFIG = True #set this to true if you change any of the keybinds
''' Configuration is over, everything down shouldn't be touched unless you know what you're doing. '''

CSGO_CFG_FILE = CSGO_DIR + "\csgo\cfg\shotsfired_gameint.cfg" #constant for path to our custom cfg file

app = Flask(__name__)

# generate the config file
if not os.path.isfile(CSGO_CFG_FILE) or REMAKE_CONFIG:
        cfgfile = open(CSGO_CFG_FILE, 'w')
        cfgfile.write('alias audio_file_on "voice_loopback 1;voice_inputfromfile 1;+voicerecord;alias audio_file_toggle audio_file_off"\n')
        cfgfile.write('alias audio_file_off "voice_loopback 0;voice_inputfromfile 0;-voicerecord;alias audio_file_toggle audio_file_on"\n')
        cfgfile.write('alias audio_file_toggle "audio_file_on"\n')
        cfgfile.write('bind ' + HOTKEY_STEAM + " audio_file_toggle")
        cfgfile.flush()
        cfgfile.close()
        print "Created CFG file!"

# delete the voice input file if it exists
try:
    os.remove(CSGO_DIR + "\\voice_input.wav")
except:
    pass

# copy and rename the sound to the CS:GO directory
shutil.copy(SOUND_NAME, CSGO_DIR)
os.rename(CSGO_DIR + "\\" + SOUND_NAME, CSGO_DIR + "\\voice_input.wav")

if os.path.isfile(CSGO_DIR + "\\voice_input.wav"):
    print "Copied file successfully!"
else:
    print "Error copying file -- check permissions."

# main() handles interfacing with the CS:GO client's gamestate integration
@app.route("/", methods=["POST"])
def main():
    data = request.data.decode('UTF-8')

    json_data = json.loads(data) # get the json from the client

    # loop five times to check all the weapon slots to detect a change
    for i in range(0,5):
        try:
            weapon_clip = json_data['player']['weapons']['weapon_'+str(i)]['ammo_clip']
            previous_weapon_clip = json_data['previously']['player']['weapons']['weapon_'+str(i)]['ammo_clip']
            if weapon_clip < previous_weapon_clip: #if the weapon was fired
                print('Shot detected!')
                autoit.win_activate('Counter-Strike: Global Offensive') # prepare by forcing us to focus on CS:GO (so the keybinds trigger)
                autoit.send(HOTKEY_AUTOIT) # send hotkey
        except:
            pass

    return 'hello world'

if __name__ == "__main__":
    app.run(port=6969)