from redvid import Downloader
import argparse

parser = argparse.ArgumentParser(description='Argument parser for redvid module')
parser._action_groups.pop()

required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')

# Required URL
required.add_argument('-u', '--url', type=str, help='Post URL for Reddit hosted video', required=True)

# Optional Redvid properties
optional.add_argument('-p',     '--path',           help='Custom path for downloaded videos', type=str, default='')
optional.add_argument('-o',     '--overwrite',      help='Overwrite existing videos and ignore exception', action='store_true')
optional.add_argument('-mxq',   '--maxquality',     help='Auto select maximum quality', action='store_true')
optional.add_argument('-mnq',   '--minquality',     help='Auto select minimum quality', action='store_true')
optional.add_argument('-mxd',   '--maxduration',    help='Ignore videos that exceed this duration (in seconds)', type=int, default=1e1000)
optional.add_argument('-mxs',   '--maxsize',        help='Ignore videos that exceed this size (in bytes)', type=int, default=1e1000)
optional.add_argument('-am',    '--automax',        help='Automatically download video with maximum size (Helps for old reddit videos with unknown qualities)', action='store_true')
optional.add_argument('-ad',    '--autodir',        help='Automatically create path if correctly typed and does not exist', action='store_true')
optional.add_argument('-px',    '--proxies',        help='Download videos through proxies for blocked regions', type=dict, default={})

args = parser.parse_args()

# Link arguments with Redvid
reddit = Downloader()

reddit.url = args.url
reddit.path = args.path
reddit.overwrite = args.overwrite
reddit.max_q = args.maxquality
reddit.min_q = args.minquality
reddit.max_d = args.maxduration
reddit.max_s = args.maxsize
reddit.auto_max = args.automax
reddit.proxies = args.proxies

reddit.download()