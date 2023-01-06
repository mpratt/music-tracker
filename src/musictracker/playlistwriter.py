import os

class PlaylistWriter:
    def __init__(self, listname):
        self.playlist = open(listname, 'a')
        if not os.path.isfile(listname):
            self.playlist.write("#EXTM3U\n")

    def __del__(self):
        self.playlist.close()

    def write(self, path, artist, track):
        if os.path.isfile(path):
            self.playlist.write(u"#EXTINF: 0, {} - {} \n".format(artist, track))
            self.playlist.write(path + "\n")
