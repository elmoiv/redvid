from redvid import Downloader

reddit = Downloader()
reddit.url = 'https://www.reddit.com/r/pythonforengineers/comments/hfmo98/what_kind_of_hawk_is_this/'
reddit.download()