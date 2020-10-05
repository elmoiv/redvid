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
    regex = r'/([a-zA-Z0-9]+)/DASHPlaylist.mpd'
    Match = re.findall(regex, page.text)
    UNQ = None
    if Match:
        UNQ = Match[0]
    return UNQ

# v1.0.9: getting duration
def getDuration(page):
    dur = re.findall(r'"duration": (\d+)', page.text)
    return int(dur[0]) if dur else None

# v1.1.0: looping through qualities to get all sizes
def getSizes(u, h, p, vs):
    sizes = []
    for v in vs:
        sizes.append(
            (v, int(h(
                u + j(v),
                _proxies=p
            ).headers['Content-Length']))
        )
    return sizes

# v1.1.1: if 'vcf.redd.it' in <BASEURL>
# we extract DASH quality names and store them in
# the same form of original re.findall result
def vcfRemover(BaseUrls, rgx):
    vcfRemovedUrls = map(
        lambda i: j(i).split('?')[0].split('/')[-1],
        BaseUrls
    )
    convertToReTags = map(
        lambda i: re.findall(rgx, f'<BaseURL>{i}</BaseURL>')[0],
        vcfRemovedUrls
    )
    return list(convertToReTags)

def mpdParse(mpd):
    # v1.0.8: Fix for new reddit mechanism
    tags = r'<BaseURL>(DASH_)?(.*?)(\.mp4)?</BaseURL>'
    re_tags = re.findall(tags, mpd)

    # v1.1.1: Fix Base Urls from vcf.redd.it
    if any('vcf.redd.it' in j(i) for i in re_tags):
        re_tags = vcfRemover(re_tags, tags)

    # Filter audio tag
    tag_aud = None
    for tag in re_tags:
        if 'audio' in tag:
            tag_aud = tag
            re_tags.remove(tag)
    
    if not re_tags:
        return 0, 0

    # Allow getting qualities with old reddit method
    try:
        yield sorted(re_tags, key=lambda a: int(a[1]))[::-1]
    except:
        yield sorted(re_tags, key=lambda a: a[1])[::-1]

    yield tag_aud

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