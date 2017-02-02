import xbmcaddon
import xbmcgui

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

line1 = "Hello World!"
line2 = "radioroks plugin"
line3 = "OMFG"

xbmcgui.Dialog().ok(addonname, line1, line2, line3)