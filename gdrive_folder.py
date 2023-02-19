import gdown

def downloadFolder(url):
    try:
        if url.split('/')[-1]=='?usp=sharing':
            url=url.replace('?usp=sharing','')
            gdown.download_folder(url)
    except Exception:
        print("Some error occured")