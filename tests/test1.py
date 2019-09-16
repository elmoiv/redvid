from redvid import Downloader

reddit = Downloader()

video_url = 'https://www.reddit.com/r/funny/comments/d502c4/the_power_of_static_electricity/?utm_source=share&utm_medium=web2x'

reddit.download(video_url)