# WEB LINKS DOWNLOADER
Recursive scraper and file downloader writen in python 3, console tool by design.

This will recursively download all the files from the given url,
    but only with the speficied extensions.
    
    USAGE : python3 web_link_dl.py http://1.3.3.7:80 txt,bzip,gzip
    
    If second parameter is not provided, uses default extensions list of :
    [
    'txt', 'gz', 'lst', '7z', 'zip', 'rar','bzip', 'gzip', 'png', 'jpg', 'db'
    ]

Important NOTE : This tool creates a dir in the working dir for any target provided to avoid filename collisions.
