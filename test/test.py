# coding=utf-8
import xml.etree.ElementTree as ET
import random

lang = 'en'
low_bitrate = False

tree = ET.parse('../resources/data/channels.xml')
channels = tree.getroot()

#print len(channels.findall('channel'))
print channels.findall('channel')[random.randint(0, len(channels.findall('channel'))-1)].text

for channel in channels.findall('channel'):
    fanarts = channel.findall('fanart')
    if len(fanarts) > 0:
        print fanarts[random.randint(0, len(fanarts)-1)].text
    else:
        print 'no fanart'