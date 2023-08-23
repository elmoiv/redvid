from redvid import Downloader


dl = Downloader()

dl.url = "https://v.redd.it/5t4rwrgudvjb1"

# Setting the filename
dl.filename = "test"


dl.download()