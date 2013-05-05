#Subres - Converts hebrew subtitles from ANSI to Unicode and provides RTL support.

import ltrsubs, os, string, hashlib, base64, re, plistlib, unicodedata

def Start():
    Log('Subres - start() called')

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
                subData = ltrsubs.writeHebSubs(sub_path)
                part.subtitles[Locale.Language.Hebrew][sub_path] = Proxy.Media(subData, codec = 'srt', format='srt')
            else:
                Log('Subtitle file doesnt exist')
                Log(dir(Proxy))
        except Exception as e:
            Log('Error: ' + e)

            
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
                    subData = ltrsubs.writeHebSubs(sub_path)
                    part.subtitles[Locale.Language.Hebrew][sub_path] = Proxy.Media(subData, codec = 'srt', format='srt')
                  else:
                    Log('Subtitle file doesnt exist')
                    Log(dir(Proxy))
              except:
                  Log('Error')
