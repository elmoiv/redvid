from secrets import token_urlsafe
from .requestmaker import Requester
from .tools import *
from uuid import uuid4

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
                filename='',
                max_q=False,
                min_q=False,
                max_d=1e1000,
                max_s=1e1000,
                auto_max=False,
                auto_dir=True,
                log=True,
                proxies={}
                ):
        self.path, self.url, self.proxies = path, url, proxies
        self.max, self.min, self.log = max_q, min_q, log
        self.max_d, self.max_s = max_d, max_s
        self.auto_max = auto_max
        self.auto_dir = auto_dir
        self.sizes_error = False
        self.filename = filename  # Store the desired filename
        self.page = None
        self.overwrite = False
        self.ischeck = False
        self.UNQ = None
        self.r_url = None
        self.videos = []
        self.video, self.audio, self.file_name = '', '', ''
        self.duration, self.size = 0, 0
        self.__unique_id = str(uuid4())
        
    def setup(self):
        """
        Checks PATH and URL for any errors
        """
        self.ischeck = False
        self.is_catch_errors = False
        
        if not self.log:
            if not self.max and not self.min:
                self.max = True

        self.path = checkPath(self.path, self.auto_dir)
        
        # v1.1.2: Fix recursive path by providing static
        # temp path
        self.temp = opj(self.path, 'redvid_temp', token_urlsafe()) + sep
        os.makedirs(self.temp, exist_ok=True)
        
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
        
        if self.page.status_code == 200:
            return True
        
        raise BaseException('Incorrect URL format')

    def scrape(self):
        """
        Gets direct video and audio (if exists) urls
        """
        self.UNQ = getUNQ(self.page)

        if not self.UNQ:
            Clean(self.temp)
            raise BaseException('No video in this post')
        
        self.r_url = 'https://v.redd.it/' + self.UNQ + '/'

        # Getting Qualities and audio (if exists) from mpd file
        mpd = self.get(
                        self.r_url + 'DASHPlaylist.mpd',
                        _proxies=self.proxies
                        )
        
        max_min_qualities = getMaxMinQualities(self.page, self.r_url)

        # v1.0.8: Fix new Reddit mechanism
        VQS, AQS = mpdParse(mpd.text, custom_video_qualities=max_min_qualities)

        if [VQS, AQS] == [0, 0]:
            raise BaseException('Qualities not found!')

        self.videos = VQS

        # Check for Audio
        if AQS:
            self.audio = self.r_url + j(AQS)

    def get_video(self):
        """
        Downloads video to the current working directory
        """
        self.pgbar(self.log, self.video, self.temp + self.__unique_id + 'video.mp4', '>> Video:')

    def get_audio(self):
        """
        Downloads audio to the current working directory
        """
        self.pgbar(self.log, self.audio, self.temp + self.__unique_id + 'audio.m4a', '>> Audio:')

    def get_and_mux(self):
        """
        Video or muxed video with audio if exists
        """
        self.get_video()

        # v1.0.5: Convert muted videos to be shareable
        if self.audio:
            self.get_audio()
            os.system(
                    'ffmpeg -hide_banner -loglevel panic -y -i "{0}video.mp4"'
                    ' -i "{0}audio.m4a" -vcodec copy -acodec copy "{0}av.mp4"'.format(
                        self.temp + self.__unique_id
                    )
                )
        else:
            os.system(
                    'ffmpeg -hide_banner -loglevel panic -y -i "{0}video.mp4"'
                    ' -vcodec copy "{0}av.mp4"'.format(
                        self.temp + self.__unique_id
                    )
                )

        # Moving video file without using shutil
        os.rename(self.temp + self.__unique_id + 'av.mp4', self.file_name)

        # Clean Temp folder
        Clean(self.temp)
    
    # v1.0.9: get size and duration
    def check(self):
        """
        Scrapes video and metadata (Duration and size)
        """
        lprint(self.log, '>> Connecting...')
        self.setup()
        
        lprint(self.log, '>> Scraping...')
        self.scrape()
        
        quality = None

        # Select Quality
        self.sizes_error = False

        # v1.1.0: Get quality according to max size
        if self.auto_max:
            lprint(self.log, '>> Getting quality according to max size.')
            sizes = getSizes(
                            self.r_url,
                            self.head,
                            self.proxies,
                            self.videos
                            )
            
            # Loop through qualities and compare each size to max_s
            for v, s in sorted(sizes, key=lambda i: i[1])[::-1]:
                if s <= self.max_s:
                    quality = j(v)
                    break
            
            # Store error if no quality is <= max_s
            if not quality:
                lprint(self.log, '>>>> All qualities are > {} bytes' \
                                 .format(self.max_s))
                self.sizes_error = True
                return
        else:
            if self.max:
                quality = j(self.videos[0])
            elif self.min:
                quality = j(self.videos[-1])
            else:
                quality = j(UserSelect(self.videos))
        
        self.video = self.r_url + quality

        self.file_name = '{}{}.mp4'.format(
                                    self.path,
                                    self.filename if self.filename else '-'.join(
                                        [self.UNQ,
                                        quality]
                                    )
                                    # v1.0.8: fix file name dups
                                    ).replace('.mp4' * 2, '.mp4')
        
        self.duration = getDuration(self.page)
        if not self.auto_max:
            self.size = int(
                        self.head(
                                self.video,
                                _proxies=self.proxies
                            ).headers['Content-Length']
                        )
        
        self.ischeck = True

    def download(self):
        """
        Automatic usage of the class
        Returns:
            self.file_name (str): PATH of the downloaded video
            0: Size exceeds maximum
            1: Duration exceeds maximum
            2: File exists
        """
        self.__unique_id = str(uuid4())

        if not self.ischeck:
            self.check()
        self.ischeck = False
        
        if self.size > self.max_s or self.sizes_error:
            lprint(self.log, '>> Size > {} bytes'.format(self.max_s))
            return 0
        
        if self.duration:
            if self.duration > self.max_d:
                lprint(self.log, '>> Duration > {}s'.format(self.max_d))
                return 1
        
        if self.overwrite and ope(self.file_name):
            os.remove(self.file_name)
        
        elif not self.overwrite and ope(self.file_name):
            Clean(self.temp)
            lprint(self.log, '{} exists!'.format(
                                    os.path.basename(self.file_name)
                                    )
                                )
            return 2
        
        lprint(self.log, '>> Downloading and Re-encoding...')
        self.get_and_mux()
        
        Clean(self.temp)
        lprint(self.log, '>> Done')

        return self.file_name
    
    def clean_temp(self):
        Clean(opj(self.path, 'redvid_temp'))