# Music Tracker
Python script used to track the times a song has been played.
The script can also generate m3u playlists using the information.

I wrote this script to do some tracking when playing songs on
audacious using the song change plugin.

The script creates a sqlite database used to store the relevant
stats.

# Installation
Download the source code, extract the data, go to the folder and run

`pip install -e .`

# Usage
This is the way I have to set it up on audacious in order to start
tracking the information.

```
// start of song
${HOME}/.local/bin/music-tracker --artist '%a' --track '%T' --file '%f' --skip-tracking true PATH_TO_LIBRARY

// end of song
${HOME}/.local/bin/music-tracker --file '%f' PATH_TO_LIBRARY
```
