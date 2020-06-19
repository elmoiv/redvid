from .requestmaker import Requester
from .tools import *
import os

class Downloader(Requester):
    '''
    # [redvid](https://github.com/elmoiv/redvid):

    ### Smart downloader for Reddit hosted videos

    - `path`: downloads folder path
    - `proxies`: if you want to use proxy while connecting to reddit
        - proxies should be of type `dict` in the form of:
            
             {

                "http":"xxx.xxx.xxx.xx",
                "https":"xxx.xxx.xxx.xx",
                ... etc

            } 
    
    '''
    def __init__(self, path='', proxies={}):
        self.proxies = proxies
        self.path = checkPath(path)
        Clean(self.path)
        os.chdir(self.path)
        os.makedirs('temp', exist_ok=True)
        os.chdir('temp')

    def setup(self, url):
        '''
        #### output: 
        - Checks if the reddit url is correct

        #### params:
        - `url`: `url` of the video post webpage
            - ex: https://www.reddit.com/r/WTF/comments/d3x4wj/fire_tornado_in_central_brazil_goi%C3%A1s/
        '''
        if isValid(url):
            return self.scrape(url)
        Clean(self.path)
        raise BaseException('Incorrect URL format')
        
    def get_video(self, url):
        '''
        #### output: 
        - Downloads video to the current working directory

        #### params:
        - `url`: direct `url` of the video
            - ex: https://v.redd.it/gzc9cijcavm31/DASH_720
        '''
        print('\n- Video:')
        self.pgbar(url, 'video.mp4')

    def get_audio(self, url):
        '''
        #### output: 
        - Downloads audio to the current working directory

        #### params:
        - `url`: direct `url` of the audio
            - ex: https://v.redd.it/gzc9cijcavm31/audio
        '''
        print('\n- Audio:')
        self.pgbar(url, 'audio.m4a')

    def mux_all(self, video, audio, ID):
        '''
        #### output: 
        - Video or muxed video with sound if exists

        #### params:
        - `video`: direct `url` of the video
            - ex: https://v.redd.it/gzc9cijcavm31/DASH_720
        - `audio`: direct `url` of the audio
            - if not exists, set it to `None`
        - `ID`: the id of the direct url
            - ex: v.redd.it/`ID`/DASH_720
        '''
        self.get_video(video)
        video_filename = '{}{}.mp4'.format(self.path, ID)

        # v1.0.5: Converting videos without audio to solve unshareable videos bug
        if not audio:
            os.system('ffmpeg -hide_banner -loglevel panic -y -i video.mp4 -vcodec copy av.mp4')
            # Moving video file without using shutil
            os.rename('video.mp4', video_filename)
            return
        
        self.get_audio(audio)
        
        # Using FFmpeg to mux audio and video
        # -hide_banner: hide header text
        # -loglevel: we set it to `panic` to disable logging but Errors
        print('\n- Merging A/V...')
        os.system('ffmpeg -hide_banner -loglevel panic -y -i video.mp4 -i audio.m4a -vcodec copy -acodec copy av.mp4')
        
        os.rename('av.mp4', video_filename)

    def scrape(self, url):
        '''
        #### output: 
        - returns a tuple: `(video_url, audio_url, ID)`

        #### params:
        - `url`: `url` of the video post webpage
            - ex: https://www.reddit.com/r/WTF/comments/d3x4wj/fire_tornado_in_central_brazil_goi%C3%A1s/
        '''
        video, audio = None, None
        page = self.get(url, _proxies=self.proxies)
        
        # Getting https://v.redd.it/{ID}
        UNQ = getUNQ(page) # Set UNQ = None for testing
        if not UNQ:
            # If we can't scrape the url from the page
            # We try to extract them from the json url of reddit
            directUrl = toJsonUrl(url)
            if directUrl:
                UNQ = getUNQ(self.get(directUrl, _proxies=self.proxies))
                if not UNQ:
                    Clean(self.path)
                    raise BaseException('No video in this post')
        
        ID = UNQ.split('/')[-2]

        # Getting Qualities and audio (if exists) from mpd file
        mpd = self.get(UNQ + 'DASHPlaylist.mpd', _proxies=self.proxies)
        VQS = mpdParse(mpd.text)

        # Check for Audio
        if hasAudio(VQS):
            audio = UNQ + VQS.pop(-1)

        # Select Quality
        video = UNQ + UserSelect(VQS)
        return video, audio, ID
        
    def download(self, url):
        '''
        ### Automatic usage of the class functions
        #### output: 
        - #### Does the hard work for you :)

        #### params:
        - `url`: `url` of the video post webpage
            - ex: https://www.reddit.com/r/WTF/comments/d3x4wj/fire_tornado_in_central_brazil_goi%C3%A1s/
        '''
        print('\n- Scraping...')
        video, audio, ID = self.setup(url)
        file_path = '{}{}.mp4'.format(self.path, ID)
        if os.path.exists(file_path):
            Clean(self.path)
            raise FileExistsError
        self.mux_all(video, audio, ID)
        Clean(self.path)
        print('\nDone')
        return file_path
