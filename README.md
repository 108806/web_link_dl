# WEB LINKS DOWNLOADER
Recursive scraper and file downloader writen in python 3, console tool by design.

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

NOTE : This version creates a directory in the working dir for every target provided.
