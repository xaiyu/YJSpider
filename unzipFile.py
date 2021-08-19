
import zipfile

def unFile():
    filezip = zipfile.ZipFile("./小容仔咕咕咕w - NO.05 白T.zip")
    zipList = filezip.namelist()
    for i in zipList:
        filezip.extract(i, "./", pwd=b"leshe")
    filezip.close()
unFile()
