import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs4
from urllib.request import urlretrieve
from urllib.parse import unquote
from shutil import copytree 
#	MONDAY SANITY CHECK:
import os, sys
_BASE_DIR_ = os.getcwd()
print(_BASE_DIR_, sys.version)


__author__ = 108806

#TODO: Fix this mess : [VALID URL] :  http://www.wp.pl:80/https://praca.money.pl/oferty-pracy/l/https://sportowefakty.wp.pl/pilka-nozna/920692/premier-league-oficjalnie-chelsea-fc-zwolnila-franka-lamparda




######################################
# HANDLING COMMAND LINE ARGUMENTS:
#######################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-target', '-targetURL', '-t',
    help='URL to download the files from, like http://google.pl',
    type=str,
    required=True)

parser.add_argument('-port', '-p',
    help='Port to connect, default for websites is 80.',
    default='80',
    type=str)

parser.add_argument('--files', '--f', 
    help='File extensions of interest, only this will be downloaded if specified.', 
    nargs='*',
    default=[
     'txt', 'gz', 'lst', '7z', 'zip', 'rar','bzip', 'gzip', 'png', 'jpg', 'db' 
 ])

parser.add_argument('--banned', '-b', '--b',
    help='List banned URL directories here',
    nargs='*',
    default=[...])

parser.add_argument('--recu','--recursive', '--r', '-r',
    help='recursive :  If disabled it will scrape only one url and will never go any deeper.', 
    action='store_true',
    default=False)

parser.add_argument('--INSANE', '-i', '--i', 
    help='insane : Downloads all files with any extension.', 
    action='store_true',
    default=False)

parser.add_argument('--dir', '--directory', '-d', 
    help='Specifies custom directory to save all the downloaded files.', 
    type=str)

parser.add_argument('--URI_decode', '-u', '--uri',
    help='''Decodes URI names of files, 
    so you can have it with nice things like spaces if you need.''',
    default=False,
    action='store_true'
)

args = parser.parse_args()


print(args)
args.target = args.target + ':' + args.port
print(F"Looking for Files with extensions: {args.files} @ {args.target}")
if args.recu : print('[INFO] : RECURSIVE MODE IS ON.')
if args.INSANE : print('[WARNING] : INSANE MODE IS ON')



def FNG(site:str):
    """[FOLDER NAME GENERATOR.
        Creates a str depending on the str given]
    Args:
        site ([type]): [https://example.com:3445]
    Returns:
        str: [https___example_com_3445]
    """
    result_str = ''
    for x in list(site):
        if x.isalnum() : result_str += x
        else: 
            if result_str.endswith('_') or result_str.endswith('@'): continue
            if x == ':' : 
                result_str += "@"
                continue
            result_str += '_'
    return result_str


def FNV(site:str):
    """
    [File Name Validator] 
    Removes all special chars from a string, 
    exceptions are listed below:
    """
    exceptions = ['.', '-', '@', '_', ' ']
    result_str = lambda s : "".join([x for x in s if x.isalnum() or x in exceptions])
    return result_str(site)




_FILES, _URLS = [], []
if not args.dir: dest_dir = FNG(args.target)
else : dest_dir = args.dir




def isValid(_url:str):
	"""
	Checks whether _url is valid URL
    Note : It returns False for valid URLs in other domains.
	"""
	parsed = urlparse(_url)
	return bool(parsed.netloc) and bool(parsed.scheme)




def scrape(_link:str, recursive:bool=False): 
    """[Recursively scrapes website for links]
    Args:
        _link (str): [http://example.com:port]
    """
    r = requests.get(_link) 
    s = bs4(r.text,"html.parser") 
       
    big_list = s.find_all("a")
    
    for ban in args.banned :
        if big_list.__contains__(ban) : big_list.remove(ban)

    for _url in big_list:
        if not _link.endswith('/'): _link += '/' 
        try :
            full_url = _link+_url.attrs['href']
        except KeyError:
            print("[INFO] The dead end.")
            continue
        
        if isValid(full_url): print("[VALID URL] : ", full_url)
        else:
            print("[INVALID URL] : ", full_url)
            continue
        
        #File extension check:
        if full_url.split('.')[-1] in args.files :
            _FILES.append(full_url)
            print("[INFO] File found : ", full_url)
            continue

        if full_url.endswith('/') and full_url not in _URLS:
            _URLS.append(full_url)
            if recursive:
                print("[WARNING] Scraping RECURSIVELY, please be careful.")
                scrape(full_url)

        if args.INSANE and not full_url.endswith('/'):
            _FILES.append(full_url)




def download(files:list, _dest_dir:str, recursive:bool=False):
    """[Downloads all the URLS from the provided list,
        but(!) only if the given URL is valid. (look isValid)]

    Args:
        files (list): [URL list, 'http://' part needed.]
        _dest_dir (str): [Destination to save the files]
        recursive (bool, optional): [Recursive mode, you are advised to be careful with that].
    """


    def dive_in(*KWARGS:list, _FULL_URL_:str, _FILE_:str):

        for K in KWARGS:
            if os.path.exists(K):
                print('[INFO] : Dir exists already - ', K)
                os.chdir(K)
                continue
            else:
                print('[INFO] : Creating directory - ', K)
                os.mkdir(K)
                try:
                    os.chdir(K)
                except FileNotFoundError as e:
                    print("[ERROR] : Couldnt create directory - ", K,
                    os.getcwd())
                    raise(e)

        urlretrieve(_FULL_URL_, FNV(_FILE_))
        try :
            if os.stat(FNV(_FILE_)):
                  print("[INFO] Successfully downloaded : ", _FILE_)
                  print("[DEBUG] CWD - ", os.getcwd())
        except FileNotFoundError as e:
            print(os.getcwd(),
            "[ERROR] : Could download the file : ", _FILE_)
            raise(e)

        os.chdir(os.path.join(_BASE_DIR_,  _dest_dir))


    if not os.path.exists(_dest_dir) : os.mkdir(_dest_dir)
    os.chdir(_dest_dir)
    
    for _LINK in files:
        tree = _LINK.split('/')
        destFile = tree[-1].split(':')[-1] 
        if args.URI_decode: destFile = unquote(destFile)
        tree = [x for x in tree if x][2:-1]
        dive_in(*tree, _FULL_URL_=_LINK, _FILE_=destFile)

    

#######################################
#STARTING THE SCRAPER:
#######################################
if __name__ =="__main__": 
    try:
        scrape(args.target, args.recu)
    except requests.exceptions.InvalidSchema as e:
        print('''
        Full URL nededed!
        example : http://webiste.com (Notice the http part)
        ''')
        print(e)
        sys.exit(1)
    download(_FILES, dest_dir, args.recu)

print("[FILES] :", len(_FILES))
print("[URLS] : ", len(_URLS))
