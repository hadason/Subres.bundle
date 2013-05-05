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
    lineRegex = re.compile(r'(^[0-9].*[0-9]*$)', re.MULTILINE)
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
        fix = re.sub(r'(<[a-zA-Z]>)*([\.\,\"\-:\?\'!\(\)a-zA-Z]*)(?P<subs>.*[א-ת]+.*?)([\.\,\"\-:\?\'!\(\)a-zA-Z]*)(</[a-zA-Z]>)*$', lambda match: reverseGroup(match, 'subs'), line)
        fix = re.sub(r'([א-ת]+.*)(?P<nums>[0-9]+)', lambda match: reverseGroup(match, 'nums'), fix)
        fix = re.sub(r'(?P<nums>[0-9]+)(.*[א-ת])+', lambda match: reverseGroup(match, 'nums'), fix)
        result += fix
    input.close()
    #codecs.BOM_UTF8 + codec.decode(result, 'iso-8859-8').encode('utf-8')
    #return codecs.BOM_UTF8 + result.encode('utf-8')
    return result

def saveHeb(inputFile):
    result = writeHebSubs(inputFile)
    file = open(inputFile + '.heb', 'w')
    file.write(str(result))
    file.close()
    
    
