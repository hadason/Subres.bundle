import ltrsubs, os, string, hashlib, base64, re, plistlib, unicodedata, codecs

def saveHeb(inputFile):
    result = ltrsubs.writeHebSubs(inputFile)
    file = open(inputFile + '.heb', 'w')
    file.write(str(result))
    file.close()
    
    
