from time import strftime, localtime
import time
import subprocess
import os
import json

try:
    with open("settings.json", 'r') as settings_file:
        settings = json.load(settings_file)
except IOError:
    settings = {"themes": {"darkTheme": "Mint-Y-Dark", "lightTheme": "Mint-Y"}, "times": {"darkThemeSwitchTime": "2200", "lightThemeSwitchTime": "0600"}}
    set_write = open("settings.json", "w")
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4)
    set_write.close()

#settings
#military time
lightTime = settings["times"]["lightThemeSwitchTime"]
darkTime = settings["times"]["darkThemeSwitchTime"]
lightTheme = settings["themes"]["lightTheme"]
darkTheme = settings["themes"]["darkTheme"]
currTheme = 2 #0 = light; 1 = dark;

def log(input): #function for writing to log file (write append)
    log = open(os.getcwd() + '/log.txt', 'a')
    log.write(strftime("%d %b %Y %H:%M:%S - ", time.localtime()) + input + '\n')
    log.close()

log("initializing")

#Loop used to constantly check if a proper time has been met with the if statements.
#Wait commands are used so the script isn't checking every possible tick.
while True:
    if (int(strftime("%H%M", time.localtime())) < int(darkTime) and int(strftime("%H%M", time.localtime())) > int(lightTime)): #switches between dark and light theme depending on the time and only if it's inbetween the bounds
        if (currTheme != 0):
            subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", lightTheme])
            log("light theme applied")
            currTheme = 0
    else:
        if (currTheme != 1):
            subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", darkTheme])
            log("dark theme applied")
            currTheme = 1

    if (int(lightTime) % 100 == 0 and int(darkTime) % 100 == 0): #this only makes sense if there are only hours in the times
        if (int(strftime("%H%M", time.localtime())) % 100 != 0): #wait until time is in the next hour to check so it can check every hour
            log("waiting " + str(60 - (int(strftime("%H%M", time.localtime())) % 100)) + " minutes")
            time.sleep((60 - int(strftime("%H%M", time.localtime())) % 100)*60)
            continue
        else:
            log("waiting an hour")
            time.sleep(3600)

    if (lightTime % 100 != 0 or darkTime % 100 != 0):
        log("waiting 5 minutes")
        time.sleep(300)

