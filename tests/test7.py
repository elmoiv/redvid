from redvid import Downloader

reddit = Downloader()
reddit.log = False
reddit.url = 'https://www.reddit.com/r/HeavyFuckingWind/comments/hiuauw/its_been_blowing_like_this_all_day_without_stop/'
reddit.download()