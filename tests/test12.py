from redvid import Downloader

reddit = Downloader()
reddit.auto_max = True

# redvid will find the quality with the size
# that does not exceed max_s (3 MB)
reddit.max_s = 3 * (1 << 20)
reddit.url = 'https://www.reddit.com/r/Unexpected/comments/9n8mmz/_/'
reddit.download()