import re, os

ope = os.path.exists

def checkPath(path):
    if not ope(path):
        path = os.getcwd()
    else:
        if os.path.isfile(path):
            path = os.path.dirname(path)
    if path[-1] != '\\':
        path += '\\'
    return path

def isValid(url):
    Match = r'(?P<url>https?://(?:[^/]+\.)?reddit\.com/r/[^/]+/comments/(?P<id>[^/?#&]+))'
    if re.search(Match, url):
        parts = [i for i in url.split('/') if i]
        if 6 < len(parts) < 9:
            return True
    return False
    
'''def toDic(data):
    return json.loads(data)'''

def toJsonUrl(url):
    if isValid(url):
        parts = url.split('/')
        if len(parts) is 9:
            url = '/'.join(parts[:-1])
        return url + '.json'
    return None

def getUNQ(page):
    regex = r'https://v\.redd\.it/[a-zA-Z0-9]+'
    Match = re.findall(regex, page.text)
    UNQ = None
    if Match:
        UNQ = Match[0]
        UNQ += '/' if UNQ[-1] != '/' else UNQ
    return UNQ
    
def mpdParse(mpd):
    tag = r'<BaseURL>(.*?)</BaseURL>'
    extracted = re.findall(tag, mpd)
    return extracted

def hasAudio(lst):
    return any(i == 'audio' for i in lst)

def UserSelect(lst):
    print('\nQualities available:')
    for n, i in enumerate(lst):
        i = i.split('_')[1]
        print('  [{}] {}p'.format(n + 1, i))
    ql = input('\nChoose Quality: ')
    # If a dumbass chose nothing
    try:
        lst[int(ql) - 1]
    except:
        ql = 1
    return lst[int(ql) - 1]

def Clean(path):
    p = path + 'temp\\'
    if not ope(p):
        return
    os.chdir(path)
    for i in os.listdir(p):
        os.remove(p+i)
    os.rmdir(p)

def Clear(text, elements=[], tgt=''):
    for element in elements:
        text = text.replace(element, tgt)
    return text