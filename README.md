Subres (Alpha version)
=======================

LTR subtitles plugin for Plex Media Server 

The purpose of Subres is to support LTR (Left to Right) languages (Hebrew, Arabic, etc.) subtitles with Plex when using a TV (or any other device) that doesn't support LTR by default
This is done by:
  1. Converting the subtitle (SRT) file to Unicode in case it is in ASCII (assuming the TV supports Unicode)
  2. Reversing the characters in the subtitle file since usually when the TV doesn't support LTR the subtitles are rendered reversed on the screen.
  
* This plugin was tested with LG 47LM7600
* Currently only Hebrew is supported

Installation Instructions
-------------------------
1. Copy the plugin (Subres.bundle) to the Plex Plugin directory 
  * Windows 7: `C:\Users\%Username%\AppData\Local\Plex Media Server\Plug-ins`.
  * Make sure to create a folder with the full name of the plugin: Subres.bundle
2. In Plex, under Settings --> Plex Media Server --> Agents, make sure that Subres is checked for each type of show (TV / Movies) and that it is first in the list of preference.
3. Restart Plex Server.

Troubleshooting
---------------
* Subres creates a log file in the following location: 
  * Windows 7: `C:\Users\%Username%\AppData\Local\Plex Media Server\Logs\PMS Plugin Logs`
* In some cases it is required to unmatch the metadata of the show after installing Subres in order for it to work
  * If you try to refresh the show and nothing is showing in the log file, go to the show and click on the "Unmatch" option. (in TV Shows it will be under the show itself and not under the episode)
