#Subres - Converts hebrew subtitles from ANSI to Unicode and provides RTL support.

import os, string, hashlib, base64, re, plistlib, unicodedata, codecs

def Start():
    Log('Subres - start() called')

def reverseHeb(match):
        line = ''
        for group in match.groups():
            if (group is None):
                continue
            if (group == match.group('subs')):
                line += group[::-1]
            else:
                line += group
        return line

def writeHebSubs(inputFile):
    input = os.fdopen(os.open(inputFile, os.O_RDONLY))
    lineRegex = re.compile(r'(^[0-9].*[0-9]*$)', re.MULTILINE)
    lines = input.readlines()
    result = ''
    for line in lines:
        if (lineRegex.match(line)):
            result += line
        else:
            fix = re.sub('(<[a-zA-Z]>)*([\.\,\"\-:\?\'!\(\)a-zA-Z]*)(?P<subs>.*?)([\.\,\"\-:\?\'!\(\)a-zA-Z]*)(</[a-zA-Z]>)*$', lambda match: reverseHeb(match), line)
            re.sub('([0-9]+)', lambda match: match.group(0)[::-1], fix)
            result += fix
    input.close()
    return codecs.BOM_UTF8 + result.decode('iso-8859-8').encode('utf-8')
    #return result
    

class SubresAgentMovies(Agent.Movies):
  name = 'Subres_Movies'
  languages = [Locale.Language.English]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.imdb', 'com.plexapp.agents.none']
  
  def search(self, results, media, lang):
    Log('Subres (Movies)- search() called');
    results.Append(MetadataSearchResult(id = 'null', score = 100));
    
  def update(self, metadata, media, lang):
    Log('Subres (Movies) - update() called')
    Log('Metadata.title: %s, media.title: %s', metadata.title, media.title)
    for i in media.items:
      for part in i.parts:
        try:
            file_path = os.path.splitext(part.file)[0]
            Log('filename without ext: %s', file_path)
            sub_path = file_path + '.srt'
            if (os.path.exists(sub_path) == True):
                Log('Subtitle file exists')
                subData = writeHebSubs(sub_path)
                part.subtitles[Locale.Language.Hebrew][sub_path] = Proxy.Media(subData, codec = 'srt', format='srt')
            else:
                Log('Subtitle file doesnt exist')
                Log(dir(Proxy))
        except:
            Log('Error')

class SubresSubtitlesAgentTV(Agent.TV_Shows):
  name = 'Subres_TV'
  languages = [Locale.Language.English]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.thetvdb', 'com.plexapp.agents.none']
  Log('Subres (TV) - initializing agent')

  def search(self, results, media, lang):
    Log('Subres (TV) - search() called')
    results.Append(MetadataSearchResult(id = 'null', score = 100))

  def update(self, metadata, media, lang):
    Log('Subres (TsV) - update() called')
    Log('Metadata.title: %s, media.title: %s', metadata.title, media.title)
    # Look for subtitles for each episode.
    for s in media.seasons:
      # If we've got a date based season, ignore it for now, otherwise it'll collide with S/E folders/XML and PMS
      # prefers date-based (why?)
      for e in media.seasons[s].episodes:
        for i in media.seasons[s].episodes[e].items:
            # Look for subtitles.
            for part in i.parts:
              try:
                  file_path = os.path.splitext(part.file)[0]
                  Log('filename without ext: %s', file_path)
                  sub_path = file_path + '.srt'
                  if (os.path.exists(sub_path) == True):
                    Log('Subtitle file exists')
                    subData = writeHebSubs(sub_path)
                    part.subtitles[Locale.Language.Hebrew][sub_path] = Proxy.Media(subData, codec = 'srt', format='srt')
                  else:
                    Log('Subtitle file doesnt exist')
                    Log(dir(Proxy))
              except:
                  Log('Error')
