# -*- coding: iso-8859-8 -*-

#ltrsubs - Converts hebrew subtitles from ANSI to Unicode and provides RTL support.

import os, string, hashlib, base64, re, plistlib, unicodedata, codecs

class LineStatus:
    LINE_NUMBER = 1
    TIME = 2
    SUBTITLES = 3

def reverseGroup(match, groupName):
        line = ''
        for group in match.groups():
            if (group is None):
                continue
            if (group == match.group(groupName)):
                line += group[::-1]
            else:
                line += group
        return line

def writeHebSubs(inputFile):
    input = os.fdopen(os.open(inputFile, os.O_RDONLY))
    lines = input.readlines()
    state = LineStatus.LINE_NUMBER
    result = ''
    for line in lines:
        if (state == LineStatus.LINE_NUMBER):
            result += line
            state = LineStatus.TIME
            continue
        if (state == LineStatus.TIME):
            result += line
            state = LineStatus.SUBTITLES
            continue
        if (line == '\n'):
            state = LineStatus.LINE_NUMBER
        line = re.sub('(<[a-zA-Z]>)*([\.\,\"\-:\?\'!\(\)a-zA-Z]*)(?P<subs>.*[א-ת]+.*?)([\.\,\"\-:\?\'!\(\)a-zA-Z]*)(</[a-zA-Z]>)*$', lambda match: reverseGroup(match, 'subs'), line)
        line = re.sub(r'([א-ת]+.*)(?P<nums>[0-9]+)', lambda match: reverseGroup(match, 'nums'), line)
        line = re.sub(r'(?P<nums>[0-9]+)(.*[א-ת])+', lambda match: reverseGroup(match, 'nums'), line)
        result += line
    input.close()
    return codecs.BOM_UTF8 + result.decode('iso-8859-8').encode('utf-8')
    
def is_hebrew_encoding(inputFile):
    with os.fdopen(os.open(inputFile, os.O_RDONLY)) as input:
        lines = input.readlines()
        for line in lines:
            try:
                #bytes(line, encoding='iso-8859-8')
                line.decode('iso-8859-8')
            #except UnicodeEncodeError as e:
            except UnicodeDecodeError as e:
                return False
        return True