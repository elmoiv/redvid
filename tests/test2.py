from redvid import Downloader

reddit = Downloader()

video_url = 'https://www.reddit.com/r/funny/comments/d4ybit/execute_order_66/?utm_source=share&utm_medium=web2x'

reddit.download(video_url)