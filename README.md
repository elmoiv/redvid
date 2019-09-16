# redvid
[![Build Status](https://api.travis-ci.org/elmoiv/redvid.svg?branch=master)](https://travis-ci.org/elmoiv/redvid)
[![Python version](https://img.shields.io/badge/python-3.x-brightgreen.svg)](https://pypi.org/project/goco/)

### Smart downloader for Reddit hosted videos

## Features
* #### Download local hosted videos with audio.
* #### Bypass bot detection.
* #### Ability to decide quality.
* #### Requires only `requests` library.

## Installation
`redvid` requires Python 3.

Use `pip` to install the package from PyPI:

```bash
pip install redvid
```

Or, install the latest version of the package from GitHub:

```bash
pip install git+https://github.com/elmoiv/redvid.git
```

## Usage
Using *redvid* to download a video:

```python
from redvid import Downloader

reddit = Downloader()

video_url = input('Enter video url: ')

reddit.download(video_url)
```

## Tests
Here are a few sample tests:

* [Video only](https://github.com/elmoiv/redvid/tree/master/tests/test1.py)
* [Video with audio](https://github.com/elmoiv/redvid/tree/master/tests/test2.py)

## Installing FFmpeg
### Windows: 

https://m.wikihow.com/Install-FFmpeg-on-Windows

(*restart your pc after applying these steps*)

### Linux: 

`sudo apt install ffmpeg`

### Mac OS:

* install [Homebrew](https://brew.sh/):

  `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
  
* Then:

  `$ brew install ffmpeg`

## TODO
* Rename downloaded videos to OP name.
* Download gifs and pictures.
* ...

## Contributing
Please contribute! If you want to fix a bug, suggest improvements, or add new features to the project, just [open an issue](https://github.com/elmoiv/redvid/issues) or send me a pull request.
