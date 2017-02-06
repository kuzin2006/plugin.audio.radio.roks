# coding=utf-8
# Kodi addon for radio Roks online streams
# developed by E.Kuzin

import sys
import urllib
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xml.etree.ElementTree as ET

VERSION = '0.0.2'


# translate internal Kodi addon/resources/ path to OS path
def os_path(filename):
    return xbmc.translatePath('special://home/addons/plugin.audio.radio.roks/resources/' + filename)


def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)


def play_song(url):
    # set the path of the song to a list item
    play_item = xbmcgui.ListItem(path=url)
    # the list item is ready to be played by Kodi
    # TODO: set channel icon in player
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)


# build playlist
# TODO: fanart, descriptions
def parse_channels():
    play_list = []
    tree = ET.parse(os_path('data/channels.xml'))
    channels = tree.getroot()
    for channel in channels.findall('channel'):
        # check minimum required channel data
        # at least one url and english name
        if channel.find('name').find('en').text is not None:
            if channel.find('name').find(lang) is not None:
                name = channel.find('name').find(lang).text.encode('utf-8')
            else:
                name = channel.find('name').find('en').text
            if low_bitrate:
                url = channel.find('url32').text
            else:
                url = channel.find('url').text
            # no url - no display
            if url == '':
                pass
            # icon, default if not configured
            if channel.find('icon') is not None:
                icon = channel.find('icon').text
            else:
                icon = None
            if icon is None:
                icon = 'DefaultMusicCompilations.png'
            else:
                icon = addon_path + '\\resources\\media\\' + channel.find('icon').text
            # now add ListItem
            # create a list item using the song filename for the label
            li = xbmcgui.ListItem(label=name)
            # TODO: setArt, thumbnails etc.
            # set the fanart to the album cover
            # li.setProperty('fanart_image', songs[song]['album_cover'])
            li.setArt({'icon': icon})
            # set the list item to playable
            li.setProperty('IsPlayable', 'true')
            # build the plugin url for Kodi
            # Example: plugin://plugin.audio.example/?url=http%3A%2F%2Fwww.theaudiodb.com%2Ftestfiles%2F01-pablo_perez-your_ad_here.mp3&mode=stream&title=01-pablo_perez-your_ad_here.mp3
            url = build_url({'mode': 'stream', 'url': url, 'title': name})
            # add the current list item to a list
            play_list.append((url, li, False))
            # print '%s - %s - %s' % (name, url, icon)
        else:
            pass
    return play_list


# parse channels info from settings
def build_playlist():
    play_list = parse_channels()
    # add list to Kodi per Martijn
    # http://forum.kodi.tv/showthread.php?tid=209948&pid=2094170#pid2094170
    xbmcplugin.addDirectoryItems(addon_handle, play_list, len(play_list))
    # set the content of the directory
    xbmcplugin.setContent(addon_handle, 'songs')
    xbmcplugin.endOfDirectory(addon_handle)

# get call params
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)

# get settings
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path').decode('utf-8')
low_bitrate = (False, True)[addon.getSetting('low_bitrate') == 'true']
lang = xbmc.getLanguage(xbmc.ISO_639_1)

# initial run
if mode is None:
    # display the list of channels in Kodi
    build_playlist()
# a song from the list has been selected
elif mode[0] == 'stream':
    # pass the url of the song to play_song
    play_song(args['url'][0])

# TODO: language strings
