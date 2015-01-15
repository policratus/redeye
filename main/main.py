from utils import files
from basic import spatial,io

def main():
    f = files.fileutils()
    s = spatial.spatial()
    i = io.io()

    filelist = f.filelist('.jpg','/hdd/Pictures')

    for ofile in filelist:
       rotated = s.rotation(ofile)
       i.show(rotated)
if __name__ == '__main__':
    main()
