#Subres - Converts hebrew subtitles from ANSI to Unicode and provides RTL support.

import ltrsubs, os, string, hashlib, base64, re, plistlib, unicodedata

def Start():
    Log('Subres - start() called')

def updatePartsSub(parts):
    for part in parts:
        try:
            file_path = os.path.splitext(part.file)[0]
            sub_path = file_path + '.srt'
            if (False == os.path.exists(sub_path)):
                Log('No subtitle file found')
                continue
            Log('Found subtitle file: ' + sub_path)
            encoding = ltrsubs.get_hebrew_encoding(sub_path)
            if (None == encoding):
                Log('Subtitle file does not seem to be in hebrew, skipping file.')
                continue
            Log('Subtitle seems to be in hebrew (' + encoding + '), processing subtitle file.')
            subData = ltrsubs.writeHebSubs(sub_path, encoding)
            processedSub = Proxy.Media(subData, codec = 'srt', format='srt')
            part.subtitles[Locale.Language.Hebrew][sub_path] = processedSub
        except Exception as e:
            Log('Error: ' + str(e))
    
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
      updatePartsSub(i.parts)   
            
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
            updatePartsSub(i.parts)