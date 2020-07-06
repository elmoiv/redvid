# redvid
[![HitCount](http://hits.dwyl.io/elmoiv/redvid.svg)](http://hits.dwyl.io/elmoiv/redvid)
[![Build Status](https://api.travis-ci.org/elmoiv/redvid.svg?branch=master)](https://travis-ci.org/elmoiv/redvid)
[![Python version](https://img.shields.io/badge/python-3.x-brightgreen.svg)](https://pypi.org/project/redvid/)

### Smart downloader for Reddit hosted videos

## Features
* Download local hosted videos with audio.
* Requires only `requests` library.
* Ability to decide quality.
* Bypass bot detection.

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

reddit = Downloader(max_q=True)
reddit.url = 'https://v.redd.it/c8oic7ppc2751'
reddit.download()
```
or
```python
from redvid import Downloader

Downloader(url='https://v.redd.it/c8oic7ppc2751', max_q=True).download()
```

## Tests
Here are a few sample tests:

  * [Video only](https://github.com/elmoiv/redvid/tree/master/tests/test1.py)
  * [Video with audio](https://github.com/elmoiv/redvid/tree/master/tests/test2.py)
  * [Choose PATH](https://github.com/elmoiv/redvid/tree/master/tests/test3.py)
  * [Auto-detect maximum quality](https://github.com/elmoiv/redvid/tree/master/tests/test4.py)
  * [Auto-detect minimum quality](https://github.com/elmoiv/redvid/tree/master/tests/test5.py)
  * [Skip file check and overwrite](https://github.com/elmoiv/redvid/tree/master/tests/test6.py)

## Installing FFmpeg
### Windows: 

https://m.wikihow.com/Install-FFmpeg-on-Windows

(*You may need to restart your pc after applying these steps*)

### Linux: 

`sudo apt install ffmpeg`

### Mac OS:

* install [Homebrew](https://brew.sh/):

  `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
  
* Then:

  `$ brew install ffmpeg`

## Changelog
### v1.0.8:
  * Fixed a bug with quality fetching.
### v1.0.7:
  * `download()` will return file path again.
### v1.0.6:
  * Can now download urls with **v.reddit.it** fromat.
  * PATH can be choosed instead of current dir.
  * Max/Min quality can be automatically set to skip quality query.
  * Added ffmpeg encoding to videos with no sound to be uploadable on some platforms.
  * Adjusted printed text and progress bars.

## Contributing
Please contribute! If you want to fix a bug, suggest improvements, or add new features to the project, just [open an issue](https://github.com/elmoiv/redvid/issues) or send me a pull request.
