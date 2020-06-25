import gi
import subprocess
import os
import json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

try:
    with open("settings.json", 'r') as settings_file:
        settings = json.load(settings_file)
except IOError:
    settings = {"themes": {"darkTheme": "Mint-Y-Dark", "lightTheme": "Mint-Y"}, "times": {"darkThemeSwitchTime": "2200", "lightThemeSwitchTime": "0600"}}
    set_write = open("settings.json", "w")
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4)
    set_write.close()

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        self.lightThemeName = settings["themes"]["lightTheme"]
        self.darkThemeName = settings["themes"]["darkTheme"]

        headerBar = Gtk.HeaderBar()
        headerBar.set_show_close_button(True)
        headerBar.props.title = "Theme Changer"
        self.set_titlebar(headerBar)

        mainFrame = Gtk.Grid()
        self.add(mainFrame)

        gridUpper = Gtk.Grid(margin = 7, column_spacing = 7, row_spacing = 5)
        mainFrame.attach(gridUpper, 0, 0 , 4, 1)

        gridLower = Gtk.Grid()
        mainFrame.attach(gridLower, 0, 1, 4, 1)

        self.set_resizable(False)

        self.bottomButtons = Gtk.ActionBar()
        
        self.exitButton = Gtk.Button(label="Exit")
        self.exitButton.connect("clicked", Gtk.main_quit)

        self.saveButton = Gtk.Button(label="Save")
        self.saveButton.connect("clicked", self.writeSettings)

        self.spaceLabelAB = Gtk.Label(label="                                                            ")

        self.bottomButtons.pack_start(self.saveButton)
        self.bottomButtons.pack_start(self.spaceLabelAB)
        self.bottomButtons.pack_end(self.exitButton)

        gridLower.add(self.bottomButtons)

        #Theme setting buttons
        self.darkButton = Gtk.Button(label="Dark Theme")
        self.darkButton.connect("clicked", self.applyDarkTheme)

        self.lightButton = Gtk.Button(label="Light Theme")
        self.lightButton.connect("clicked", self.applyLightTheme)


        #Dark theme chooser
        self.showDarkChoiceLabel = Gtk.Label(label="Choose a GTK dark theme:")

        self.darkCombo = Gtk.ComboBoxText()
        self.darkCombo.connect("changed",self.writeDarkTheme)

        
        #Light theme chooser
        self.showLightChoiceLabel = Gtk.Label(label="Choose a GTK light theme:")

        self.lightCombo = Gtk.ComboBoxText()
        self.lightCombo.connect("changed",self.writeLightTheme)

        #Time settings
        self.showCautionTimeLabel = Gtk.Label(label="Use military time for the time stamps.")
        self.showCautionTimeConvertionLabel = Gtk.Label(label="18:00 -> 1800 | 06:00 -> 0600")
        
        #Light time settings
        self.showLightTimeChoiceLabel = Gtk.Label(label="Light time:")

        self.lightChangeTimeSet = Gtk.Entry()
        self.lightChangeTimeSet.connect("activate", self.writeLightTime)

        #Dark time settings
        self.showDarkTimeChoiceLabel = Gtk.Label(label="Dark time:")

        self.darkChangeTimeSet = Gtk.Entry()
        self.darkChangeTimeSet.set_max_width_chars(5)
        self.darkChangeTimeSet.connect("activate", self.writeDarkТime)

        self.syncTimesWithJSON(self.lightChangeTimeSet, self.darkChangeTimeSet)

        #Theme search
        self.defaultpath = "/usr/share/themes/"

        themes = self.findThemes(self.defaultpath)

        self.syncThemesWithJSON(themes, self.darkCombo, self.lightCombo)

        gridUpper.attach(self.showCautionTimeLabel, 0, 0, 2, 1)
        gridUpper.attach(self.showCautionTimeConvertionLabel, 0, 1, 2, 1)
        gridUpper.attach(self.showDarkTimeChoiceLabel, 0, 2, 1, 1)
        gridUpper.attach_next_to(self.showLightTimeChoiceLabel, self.showDarkTimeChoiceLabel, 1, 1, 1)
        gridUpper.attach(self.darkChangeTimeSet, 0, 3, 1, 1)
        gridUpper.attach_next_to(self.lightChangeTimeSet, self.darkChangeTimeSet, 1, 1, 1)
        gridUpper.attach(self.showDarkChoiceLabel, 0, 4, 2, 1)
        gridUpper.attach(self.darkCombo, 0, 5, 2, 1)
        gridUpper.attach(self.showLightChoiceLabel, 0, 6, 2, 1)
        gridUpper.attach(self.lightCombo, 0, 7, 2, 1)
        gridUpper.attach(self.darkButton, 0, 8, 1, 1)
        gridUpper.attach_next_to(self.lightButton, self.darkButton, 1, 1, 1)


    
    def findThemes(self, path):
        my_dirs = sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
        
        i = 0
        for theme in my_dirs:
            self.darkCombo.insert(i, str(i), theme)
            self.lightCombo.insert(i, str(i), theme)
            i = i + 1 

        return my_dirs

    def syncTimesWithJSON(self, darkTime, lightTime):
        darkTime.set_text(settings["times"]["lightThemeSwitchTime"])
        lightTime.set_text(settings["times"]["darkThemeSwitchTime"])
    
    def syncThemesWithJSON(self, themes, darkThemeCombo, lightThemeCombo):
        i = 0
        for theme in themes:
            if (theme == self.lightThemeName):
                lightThemeCombo.set_active(i)
            if (theme == self.darkThemeName):
                darkThemeCombo.set_active(i)
            i = i + 1 

    def writeDarkТime(self, widget):   
        settings["times"]["darkThemeSwitchTime"] = self.darkChangeTimeSet.get_text()

    def writeLightTime(self, widget):
        settings["times"]["lightThemeSwitchTime"] = self.lightChangeTimeSet.get_text()

    def writeDarkTheme(self, widget):
        settings["themes"]["darkTheme"] = self.darkCombo.get_active_text()

    def writeLightTheme(self, widget):
        settings["themes"]["lightTheme"] = self.lightCombo.get_active_text()

    def applyDarkTheme(self, widget):
        print("Dark theme applied.")
        subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", self.darkCombo.get_active_text()])

    def applyLightTheme(self, widget):
        print("Light theme applied.")   
        subprocess.call(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", self.lightCombo.get_active_text()])

    def writeSettings(self, widget):
        with open("settings.json", 'w') as settings_file:
            json.dump(settings, settings_file, indent=4)

#print("choosetheme:")
#print(dir(ChooseTheme.props))

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()

#print("win:")
#print(dir(win.props))


#print(dir(win.props))
#win.props.resizable(True)

Gtk.main()