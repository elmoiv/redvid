from .requestmaker import Requester
from .tools import *
__import__('warnings').filterwarnings("ignore")

class Downloader(Requester):
    """
    Smart downloader for Reddit hosted videos

    Attributes:
        url (str): Reddit post url that contains video.
        path (str): Location where videos will be saved.
        max_q (bool): Get video with maximum quality.
        min_q (bool): Get video with minimum quality.
        max_d (int): Allow only when duration is <= max_d.
        max_s (int): Allow only when size is <= max_s.
        overwrite (bool): To skip file checking and download.
        log (bool): Turn logging on or off.
        proxies (dict): Use proxy while connecting to Reddit.
    """
    def __init__(
                self,
                url='',
                path='',
                max_q=False,
                min_q=False,
                max_d=1e1000,
                max_s=1e1000,
                log=True,
                proxies={}
                ):
        self.path, self.url, self.proxies = path, url, proxies
        self.max, self.min, self.log = max_q, min_q, log
        self.max_d, self.max_s = max_d, max_s
        self.page = None
        self.overwrite = False
        self.ischeck = False
        self.video, self.audio, self.file_name = '', '', ''
        self.duration, self.size = 0, 0
        
    def setup(self):
        """
        Checks PATH and URL for any errors
        """
        if not self.log:
            if not self.max and not self.min:
                self.max = True

        self.path = checkPath(self.path)
        Clean(self.path)
        os.chdir(self.path)
        
        os.makedirs('temp', exist_ok=True)
        os.chdir('temp')
        
        # Allow v.redd.it url formats
        if 'v.redd.it' in self.url:
            self.url = self.get(
                                self.url,
                                _proxies=self.proxies
                                ).url
        
        self.page = self.get(
                            toJsonUrl(self.url),
                            _proxies=self.proxies
                            )
        
        if self.page.status_code is 200:
            return True
        
        raise BaseException('Incorrect URL format')

    def scrape(self):
        """
        Gets direct video and audio (if exists) urls
        """
        UNQ = getUNQ(self.page)
        if not UNQ:
            Clean(self.path)
            raise BaseException('No video in this post')

        # Getting Qualities and audio (if exists) from mpd file
        mpd = self.get(
                        UNQ + 'DASHPlaylist.mpd',
                        _proxies=self.proxies
                        )
        # v1.0.8: Fix new Reddit mechanism
        VQS, AQS = mpdParse(mpd.text)

        # Check for Audio
        if AQS:
            self.audio = UNQ + j(AQS[0])

        # Select Quality
        if self.max:
            quality = j(VQS[0])
        elif self.min:
            quality = j(VQS[-1])
        else:
            quality = j(UserSelect(VQS))
        
        self.video = UNQ + quality
        self.file_name = '{}{}-{}.mp4'.format(
                                    self.path,
                                    UNQ.split('/')[-2],
                                    quality
                                    # v1.0.8: fix file name dups
                                    ).replace('.mp4' * 2, '.mp4')

    def get_video(self):
        """
        Downloads video to the current working directory
        """
        self.pgbar(self.log, self.video, 'video.mp4', '>> Video:')

    def get_audio(self):
        """
        Downloads audio to the current working directory
        """
        self.pgbar(self.log, self.audio, 'audio.m4a', '>> Audio:')

    def get_and_mux(self):
        """
        Video or muxed video with audio if exists
        """
        self.get_video()

        # v1.0.5: Convert muted videos to be shareable
        if self.audio:
            self.get_audio()
            os.system(
                    'ffmpeg -hide_banner -loglevel panic -y -i video.mp4'
                    ' -i audio.m4a -vcodec copy -acodec copy av.mp4'
                    )
        else:
            os.system(
                    'ffmpeg -hide_banner -loglevel panic -y -i video.mp4'
                    ' -vcodec copy av.mp4'
                    )

        # Moving video file without using shutil
        os.rename('av.mp4', self.file_name)
    
    # v1.0.9: get size and duration
    def check(self):
        """
        Scrapes video and metadata (Duration and size)
        """
        self.ischeck = True
        
        lprint(self.log, '>> Connecting...')
        self.setup()
        
        lprint(self.log, '>> Scraping...')
        self.scrape()
        
        self.duration = getDuration(self.page)
        self.size = int(
                    self.head(
                                self.video,
                                _proxies=self.proxies
                            ).headers['Content-Length']
                        )
    
    def download(self):
        """
        Automatic usage of the class

        Returns:
            self.file_name (str): PATH of the downloaded video
            0: Size exceeds maximum
            1: Duration exceeds maximum
            2: File exists
        """
        if not self.ischeck:
            self.check()
        
        if self.size > self.max_s:
            lprint(self.log, '>> Size > {} bytes'.format(self.max_s))
            return 0
        
        if self.duration > self.max_d:
            lprint(self.log, '>> Duration > {}s'.format(self.max_d))
            return 1
        
        if self.overwrite and ope(self.file_name):
            os.remove(self.file_name)
        
        elif not self.overwrite and ope(self.file_name):
            Clean(self.path)
            lprint(self.log, '{} exists!'.format(
                                    os.path.basename(self.file_name)
                                    )
                                )
            return 2
        
        lprint(self.log, '>> Downloading and Re-encoding...')
        self.get_and_mux()
        
        Clean(self.path)
        lprint(self.log, '>> Done')

        self.ischeck = False
        return self.file_name