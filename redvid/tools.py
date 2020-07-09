import re, os

ope = os.path.exists
sep = os.path.sep
j = ''.join

def lprint(switch=0, *args, **kwargs):
    if switch:
        print(*args, **kwargs)

def checkPath(path):
    if not ope(path):
        path = os.getcwd()
    else:
        if os.path.isfile(path):
            path = os.path.dirname(path)
    if path[-1] != sep:
        path += sep
    return path

def toJsonUrl(url):
    parts = url.split('/')
    if len(parts) is 9:
        url = '/'.join(parts[:-1])
    return url + '.json'

def getUNQ(page):
    regex = r'https://v\.redd\.it/[a-zA-Z0-9]+'
    Match = re.findall(regex, page.text)
    UNQ = None
    if Match:
        UNQ = Match[0]
        UNQ += '/' if UNQ[-1] != '/' else UNQ
    return UNQ

# v1.0.9: getting duration
def getDuration(page):
    dur = re.findall(r'"duration": (\d+)', page.text)
    return int(dur[0]) if dur else None

def mpdParse(mpd):
    # v1.0.8: Fix for new reddit mechanism
    tag_vid = r'<BaseURL>(DASH_)?(\d+)(\.mp4)?</BaseURL>'
    tag_aud = r'<BaseURL>(DASH_)?(audio)(\.mp4)?</BaseURL>'
    lst_vid = re.findall(tag_vid, mpd)
    yield sorted(lst_vid, key=lambda a: int(a[1]))[::-1]
    yield re.findall(tag_aud, mpd)

def UserSelect(lst):
    print('\nQualities available:')
    for n, i in enumerate(lst):
        print('  [{}] {}p'.format(n + 1, i[1]))
    ql = input('\nChoose Quality: ')
    # If a dumbass chose nothing
    try:
        lst[int(ql) - 1]
    except:
        ql = 1
    return lst[int(ql) - 1]

def Clean(path):
    p = path + 'temp' + sep
    if not ope(p):
        return
    os.chdir(path)
    for i in os.listdir(p):
        os.remove(p + i)
    os.rmdir(p)