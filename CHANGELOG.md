### v2.0.3 - 27-11-2023:
  * [#35](https://github.com/elmoiv/redvid/pull/35) Fixed random audio track given to videos with no audio track.
  * Temp cleaning is now true by default. Use `-nc` or `--noclean` to save temp files.
### v2.0.2 - 30-08-2023:
  * [#34](https://github.com/elmoiv/redvid/pull/34) Added option to set custom filename.
### v2.0.1 - 11-08-2023:
  * [#33](https://github.com/elmoiv/redvid/pull/33) Fixed mixing up .vtt files with videos.
### v2.0.0 - 07-08-2023:
  * [#32](https://github.com/elmoiv/redvid/issues/32) Fixed fetching audio with the new Reddit architecture.
### v1.2.0 - 09-03-2022:
  * [#24](https://github.com/elmoiv/redvid/pull/24) Added support for parallel instances saving to same directory.
  * You can now call `redvid` directly from terminal with no need for `credvid.py`.
  * Added custom temp clean method.
### v1.1.3 - 30-03-2021:
  * [#20](https://github.com/elmoiv/redvid/issues/20) Added a feature to create a folder in case it does not exist.
### v1.1.2 - 05-01-2021:
  * [#18](https://github.com/elmoiv/redvid/issues/18) Fixed bug when handling path that caused recursive directories.
### v1.1.1 - 05-10-2020:
  * [#15](https://github.com/elmoiv/redvid/issues/15) Fixed bug when fetching reddit videos with expiry date.
### v1.1.0 - 25-08-2020:
  * [#11](https://github.com/elmoiv/redvid/issues/11) redvid can now decide best quality according to given size.
  * Added support for old reddit videos.
  * Fixed bug where video qualities list can't be parsed.
### v1.0.9 - 09-07-2020:
  * [#8](https://github.com/elmoiv/redvid/issues/8) Added the ability to disable logging.
  * Maximum video size can be set.
  * [#9](https://github.com/elmoiv/redvid/issues/9) Maximum video duration can be set.
### v1.0.8 - 01-07-2020:
  * [#7](https://github.com/elmoiv/redvid/issues/7) Fixed a bug with quality fetching.
### v1.0.7 - 01-07-2020:
  * `download()` will return file path again.
### v1.0.6 - 01-07-2020:
  * [#5](https://github.com/elmoiv/redvid/issues/5) Can now download urls with **v.reddit.it** fromat.
  * [#4](https://github.com/elmoiv/redvid/issues/4) PATH can be choosed instead of current dir.
  * [#3](https://github.com/elmoiv/redvid/issues/3) Max/Min quality can be automatically set to skip quality query.
  * Added ffmpeg encoding to videos with no sound to be uploadable on some platforms.
  * Adjusted printed text and progress bars.
### v1.0.5 - 23-4-2020:
  * First Release
