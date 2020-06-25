import time
from time import strftime, localtime
import os
import json
import subprocess

def log(input): #function for writing to log file (write append)
    log = open(os.getcwd() + '/log.txt', 'a')
    log.write(strftime("%d %b %Y %H:%M:%S - ", time.localtime()) + input + '\n')
    log.close()

def checkTimeInterval(darkSwitchTime, lightSwitchTime):
    if (int(strftime("%H%M", time.localtime())) < darkSwitchTime and int(strftime("%H%M", time.localtime())) > lightSwitchTime): 
        return True
    return False

def waitUntilChangeTime(darkSwitchTime, lightSwitchTime):
    if (lightSwitchTime % 100 == 0 and darkSwitchTime % 100 == 0): #this only makes sense if there are only hours in the times
        if (int(strftime("%H%M", time.localtime())) % 100 != 0): #wait until time is in the next hour to check so it can check every hour
            log("waiting " + str(60 - (int(strftime("%H%M", time.localtime())) % 100)) + " minutes")
            time.sleep((60 - int(strftime("%H%M", time.localtime())) % 100)*60)
        else:
            log("waiting an hour")
            time.sleep(3600)

    if (lightSwitchTime % 100 != 0 or darkSwitchTime % 100 != 0):
        log("waiting 5 minutes")
        time.sleep(300)

def findThemes(self, path):
    return sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])

def syncTimesWithJSON(self, darkTime, lightTime, settings):
    darkTime.set_text(settings["times"]["lightThemeSwitchTime"])
    lightTime.set_text(settings["times"]["darkThemeSwitchTime"])

def syncThemesWithJSON(self, themes, darkThemeCombo, lightThemeCombo):
    i = 0
    for theme in themes:
        if (theme == self.lightThemeName):
            darkThemeCombo.set_active(i)
        if (theme == self.darkThemeName):
            lightThemeCombo.set_active(i)
        i = i + 1
    
def writeSettings(self, settings):
    with open("settings.json", 'w') as settings_file:
        json.dump(settings, settings_file, indent=4)

def writeDarkТime(self, widget, settings):   
    settings["times"]["darkThemeSwitchTime"] = self.darkChangeTimeSet.get_text()

def writeLightTime(self, widget, settings):
    settings["times"]["lightThemeSwitchTime"] = self.lightChangeTimeSet.get_text()

def writeDarkTheme(self, widget, settings):
    settings["themes"]["darkTheme"] = self.darkCombo.get_active_text()

def writeLightTheme(self, widget, settings):
    settings["themes"]["lightTheme"] = self.lightCombo.get_active_text()

def applyDarkThemeFromComboBox(self, widget):
    subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", self.darkCombo.get_active_text()])

def applyLightThemeFromComboBox(self, widget):
    subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", self.lightCombo.get_active_text()])

def applyDarkThemeFromJSON(self, widget, settings):
    subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", settings["themes"]["darkTheme"]])

def applyLightThemeFromJSON(settings):
    subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", settings["themes"]["lightTheme"]])
