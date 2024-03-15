import os
import sqlite3
from datetime import datetime

class DatabaseTracker:
    def __init__(self, path):
        self.database_location = "{}/stats.sqlite".format(path)
        if os.path.isfile(path):
            self.database_location = path

        self.db = sqlite3.connect(self.database_location)
        self.create_tables()

    def create_tables(self):
        self.db.execute('CREATE TABLE IF NOT EXISTS tracks (path text, artist text, track text, total integer)')
        self.db.execute('CREATE TABLE IF NOT EXISTS plays (path text, date_played datetime)')

    def recalculate(self):
        rows = self.db.execute('SELECT path, COUNT(*) as total FROM plays GROUP BY "path" ORDER BY total DESC').fetchall()
        for row in rows:
            self.db.execute('UPDATE tracks SET total = ? WHERE path = ?', (row[1], row[0]))

    def add_track(self, path, artist, track):
        path = self.clean_path(path)
        file = self.get_file(path)

        if not file:
            self.db.execute('INSERT INTO tracks (path, artist, track, total) VALUES (?, ?, ?, ?)', (path, artist, track, 0))
            self.db.commit()

    def count_play(self, path):
        path = self.clean_path(path)
        self.db.execute('UPDATE tracks SET total = total + 1 WHERE path = ?', (path,))

        now = datetime.now()
        self.db.execute('INSERT INTO plays (path, date_played) VALUES (?, ?)', (path, now.strftime("%Y-%m-%d %H:%M:%S")))
        self.db.commit()

    def get_trending(self, days):
        return self.db.execute('SELECT path, COUNT(*) as total, date_played FROM plays WHERE date_played >= DATETIME("now", "-' + days + ' days", "localtime") GROUP BY "path" ORDER BY total DESC LIMIT 100').fetchall()

    def get_top(self, total):
        return self.db.execute('SELECT path, artist, track FROM tracks ORDER BY total DESC LIMIT ?', (total,)).fetchall()

    def get_file(self, path):
        rows = self.db.execute('SELECT path, artist, track, total FROM tracks WHERE path = ?', (path, )).fetchall()
        return rows if len(rows) > 0 else None

    def clean_path(self, path):
        return path.replace('file://', '')

    def delete_file(self, path):
        self.db.execute('DELETE FROM tracks WHERE path = ?', (path, ))
        self.db.execute('DELETE FROM plays WHERE path = ?', (path, ))

    def purge(self):
        rows = self.db.execute('SELECT path, artist, track, total FROM tracks').fetchall()
        for row in rows:
            if not os.path.isfile(row[0]):
                self.delete_file(row[0])
