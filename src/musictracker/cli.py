import os
import urllib.parse
import logging
from argparse import ArgumentParser
from datetime import datetime
from .databasetracker import DatabaseTracker
from .playlistwriter import PlaylistWriter

def log_info(enable, message):
    if enable:
        logging.basicConfig(filename="{}/music-tracker.log".format(os.path.expanduser("~")), encoding='utf-8', level=logging.DEBUG)
        logging.info(message)

def run():
    parser = ArgumentParser(description = 'music-tracker')
    parser.add_argument('database')
    parser.add_argument('--file')
    parser.add_argument('--artist')
    parser.add_argument('--track')
    parser.add_argument('--export-top')
    parser.add_argument('--trending')
    parser.add_argument('--purge')
    parser.add_argument('--verbose')
    parser.add_argument('--skip-tracking')
    parser.add_argument('--recalculate')
    args = parser.parse_args()

    now = datetime.now()
    database = DatabaseTracker(os.path.abspath(args.database))

    for arg, value in sorted(vars(args).items()):
        log_info(args.verbose, "Script Arguments: {} - {}".format(arg, value))

    if args.recalculate:
        print('Recalculating stats...')
        database.recalculate()
        return

    if args.export_top or args.trending:
        if args.trending:
            listname = 'trending-last-{}-days_{}.m3u'.format(args.trending, now.strftime('%Y-%m-%d_%H%M'))
            rows = database.get_trending(args.trending)
        else:
            listname = 'top-{}-songs_{}.m3u'.format(args.export_top, now.strftime('%Y-%m-%d_%H%M'))
            rows = database.get_top(args.export_top)

        writer = PlaylistWriter(listname)
        for row in rows:
            writer.write(row[0], row[1], row[2])
    else:

        media_file = urllib.parse.unquote(args.file)
        log_info(args.verbose, 'file: {}, artist: {}, track: {}'.format(args.file, args.artist, args.track))

        database.add_track(media_file, args.artist, args.track)
        if not args.skip_tracking:
            log_info(args.verbose, 'Counting play for: {}'.format(media_file))
            database.count_play(media_file)

    if args.purge:
        database.purge()

if __name__ == "__main__":
    run()
