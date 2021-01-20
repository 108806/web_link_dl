import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs4
from urllib.request import urlretrieve
#	MONDAY SANITY CHECK:
import os, sys
print(os.getcwd(), sys.version)

__author__ = 108806
__version__ = 0.2

def HALP():
    """
    This will recursively download all the files from the given url, 
    but only with the speficied extensions.
    
    [WARNING!] 
    This will also download files from every link found in every link in a domain, 
    use --single-page to disable this feature.
    
    USAGE : python3 web_link_dl.py http://1.3.3.7:80 txt,bzip,gzip
    USAGE : python3 web_link_dl.py http://tfr.org/cisco-ios/37xx/3725/ bin --single-page
    
    If the second parameter somehow fails, default extensions list will be used :
    [
    'txt', 'gz', 'lst', '7z', 'zip', 'rar','bzip', 'gzip', 'png', 'jpg', 'db'
    ]
    
    """
    print(HALP.__doc__)

arg1 = sys.argv[1].lower()
H = [ 'halp', 'help', 'h', '-h', '-help','--help' ]
if arg1 in H:
    HALP()
    sys.exit(0)


def FNG(site):
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


addr = sys.argv[1] #EXAMPLE : 'http://1.3.3.142:48000'

try:
    extensions = sys.argv[2].replace(' ', '')
except IndexError:
    #[WARNING]! 
    #Files with all of these extensions and with only these will be downloaded!
    extensions = [ 
    'txt', 'gz', 'lst', '7z', 'zip', 'rar','bzip', 'gzip', 'png', 'jpg', 'db' 
    ]

recu = True
arg3 =  sys.argv[3].strip()  
if arg3 == '--singlepage' or arg3 == '--single-page':
    recu = False
print("RECURSIVE SET AS ", recu)

files, urls = [], []
dest_dir = FNG(addr)
print(dest_dir)




def isvalid(_url:str):
	"""
	Checks whether _url is valid URL
	"""
	parsed = urlparse(_url)
	return bool(parsed.netloc) and bool(parsed.scheme)


def scrape(_link:str, recursive:bool=True): 
    """[Recursively scrapes website for links]
    Args:
        _link (str): [http://example.com:port]
    """
    r = requests.get(_link) 
    s = bs4(r.text,"html.parser") 
       
    big_list = s.find_all("a")
    
    for _url in big_list:
        if not _link.endswith('/'): _link += '/' 
        full_url = _link+_url.attrs['href']
        
        if isvalid(full_url): print("[VALID URL] : ", full_url)
        else:
            print("[INVALID URL] : ", full_url)
            continue
        
        if full_url.split('.')[-1] in extensions:
            files.append(full_url)
            continue

        if full_url.endswith('/') and full_url not in urls:
            urls.append(full_url)
            if recursive:
                print("[WARNING] Scraping RECURSIVELY, please be careful.")
                scrape(full_url)


def download(files:list, _dest_dir:str, recursive:bool=True):
    if not os.path.exists(_dest_dir) : os.mkdir(_dest_dir)
    os.chdir(_dest_dir)
    for file in files:
        url_parts = file.split('/')
        if len(url_parts) > 4 and recu:
            #Add netloc to filenames from high dirs only.
            dest = file.split('/')[-2] + '@' + file.split('/')[-1] 
        else : dest = url_parts[-1]
        urlretrieve(file, dest)
        if os.path.exists(dest): print("[INFO] Successfully downloaded : ", dest)
        else: print("[ERROR] : Could not downlload  :", dest)
        
    
if __name__ =="__main__": 
    scrape(addr, recu)
    download(files, dest_dir, recu)
    
print("[FILES] :", len(files))
print("[URLS] : ", len(urls))

