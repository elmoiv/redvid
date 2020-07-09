from redvid import Downloader

reddit = Downloader()
reddit.max_s = 5 * (1 << 20)  # 5 MB
reddit.url = 'https://www.reddit.com/r/HeavyFuckingWind/comments/hiuauw/its_been_blowing_like_this_all_day_without_stop/'
reddit.download()