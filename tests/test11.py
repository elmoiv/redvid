from redvid import Downloader

reddit = Downloader()
reddit.url = 'https://www.reddit.com/r/HeavyFuckingWind/comments/hiuauw/its_been_blowing_like_this_all_day_without_stop/'

reddit.check()
if reddit.duration <= 20:
    reddit.download()
else:
    print('Duration > 20 seconds')