from .redvid import Downloader
from . import __version__
import argparse

def run():
    parser = argparse.ArgumentParser(description='Argument parser for redvid module')
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Required URL
    required.add_argument(
        '-u',
        '--url',
        type=str,
        help='Post URL for Reddit hosted video'
    )

    # Optional Redvid properties
    optional.add_argument(
        '-p',
        '--path',
        type=str,
        default='',
        help='Custom path for downloaded videos'
    )
    optional.add_argument(
        '-fn',
        '--filename',
        type=str,
        help='Set custom filename for downloaded video'
    )
    optional.add_argument(
        '-o',
        '--overwrite',
        action='store_true',
        help='Overwrite existing videos and ignore exception'
    )
    optional.add_argument(
        '-mxq',
        '--maxquality',
        action='store_true',
        help='Auto select maximum quality'
    )
    optional.add_argument(
        '-mnq',
        '--minquality',
        action='store_true',
        help='Auto select minimum quality'
    )
    optional.add_argument(
        '-mxd',
        '--maxduration',
        type=int,
        default=1e1000,
        help='Ignore videos that exceed this duration (in seconds)'
    )
    optional.add_argument(
        '-mxs',
        '--maxsize',
        type=int,
        default=1e1000,
        help='Ignore videos that exceed this size (in bytes)'
    )
    optional.add_argument(
        '-am',
        '--automax',
        action='store_true',
        help='Automatically download video with maximum size (Helps for old reddit videos with unknown qualities)'
    )
    optional.add_argument(
        '-ad',
        '--autodir',
        action='store_true',
        help='Automatically create path if correctly typed and does not exist'
    )
    optional.add_argument(
        '-px',
        '--proxies',
        type=dict,
        default={},
        help='Download videos through proxies for blocked regions'
    )
    optional.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='Show redvid version'
    )
    optional.add_argument(
        '-nc',
        '--noclean',
        action='store_true',
        help='Don\'t clean temp folder after download is done'
    )

    args = parser.parse_args()
    
    if args.version:
        print('redvid ' + __version__)
    elif not args.url:
        print('Error: The following arguments are required: -u/--url')
    else:
        # Link arguments with Redvid
        reddit = Downloader()

        reddit.url = args.url
        reddit.path = args.path
        reddit.overwrite = args.overwrite
        reddit.max = args.maxquality
        reddit.min = args.minquality
        reddit.max_d = args.maxduration
        reddit.max_s = args.maxsize
        reddit.auto_max = args.automax
        reddit.auto_dir = args.autodir
        reddit.proxies = args.proxies
        reddit.filename = args.filename

        reddit.download()
        if not args.noclean:
            reddit.clean_temp()

if __name__ == '__main__':
    run()
    