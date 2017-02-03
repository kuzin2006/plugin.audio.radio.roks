# coding=utf-8
import xml.etree.ElementTree as ET

lang = 'en'
low_bitrate = False

tree = ET.parse('../channels.xml')
channels = tree.getroot()

for channel in channels.findall('channel'):
    # check minimum required channel data
    # at least one url and english name
    if channel.find('name').find('en').text != '':
        if channel.find('name').find(lang) is not None:
            name = channel.find('name').find(lang).text
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
        # now add ListItem
        print '%s - %s - %s' % (name, url, icon)
    else: pass
