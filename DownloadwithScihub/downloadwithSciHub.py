from scihub import SciHub

sh = SciHub()

# def FetchDOIAndDownload(doi):
#     result = sh.download(identifier=doi, path='F:\Software\Pycharm\workspace\zhiwang_spider\zhiwang_spider\DownloadwithScihub\ppp.pdf')
#     print(result)

if "__name__" == "__main__":
    result = sh.fetch('http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1648853')
    print(result)
    # doi = "10.1109/ICDCS.2006.48"
    # FetchDOIAndDownload(doi)