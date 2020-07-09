from redvid import Downloader

reddit = Downloader()
reddit.max_d = 20  # 20 seconds
reddit.url = 'https://www.reddit.com/r/HeavyFuckingWind/comments/hiuauw/its_been_blowing_like_this_all_day_without_stop/'
reddit.download()